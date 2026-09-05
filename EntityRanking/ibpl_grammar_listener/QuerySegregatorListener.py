from .o9IBPLListener import o9IBPLListener
from .o9IBPLParser import o9IBPLParser
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.ErrorStrategy import DefaultErrorStrategy, InputMismatchException
from antlr4.atn.ATNState import ATNState


# Dimension names that should never contribute to the members list.
_EXCLUDED_DIMENSIONS = frozenset({'version', 'time'})


class ErrorStrategy(DefaultErrorStrategy):
    def sync(self, recognizer):
        s = recognizer._interp.atn.states[recognizer.state]
        if not self.errorRecoveryMode:
            el = recognizer.getTokenStream().LA(1)
            if el != -1 and not self.nextTokensContains(recognizer, s, el) and not recognizer.isExpectedToken(el):
                state_type = s.stateType
                if state_type in {ATNState.BLOCK_START, ATNState.PLUS_BLOCK_START, ATNState.STAR_BLOCK_START, ATNState.STAR_LOOP_ENTRY}:
                    if self.singleTokenDeletion(recognizer) is None:
                        raise InputMismatchException(recognizer)
                    return

                if state_type in {ATNState.TOKEN_START, ATNState.RULE_STOP, ATNState.BLOCK_END}:
                    pass
                elif state_type in {ATNState.STAR_LOOP_BACK, ATNState.PLUS_LOOP_BACK}:
                    self.reportUnwantedToken(recognizer)
                    set = recognizer.getExpectedTokens().union(self.getErrorRecoverySet(recognizer))
                    self.consumeUntil(recognizer, set)
                else:
                    return

    def nextTokensContains(self, recognizer, s, el):
        return el in recognizer._interp.atn.nextTokens(s)


class SyntaxError:
    def __init__(self, line, column, msg, offendingSymbol):
        self.line = line
        self.column = column
        self.msg = msg
        self.offendingSymbol = offendingSymbol


class ListErrorReporter(ErrorListener):
    def __init__(self, raise_on_error: bool = True):
        super().__init__()
        self.raise_on_error = raise_on_error
        self._errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error = SyntaxError(line, column, msg, offendingSymbol.text if offendingSymbol else "")
        self._errors.append(error)
        if self.raise_on_error:
            raise Exception(f"ANTLR Parse Error: line {line}:{column} {msg}")

    def getErrors(self):
        return self._errors


class QueryInfoListener(o9IBPLListener):
    """
    Collects structured query information for every top-level statement in
    an o9IBPL parse tree.

    After a tree walk, self.results is a list of dicts — one per top-level
    statement — each with the following keys:

        query       : str   — raw text of the full statement
        query_type  : str   — 'Select', 'Scope', 'Update', 'Assignment', …
        dim_attrs   : list  — [{'dimName': str, 'attrName': str}, …]
                              de-duplicated dimension.attribute pairs
        named_sets  : list  — named set / resolvable identifiers (& $$ %%)
                              de-duplicated
        measures    : list  — measure / transient / edge property names
                              de-duplicated
        coalesce_measures : list — measures that appear inside coalesce() calls
        lead_offsets : list — [{'base', 'offset', 'applied_to'}, …]
        filters     : list  — mixed list of filter entries:
                                str                  — standalone member /
                                                       graph reference with no
                                                       separate subject
                                {subject: expression}— single-key dict when
                                                       subject can be cleanly
                                                       separated from the
                                                       predicate
        object      : dict | None — contextual dict for the primary entity
        arguments   : dict  — key-value pairs from json / commandOption /
                              ARGUMENTS clauses
        members     : list  — concrete member/fact values (sorted).
                              Pinpoint member values, comparison RHS values,
                              assignment RHS values, and JSON string values
                              from exec procedure calls.
                              Excludes time and version dimension members.

    Nested statements (e.g. inside SCOPE … END SCOPE blocks) contribute
    their data to the enclosing statement's result dict rather than
    producing a separate entry.

    Parameters
    ----------
    members_only : bool
        When True, only 'query' and 'members' are populated per statement.
        All query-info listeners (query_type, dim_attrs, measures, filters, …)
        short-circuit immediately, leaving only member collection running.
    """

    def __init__(self, members_only: bool = False):
        self.results: list[dict] = []

        self._members_only: bool = members_only

        self._stmt_depth: int = 0
        # Stack of saved parent frames — one entry pushed per enterStatement,
        # popped on exitStatement.  Each nested statement gets its own isolated
        # _current so dim_attrs/measures/named_sets/members never leak between
        # a procedure body and its nested scope/assignment statements.
        self._stack: list = []
        self._current: dict | None = None

        self._dim_attr_seen:  set = set()
        self._measure_seen:   set = set()
        self._named_set_seen: set = set()

        self._filter_depth:   int = 0
        self._coalesce_depth: int = 0

        # Member collection state — reset per statement (any depth).
        self._members:      set  = set()
        self._in_exec_proc: bool = False

        # Formulae collection state — reset per statement.
        # _formula_lhs_measure: measure name on the LHS of an assignment rule.
        # _coalesce_args_stack: one list per open coalesce call, so each call's
        #   entities can be captured as a separate tuple in the formula output.
        self._formula_lhs_measure: str | None = None
        self._coalesce_args_stack: list[list] = []

    # ------------------------------------------------------------------
    # Helpers — query info
    # ------------------------------------------------------------------

    @staticmethod
    def _strip(text: str) -> str:
        """Remove surrounding square brackets or double-quotes."""
        return text.strip('[]"')

    def _active(self) -> bool:
        """True whenever a statement is being walked, at any nesting depth."""
        return self._current is not None

    def _qi_active(self) -> bool:
        """True when inside a statement AND query-info collection is enabled.
        In members_only mode all pure query-info listeners short-circuit via
        this guard, leaving only member collection running."""
        return self._current is not None and not self._members_only

    def _add_dim_attr(self, dim: str, attr: str) -> None:
        key = (dim, attr)
        if key not in self._dim_attr_seen:
            self._dim_attr_seen.add(key)
            self._current['dim_attrs'].append({'dimName': dim, 'attrName': attr})

    def _add_measure(self, name: str) -> None:
        if name not in self._measure_seen:
            self._measure_seen.add(name)
            self._current['measures'].append(name)

    def _add_coalesce_measure(self, name: str) -> None:
        """Record a measure inside a coalesce() call.
        Also adds to the regular measures list for completeness.
        Additionally appends the name to the innermost open coalesce arg-list
        so exitStatement can produce one tuple per coalesce call."""
        self._add_measure(name)
        seen_key = f'__coalesce__{name}'
        if seen_key not in self._measure_seen:
            self._measure_seen.add(seen_key)
            self._current['coalesce_measures'].append(name)
        # Feed the per-call accumulator (innermost open coalesce).
        if self._coalesce_args_stack:
            self._coalesce_args_stack[-1].append(name)

    def _add_named_set(self, name: str) -> None:
        if name not in self._named_set_seen:
            self._named_set_seen.add(name)
            self._current['named_sets'].append(name)

    def _set_filter(self, subject: str | None, expression: str) -> None:
        """Append a filter entry.
        - If subject is None or equals expression, store as a plain string.
        - Otherwise store as a single-key dict {subject: expression}.
        """
        if subject is None or subject == expression:
            self._current['filters'].append(expression)
        else:
            self._current['filters'].append({subject: expression})

    def _in_filter_ctx(self) -> bool:
        """True when the walker is inside a filter-set context."""
        return self._qi_active() and self._filter_depth > 0


    def _set_query_type(self, query_type: str) -> None:
        """Set query_type only if it has not already been set."""
        if not self._current['query_type']:
            self._current['query_type'] = query_type

    def _set_query(self, query: str) -> None:
        """Override the query text for this statement.
        Guards on 'query' (not 'query_type') so that the first specific enter
        method that fires can refine the text set by enterStatement, without
        later sibling statements from overwriting it."""
        if not self._current['query']:
            self._current['query'] = query

    @staticmethod
    def _find_first_measure_name(ctx):
        """DFS walk returning the first Measure_nameContext descendant, or None."""
        if isinstance(ctx, o9IBPLParser.Measure_nameContext):
            return ctx
        for i in range(ctx.getChildCount()):
            result = QueryInfoListener._find_first_measure_name(ctx.getChild(i))
            if result is not None:
                return result
        return None

    def _find_parent_of_type(self, ctx, target_type):
        """Walk up the parse tree, returning the first ancestor that is an
        instance of target_type.  target_type may be a single type or a tuple
        of types (same semantics as isinstance)."""
        parent = ctx.parentCtx
        while parent is not None:
            if isinstance(parent, target_type):
                return parent
            parent = parent.parentCtx
        return None

    @staticmethod
    def _scalar_subject(scalar_ctx) -> str | None:
        """Walk the operator-precedence tree to extract the leftmost operand.
        Returns None when the expression is compound or the walk fails."""
        try:
            return (
                scalar_ctx
                .condExpr()
                .orExpr()
                .andExpr(0)
                .equExpr(0)
                .notEquExpr(0)
                .inScalarSetExpr(0)
                .relExpr()
                .relStrExpr(0)
                .addExpr(0)
                .subExpr(0)
                .mulExpr(0)
                .divExpr(0)
                .modExpr(0)
                .powExpr(0)
                .unaryExpr()
                .valueExpr()
                .getText()
            )
        except (AttributeError, TypeError, IndexError):
            return None

    def _base_subject(self, mem_ctx, emit: bool = False) -> str:
        """Recursively find the canonical base subject of a member expression,
        stripping filter and level-attribute wrappers.

        When emit=True, calls _set_filter for every MemberLevelAttribute node
        stripped along the way.

        Rules applied bottom-up:
          MemberFilter         → recurse transparently
          MemberLevelAttribute → if emit: record {base: member}; return base text
          Other wrapper        → recurse into single child member_expression
        """
        if isinstance(mem_ctx, o9IBPLParser.MemberFilterContext):
            return self._base_subject(mem_ctx.member_expression(), emit=emit)

        if isinstance(mem_ctx, o9IBPLParser.MemberLevelAttributeContext):
            base_text = mem_ctx.member_expression().getText()
            if emit:
                member = self._strip(mem_ctx.identifier().getText())
                self._set_filter(base_text, member)
            return base_text

        child_result = getattr(mem_ctx, 'member_expression', lambda: None)()
        if child_result is None or isinstance(child_result, list):
            return mem_ctx.getText()

        stripped = self._base_subject(child_result, emit=emit)
        if stripped == child_result.getText():
            return mem_ctx.getText()

        full_text  = mem_ctx.getText()
        child_text = child_result.getText()
        if full_text.startswith(child_text):
            return stripped + full_text[len(child_text):]
        return full_text

    @staticmethod
    def _parse_json_value(vctx) -> 'str | list | dict | None':
        """Recursively parse a jsonValue context into a native Python value."""
        if vctx is None:
            return None
        jo = vctx.jsonObject() if hasattr(vctx, 'jsonObject') else None
        if jo is not None:
            result = {}
            for pair in (jo.jsonPair() or []):
                ks  = pair.jsonstring()
                key = ks.getText().strip('"\'') if ks else pair.getText()
                val = QueryInfoListener._parse_json_value(pair.jsonValue())
                result[key] = val
            return result
        ja = vctx.jsonArray() if hasattr(vctx, 'jsonArray') else None
        if ja is not None:
            return [
                QueryInfoListener._parse_json_value(item)
                for item in (ja.jsonValue() or [])
            ]
        js = vctx.jsonstring() if hasattr(vctx, 'jsonstring') else None
        if js is not None:
            return js.getText().strip('"\'')
        return vctx.getText()

    @staticmethod
    def _extract_json_args(json_ctx) -> dict:
        """Walk json → jsonValue → jsonObject → jsonPair* and return a
        {key: value} dict.  JSON_BLOCK is returned as {'_raw': block_text}."""
        if json_ctx is None:
            return {}
        try:
            jv = json_ctx.jsonValue() if hasattr(json_ctx, 'jsonValue') else None
            if jv is None:
                raw = json_ctx.getText().strip('{}')
                return {'_raw': raw}
            jo = jv.jsonObject() if hasattr(jv, 'jsonObject') else None
            if jo is None:
                return {'_value': QueryInfoListener._parse_json_value(jv)}
            result = {}
            for pair in (jo.jsonPair() or []):
                ks  = pair.jsonstring()
                key = ks.getText().strip('"\'') if ks else pair.getText()
                result[key] = QueryInfoListener._parse_json_value(pair.jsonValue())
            return result
        except (AttributeError, TypeError):
            return {}

    @staticmethod
    def _extract_command_option_args(ctx) -> dict:
        """Walk commandOption* children and return {identifier: value} dict."""
        args = {}
        try:
            for opt in (ctx.commandOption() or []):
                identifiers = opt.identifier()
                if not identifiers:
                    continue
                key = identifiers[0].getText().strip('"\'[]')
                if len(identifiers) > 1:
                    val = identifiers[1].getText().strip('"\'[]')
                elif opt.bools() is not None:
                    val = opt.bools().getText()
                elif opt.INTEGERS() is not None:
                    sign = '-' if opt.MINUS() is not None else ''
                    val = sign + opt.INTEGERS().getText()
                else:
                    val = opt.getText()
                args[key] = val
        except (AttributeError, TypeError):
            pass
        return args

    # ------------------------------------------------------------------
    # Helpers — member collection
    # ------------------------------------------------------------------

    def _add_member(self, value: str) -> None:
        """Add a concrete member value to the per-statement members set."""
        if value:
            self._members.add(value)

    @staticmethod
    def _extract_dimension(text: str) -> str:
        """Return the leading dimension name from a dotted expression."""
        part = text.split('.')[0] if '.' in text else text
        return part.replace('[', '').replace(']', '').strip()

    @staticmethod
    def _is_excluded_dimension(dim: str) -> bool:
        return dim.strip().lower() in _EXCLUDED_DIMENSIONS

    @staticmethod
    def _should_collect(lhs_clean: str, dim_clean: str) -> bool:
        """True when the LHS/dimension warrants member collection."""
        if '#.key' in lhs_clean or lhs_clean.startswith('time'):
            return False
        return dim_clean not in _EXCLUDED_DIMENSIONS

    @staticmethod
    def _is_measure_or_transient(lhs_clean: str) -> bool:
        return 'measure' in lhs_clean or 'transient' in lhs_clean

    @staticmethod
    def _extract_identifier_text(expr_ctx) -> str | None:
        """Extract a member/fact identifier string from an expression context."""
        for child in expr_ctx.getChildren():
            if callable(getattr(child, 'identifier', None)):
                id_node = child.identifier()
                if id_node:
                    return id_node.getText()
            elif callable(getattr(child, 'QUOTEDID', None)):
                id_node = child.QUOTEDID()
                if id_node:
                    return id_node.getText()
            elif callable(getattr(child, 'STRING', None)):
                id_node = child.STRING()
                if id_node:
                    return id_node.getText()
        text = expr_ctx.getText()
        if (text.startswith('"') and text.endswith('"')) or \
           (text.startswith('[') and text.endswith(']')):
            return text
        return None

    def _get_dimension_from_member_filter(self, ctx) -> str | None:
        """Walk up to the nearest MemberFilter context and return its dimension name."""
        filter_ctx = self._find_parent_of_type(ctx, o9IBPLParser.MemberFilterContext)
        if not filter_ctx:
            return None
        member_expr = filter_ctx.member_expression()
        if not member_expr:
            return None
        return self._extract_dimension(member_expr.getText())

    # ------------------------------------------------------------------
    # Statement boundary
    # ------------------------------------------------------------------

    def enterStatement(self, ctx: o9IBPLParser.StatementContext):
        self._stmt_depth += 1
        # Save parent state — every statement at every depth gets its own frame.
        self._stack.append({
            'current':              self._current,
            'dim_attr_seen':        self._dim_attr_seen,
            'measure_seen':         self._measure_seen,
            'named_set_seen':       self._named_set_seen,
            'filter_depth':         self._filter_depth,
            'coalesce_depth':       self._coalesce_depth,
            'members':              self._members,
            'in_exec_proc':         self._in_exec_proc,
            'formula_lhs_measure':  self._formula_lhs_measure,
            'coalesce_args_stack':  self._coalesce_args_stack,
        })
        # Fresh isolated context for this statement.
        if self._members_only:
            self._current = {
                'query':   ctx.getText(),
                'members': [],
            }
        else:
            self._current = {
                'query':             ctx.getText(),
                'query_type':        '',
                'dim_attrs':         [],
                'named_sets':        [],
                'measures':          [],
                'coalesce_measures': [],
                'lead_offsets':      [],
                'filters':           [],
                'object':            None,
                'arguments':         {},
                'formulae':          [],
                '_is_scope':         False,
                'members':           [],
            }
            self._dim_attr_seen  = set()
            self._measure_seen   = set()
            self._named_set_seen = set()
            self._filter_depth   = 0
            self._coalesce_depth = 0
        self._members              = set()
        self._in_exec_proc         = False
        self._formula_lhs_measure  = None
        self._coalesce_args_stack  = []

    def exitStatement(self, ctx: o9IBPLParser.StatementContext):
        # Finalise this statement's result.
        if self._current is not None:
            self._current['members'] = sorted(self._members)

        # If the parent is a scope statement, propagate this child:
        #   (a) as a formula entry in parent's 'formulae'
        #   (b) its measures merged into the parent's measures list
        # Nested scope-within-scope is excluded — only leaf rules (Assignment,
        # Update, etc.) are treated as formulae.
        _is_nested_in_scope = False
        if self._stack and self._current is not None and not self._members_only:
            parent_frame   = self._stack[-1]
            parent_current = parent_frame.get('current')
            _SCOPE_TYPES = frozenset({
                '', None, 'Block Scope', 'Scope', 'Cartesian Scope',
                'Recurrence Scope', 'Insert Scope', 'Ordered Recurrence Scope',
                'Block Scope Graph', 'Graph Edge Property Assignment Scope',
            })
            child_type = self._current.get('query_type')
            if parent_current is not None and parent_current.get('_is_scope'):
                _is_nested_in_scope = True
                if child_type not in _SCOPE_TYPES:
                    # --- formula propagation ---
                    lhs = self._formula_lhs_measure
                    all_measures = self._current.get('measures', [])
                    rhs = [m for m in all_measures if m != lhs]
                    raw_stack = self._coalesce_args_stack
                    if raw_stack:
                        coalesce_tuples = [tuple(args) for args in raw_stack if args]
                    elif self._current.get('coalesce_measures'):
                        coalesce_tuples = [tuple(self._current['coalesce_measures'])]
                    else:
                        coalesce_tuples = []
                    measure_leadoffsets = [
                        f"{lo['base']}.leadoffset({lo['offset']})"
                        for lo in self._current.get('lead_offsets', [])
                        if isinstance(lo.get('applied_to'), dict)
                        and 'measure' in lo['applied_to']
                    ]
                    parent_current['formulae'].append({
                        'rule':                self._current['query'],
                        'lhs_measure':         lhs,
                        'rhs_measures':        rhs,
                        'coalesce_measures':   coalesce_tuples,
                        'measures_leadoffset': measure_leadoffsets,
                    })
                    # --- propagation into parent ---
                    parent_seen = parent_frame['measure_seen']
                    for m in all_measures:
                        if m not in parent_seen:
                            parent_seen.add(m)
                            parent_current['measures'].append(m)
                    for m in self._current.get('coalesce_measures', []):
                        key = f'__coalesce__{m}'
                        if key not in parent_seen:
                            parent_seen.add(key)
                            parent_current['coalesce_measures'].append(m)
                    # lead_offsets are per-rule entries — append all of them;
                    # no deduplication needed as each entry is a unique dict.
                    parent_current['lead_offsets'].extend(
                        self._current.get('lead_offsets', [])
                    )

        # Scope children are fully captured via formulae above; every other
        # statement (top-level or nested inside a non-scope parent) goes into
        # self.results as normal.
        if not _is_nested_in_scope:
            self.results.append(self._current)

        # Restore parent frame.
        if self._stack:
            saved = self._stack.pop()
            self._current               = saved['current']
            self._dim_attr_seen         = saved['dim_attr_seen']
            self._measure_seen          = saved['measure_seen']
            self._named_set_seen        = saved['named_set_seen']
            self._filter_depth          = saved['filter_depth']
            self._coalesce_depth        = saved['coalesce_depth']
            self._members               = saved['members']
            self._in_exec_proc          = saved['in_exec_proc']
            self._formula_lhs_measure   = saved['formula_lhs_measure']
            self._coalesce_args_stack   = saved['coalesce_args_stack']
        else:
            self._current = None
        self._stmt_depth -= 1

    # ------------------------------------------------------------------
    # Query type — SELECT variants
    # ------------------------------------------------------------------

    def enterSelectMemberExprStatement(self, ctx: o9IBPLParser.SelectMemberExprStatementContext):
        """
        Grammar alternatives:
            selectCrossJoinStatement
            | selectCrossJoinStatementWithPostFilter
            | selectMemberStatement
            | selectScenarioScopedMemberStatement
            | SELECT graphNodeMembersStatement
            | SELECT scalar_expression          ← triggers 'object'
        """
        if not self._qi_active():
            return
        self._set_query_type('Select')
        scalar = ctx.scalar_expression()
        if scalar is not None:
            self._current['object'] = {'expression': scalar.getText()}

    def enterSpreadSelectCrossJoinStatement(self, ctx: o9IBPLParser.SpreadSelectCrossJoinStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Spread Select')

    def enterSelectGraphEdgeProjectStatement(self, ctx: o9IBPLParser.SelectGraphEdgeProjectStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Select Graph Edge Project')

    def enterSelectGraphEdgesStatement(self, ctx: o9IBPLParser.SelectGraphEdgesStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Select Graph Edges')

    def enterSelectGraphPathsStatement(self, ctx: o9IBPLParser.SelectGraphPathsStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Select Graph Paths')

    def enterSelectDimensionGraphEdgesStatement(self, ctx: o9IBPLParser.SelectDimensionGraphEdgesStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Select Dimension Graph Edges')

    def enterCountSelectMemberExprStatement(self, ctx: o9IBPLParser.CountSelectMemberExprStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Count Select')

    # ------------------------------------------------------------------
    # Query type — SCOPE variants
    # ------------------------------------------------------------------

    def enterScopeStatement(self, ctx: o9IBPLParser.ScopeStatementContext):
        """Grammar: scopePrefix SCOPE COLON member_measure_crossjoin …"""
        if not self._qi_active():
            return
        prefix = ctx.scopePrefix().getText().strip()
        label = f'{prefix} Scope'.strip() if prefix else 'Scope'
        self._set_query_type(label)
        self._current['_is_scope'] = True

    def enterBlockScopeStatement(self, ctx: o9IBPLParser.BlockScopeStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Block Scope')
        self._current['_is_scope'] = True

    def enterBlockScopeGraphStatement(self, ctx: o9IBPLParser.BlockScopeGraphStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Block Scope Graph')
        self._current['_is_scope'] = True

    def enterRecurrenceScopeStatement(self, ctx: o9IBPLParser.RecurrenceScopeStatementContext):
        """Grammar: (ORDERED)? RECURRENCE SCOPE COLON …"""
        if not self._qi_active():
            return
        prefix = 'Ordered ' if ctx.ORDERED() else ''
        self._set_query_type(f'{prefix}Recurrence Scope')
        self._current['_is_scope'] = True

    def enterInsertScopeStatement(self, ctx: o9IBPLParser.InsertScopeStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Insert Scope')
        self._current['_is_scope'] = True

    def enterScopedGraphEdgePropertyAssignments(self, ctx: o9IBPLParser.ScopedGraphEdgePropertyAssignmentsContext):
        if not self._qi_active():
            return
        self._set_query_type('Graph Edge Property Assignment Scope')
        self._current['_is_scope'] = True

    # ------------------------------------------------------------------
    # Query type — UPDATE / ASSIGNMENT
    # ------------------------------------------------------------------

    def enterUpdateStatement(self, ctx: o9IBPLParser.UpdateStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Update')

    def enterRespreadStatement(self, ctx: o9IBPLParser.RespreadStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Respread')

    def enterAssignment(self, ctx: o9IBPLParser.AssignmentContext):
        """
        Grammar: scalar_expression ASSIGN null_or_scalar_exp
        Update takes precedence — _set_query_type only writes when empty.
        Also collects measure assignment RHS values into members, and records
        the LHS measure name so formulae can distinguish lhs from rhs.
        """
        if not self._active():
            return
        # Query-info — only in full mode.
        if self._qi_active():
            self._set_query_type('Assignment')
        # LHS measure capture — walk the parse tree for the first Measure_nameContext
        # rather than stringifying and regex-searching.
        if self._formula_lhs_measure is None:
            measure_ctx = self._find_first_measure_name(ctx.scalar_expression())
            if measure_ctx is not None:
                self._formula_lhs_measure = self._strip(measure_ctx.identifier(0).getText())
                # Member collection — RHS value (only relevant when LHS is a measure).
                rhs = self._extract_identifier_text(ctx.null_or_scalar_exp())
                if rhs:
                    self._add_member(rhs)

    def enterMassUpdateStatement(self, ctx: o9IBPLParser.MassUpdateStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Mass Update')

    # ------------------------------------------------------------------
    # Query type — CONTROL FLOW
    # ------------------------------------------------------------------

    def enterForeachStatement(self, ctx: o9IBPLParser.ForeachStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('ForEach')

    def enterIfStatement(self, ctx: o9IBPLParser.IfStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('If')

    # ------------------------------------------------------------------
    # Query type — DATA / MEMBER MANAGEMENT
    # ------------------------------------------------------------------

    def enterCreateSetStatement(self, ctx: o9IBPLParser.CreateSetStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Create Set')

    def enterCreateVersionStatement(self, ctx: o9IBPLParser.CreateVersionStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Create Version')

    def enterDeleteVersionStatement(self, ctx: o9IBPLParser.DeleteVersionStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Delete Version')

    def enterCreateScenarioStatement(self, ctx: o9IBPLParser.CreateScenarioStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Create Scenario')

    def enterCreateMemberStatement(self, ctx: o9IBPLParser.CreateMemberStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Create Member')

    def enterUpdateMemberStatement(self, ctx: o9IBPLParser.UpdateMemberStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Update Member')

    def enterDeleteMemberStatement(self, ctx: o9IBPLParser.DeleteMemberStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Delete Member')

    def enterBeginTransactionStatement(self, ctx: o9IBPLParser.BeginTransactionStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Begin Transaction')

    def enterCommitTransactionStatement(self, ctx: o9IBPLParser.CommitTransactionStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Commit Transaction')

    def enterDeleteFactStatement(self, ctx: o9IBPLParser.DeleteFactStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Delete Data')

    def enterUpdateGraphStatement(self, ctx: o9IBPLParser.UpdateGraphStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Update Graph')

    def enterTraverseGraphStatement(self, ctx: o9IBPLParser.TraverseGraphStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Traverse Graph')

    def enterSubGraphStatement(self, ctx: o9IBPLParser.SubGraphStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('SubGraph')

    def enterVertexSetStatement(self, ctx: o9IBPLParser.VertexSetStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Vertex Set')

    def enterExecProcedureStatement(self, ctx: o9IBPLParser.ExecProcedureStatementContext):
        """Grammar: (EXECUTE | EXPAND) PROCEDURE procname=identifier json?"""
        if not self._active():
            return
        # Query-info — only in full mode.
        if self._qi_active():
            self._set_query_type('Execute Procedure')
            proc_name = self._strip(ctx.procname.getText())
            self._current['object'] = {'procedure': proc_name}
            self._current['arguments'].update(self._extract_json_args(ctx.json()))
        # _in_exec_proc must be set in both modes so enterJsonPair fires correctly.
        self._in_exec_proc = True

    def exitExecProcedureStatement(self, ctx: o9IBPLParser.ExecProcedureStatementContext):
        self._in_exec_proc = False

    def enterOnDemandPluginStatement(self, ctx: o9IBPLParser.OnDemandPluginStatementContext):
        """Grammar: EXECUTE PLUGIN INSTANCE instanceName=identifier …"""
        if not self._qi_active():
            return
        self._set_query_type('Execute Plugin')
        plugin_name = self._strip(ctx.instanceName.getText())
        self._current['object'] = {'plugin': plugin_name}

    def enterOperatingScopeStatement(self, ctx: o9IBPLParser.OperatingScopeStatementContext):
        """
        Grammar: FOR MEASURES LBRACE (unqualified_measure_name | measure_name)*
                 RBRACE usingScopeStatement
        Captures the scope crossjoin text and stores it in object['scope'].
        Multiple operatingScopeStatement children are joined with '; '.
        """
        if not self._qi_active():
            return
        if self._find_parent_of_type(ctx, o9IBPLParser.OnDemandPluginStatementContext) is None:
            return
        obj = self._current['object'] or {}
        scope_text = (
            ctx.usingScopeStatement().scopeClause().member_crossjoin().getText()
            if ctx.usingScopeStatement() else ''
        )
        existing = obj.get('scope', '')
        obj['scope'] = f'{existing}; {scope_text}'.lstrip('; ') if existing else scope_text
        self._current['object'] = obj

    def enterGenericNameValue(self, ctx: o9IBPLParser.GenericNameValueContext):
        """
        Grammar: LPAREN identifier COMMA scalar_expression RPAREN
        Only collected when inside an onDemandPluginStatement.
        """
        if not self._qi_active():
            return
        if self._find_parent_of_type(ctx, o9IBPLParser.OnDemandPluginStatementContext) is None:
            return
        key = self._strip(ctx.identifier().getText())
        val = ctx.scalar_expression().getText()
        self._current['arguments'][key] = val

    def enterServiceCommandStatement(self, ctx: o9IBPLParser.ServiceCommandStatementContext):
        """Grammar: EXECSERVICECOMMAND identifier (ARGUMENTS json)?"""
        if not self._qi_active():
            return
        self._set_query_type('Service Command')
        cmd_name = self._strip(ctx.identifier().getText())
        self._current['object'] = {'service_command': cmd_name}
        self._current['arguments'].update(self._extract_json_args(ctx.json()))

    def enterSaveStatement(self, ctx: o9IBPLParser.SaveStatementContext):
        """Grammar: SAVE LPAREN identifier? RPAREN … (ARGUMENTS json)?"""
        if not self._qi_active():
            return
        self._set_query_type('Save')
        path_id = ctx.identifier()
        if path_id is not None:
            self._current['object'] = {'path': self._strip(path_id.getText())}
        self._current['arguments'].update(self._extract_json_args(ctx.json()))

    def enterEnableDisablePlanStatement(self, ctx: o9IBPLParser.EnableDisablePlanStatementContext):
        """Grammar: (ENABLE | DISABLE) PLAN"""
        if not self._qi_active():
            return
        label = 'Enable Plan' if ctx.ENABLE() is not None else 'Disable Plan'
        self._set_query_type(label)

    def enterDownloadDatafileStatement(self, ctx: o9IBPLParser.DownloadDatafileStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Download Data File')
        self._current['arguments'].update(self._extract_command_option_args(ctx))

    def enterUploadDatafileStatement(self, ctx: o9IBPLParser.UploadDatafileStatementContext):
        if not self._qi_active():
            return
        self._set_query_type('Upload Data File')
        self._current['arguments'].update(self._extract_command_option_args(ctx))

    # ------------------------------------------------------------------
    # Dimension attributes
    # ------------------------------------------------------------------

    def enterLevelattribute_name(self, ctx: o9IBPLParser.Levelattribute_nameContext):
        if not self._qi_active():
            return
        if ctx.dimension_name() is None:
            return
        dim  = self._strip(ctx.dimension_name().getText())
        attr = self._strip(ctx.identifier().getText())
        self._add_dim_attr(dim, attr)

    # ------------------------------------------------------------------
    # Named sets
    # ------------------------------------------------------------------

    def enterMemberSetReference(self, ctx: o9IBPLParser.MemberSetReferenceContext):
        """Grammar: (graph_identifier DOT (from_tail|to_head) DOT)? RESOLVABLES"""
        if not self._qi_active():
            return
        token = ctx.RESOLVABLES()
        if token:
            self._add_named_set(token.getText().lstrip('&'))

    def enterNamedNodeReference(self, ctx: o9IBPLParser.NamedNodeReferenceContext):
        """Grammar: NAMEDNODE multifilter_clause?"""
        if not self._qi_active():
            return
        token = ctx.NAMEDNODE()
        if token:
            self._add_named_set(token.getText().lstrip('$'))

    def enterNamedNodeFilterSetReference(self, ctx: o9IBPLParser.NamedNodeFilterSetReferenceContext):
        """Grammar: NAMEDNODEFILTERSET multifilter_clause?"""
        if not self._qi_active():
            return
        token = ctx.NAMEDNODEFILTERSET()
        if token:
            self._add_named_set(token.getText().lstrip('%'))

    def enterNamedNodeGraphReference(self, ctx: o9IBPLParser.NamedNodeGraphReferenceContext):
        """Grammar: (graph_identifier DOT)? (from_tail|to_head) DOT NAMEDNODE …"""
        if not self._qi_active():
            return
        token = ctx.NAMEDNODE()
        if token:
            self._add_named_set(token.getText().lstrip('$'))

    def enterNamedNodeFilterSetGraphReference(self, ctx: o9IBPLParser.NamedNodeFilterSetGraphReferenceContext):
        """Grammar: (graph_identifier DOT)? (from_tail|to_head) DOT NAMEDNODEFILTERSET …"""
        if not self._qi_active():
            return
        token = ctx.NAMEDNODEFILTERSET()
        if token:
            self._add_named_set(token.getText().lstrip('%'))

    # ------------------------------------------------------------------
    # Measures
    # ------------------------------------------------------------------

    def enterMeasure_name(self, ctx: o9IBPLParser.Measure_nameContext):
        """
        Grammar: MEASURE DOT identifier | MEASURE DOT identifier DOT identifier
        Routes through _add_coalesce_measure when inside a coalesce call.
        """
        if not self._qi_active():
            return
        name = self._strip(ctx.identifier(0).getText())
        if self._coalesce_depth > 0:
            self._add_coalesce_measure(name)
        else:
            self._add_measure(name)

    def enterTransient_measure_name(self, ctx: o9IBPLParser.Transient_measure_nameContext):
        """Grammar: TRANSIENT DOT identifier"""
        if not self._qi_active():
            return
        name = self._strip(ctx.identifier().getText())
        if self._coalesce_depth > 0:
            self._add_coalesce_measure(name)
        else:
            self._add_measure(name)

    def enterFully_qualified_edge_property(self, ctx: o9IBPLParser.Fully_qualified_edge_propertyContext):
        """Grammar: EDGE DOT graphName DOT edgePropertyName"""
        if not self._qi_active():
            return
        self._add_measure(self._strip(ctx.edgePropertyName().getText()))

    def enterEdge_property(self, ctx: o9IBPLParser.Edge_propertyContext):
        """Grammar: EDGE DOT edgePropertyName"""
        if not self._qi_active():
            return
        self._add_measure(self._strip(ctx.edgePropertyName().getText()))

    def enterLiteralCoalesce(self, ctx: o9IBPLParser.LiteralCoalesceContext):
        """Grammar (#LiteralCoalesce): COALESCE LPAREN scalar_expression* RPAREN"""
        if not self._qi_active():
            return
        self._coalesce_depth += 1
        # Push a fresh arg-list for this coalesce call so we can later produce
        # one tuple per call in the formula's coalesce_measures list.
        self._coalesce_args_stack.append([])

    def exitLiteralCoalesce(self, ctx: o9IBPLParser.LiteralCoalesceContext):
        if self._coalesce_depth > 0:
            self._coalesce_depth -= 1
        # The args collected for this call stay on the stack; exitStatement
        # will harvest them all into the formula's coalesce_measures list.

    def enterMeasure_with_scope_or_graph_coordinates(self, ctx: o9IBPLParser.Measure_with_scope_or_graph_coordinatesContext):
        """Grammar: (MEASURE DOT)? identifier AT (…)"""
        if not self._qi_active():
            return
        ids = ctx.identifier()
        if ids:
            self._add_measure(self._strip(ids[0].getText()))

    def enterMemberLeadOffset(self, ctx: o9IBPLParser.MemberLeadOffsetContext):
        """
        Grammar (#MemberLeadOffset):
            member_expression DOT LEADOFFSET LPAREN scalar_expression RPAREN

        applied_to cases:
          Measure.[Inventory]@(Time.#.LeadOffset(-1))
            → {'measure': 'Inventory'}
          Time.[Day].[22].leadoffset(-12)
            → {'dim_attr': 'Time.[Day]', 'member': '22'}
          &CurrentDay.element(0).LeadOffset(-10)
            → {'named_set': 'CurrentDay'}
        """
        if not self._qi_active():
            return
        base_ctx = ctx.member_expression()
        base     = base_ctx.getText()
        offset   = ctx.scalar_expression().getText()
        applied_to = None

        msc = self._find_parent_of_type(
            ctx, o9IBPLParser.Measure_with_scope_or_graph_coordinatesContext
        )
        if msc is not None:
            ids = msc.identifier()
            if ids:
                applied_to = {'measure': self._strip(ids[0].getText())}

        if applied_to is None and isinstance(base_ctx, o9IBPLParser.MemberLevelAttributeContext):
            applied_to = {
                'dim_attr': base_ctx.member_expression().getText(),
                'member':   self._strip(base_ctx.identifier().getText()),
            }

        if applied_to is None:
            root_text = base.lstrip('(')
            if root_text.startswith('&'):
                applied_to = {'named_set': root_text.lstrip('&').split('.')[0]}
            elif root_text.startswith('$$') or root_text.startswith('%%'):
                applied_to = {'named_set': root_text.lstrip('$%').split('.')[0]}

        entry = {'base': base, 'offset': offset}
        if applied_to:
            entry['applied_to'] = applied_to
        self._current['lead_offsets'].append(entry)

    # ------------------------------------------------------------------
    # Member collection
    # ------------------------------------------------------------------

    def enterMemberFind(self, ctx: o9IBPLParser.MemberFindContext):
        """Grammar (#MemberFind): member_expression DOT FIND LPAREN … RPAREN"""
        if not self._active():
            return
        dim = self._extract_dimension(ctx.member_expression().getText())
        if self._is_excluded_dimension(dim):
            return
        ident = self._extract_identifier_text(ctx)
        if ident:
            self._add_member(ident)

    def enterMemberAttributeAssignment(self, ctx: o9IBPLParser.MemberAttributeAssignmentContext):
        """CREATEMEMBER / UPDATEMEMBER / DELETEMEMBER attribute assignments."""
        if not self._active():
            return
        dim = self._extract_dimension(ctx.levelattribute_name().getText())
        if self._is_excluded_dimension(dim):
            return
        if ctx.valueExpr() is not None:
            self._add_member(ctx.valueExpr().getText())
        if ctx.identifier() is not None:
            self._add_member(ctx.identifier().getText())

    def enterRelExprString(self, ctx: o9IBPLParser.RelExprStringContext):
        """LIKE / CONTAINS / STARTSWITH / ENDSWITH comparisons."""
        if not self._active():
            return
        if len(ctx.addExpr()) < 2:
            return
        lhs_clean = ctx.addExpr(0).getText().strip().lower()
        rhs = self._extract_identifier_text(ctx.addExpr(1))
        if not rhs:
            return
        dim_clean = (self._get_dimension_from_member_filter(ctx) or '').strip().lower()
        if self._should_collect(lhs_clean, dim_clean) or self._is_measure_or_transient(lhs_clean):
            self._add_member(rhs)

    def enterRelExprNumeric(self, ctx: o9IBPLParser.RelExprNumericContext):
        """<, <=, >, >= comparisons."""
        if not self._active():
            return
        if len(ctx.relStrExpr()) < 2:
            return
        lhs_clean = ctx.relStrExpr(0).getText().strip().lower()
        rhs = self._extract_identifier_text(ctx.relStrExpr(1))
        if not rhs:
            return
        dim_clean = (self._get_dimension_from_member_filter(ctx) or '').strip().lower()
        if self._should_collect(lhs_clean, dim_clean) or self._is_measure_or_transient(lhs_clean):
            self._add_member(rhs)

    def enterEquExpr(self, ctx: o9IBPLParser.EquExprContext):
        """== comparisons."""
        if not self._active():
            return
        if len(ctx.notEquExpr()) < 2:
            return
        lhs_clean = ctx.notEquExpr(0).getText().strip().lower()
        rhs = self._extract_identifier_text(ctx.notEquExpr(1))
        if not rhs:
            return
        dim_clean = (self._get_dimension_from_member_filter(ctx) or '').strip().lower()
        if self._should_collect(lhs_clean, dim_clean) or self._is_measure_or_transient(lhs_clean):
            self._add_member(rhs)

    def enterNotEquExpr(self, ctx: o9IBPLParser.NotEquExprContext):
        """<> / != comparisons."""
        if not self._active():
            return
        if len(ctx.inScalarSetExpr()) < 2:
            return
        lhs_clean = ctx.inScalarSetExpr(0).getText().strip().lower()
        rhs = self._extract_identifier_text(ctx.inScalarSetExpr(1))
        if not rhs:
            return
        dim_clean = (self._get_dimension_from_member_filter(ctx) or '').strip().lower()
        if self._should_collect(lhs_clean, dim_clean):
            self._add_member(rhs)

    def enterInScalarSetExpr(self, ctx: o9IBPLParser.InScalarSetExprContext):
        """expr IN {val1, val2, …}"""
        if not self._active():
            return
        if not ctx.IN():
            return
        lhs_clean = ctx.relExpr().getText().strip().lower()
        rhs_list_ctx = ctx.scalar_exprList()
        if not rhs_list_ctx:
            return
        dim_clean = (self._get_dimension_from_member_filter(ctx) or '').strip().lower()
        if self._should_collect(lhs_clean, dim_clean) or self._is_measure_or_transient(lhs_clean):
            for s_expr in rhs_list_ctx.scalar_expression():
                value = self._extract_identifier_text(s_expr)
                if value:
                    self._add_member(value)

    def enterJsonPair(self, ctx: o9IBPLParser.JsonPairContext):
        """Extract string values from JSON pairs inside exec procedure calls."""
        if not self._in_exec_proc:
            return
        value_ctx = ctx.jsonValue()
        if value_ctx.jsonObject() is not None:
            return
        key = ctx.jsonstring().STRING().getText().strip('"').strip().lower()
        if key in _EXCLUDED_DIMENSIONS:
            return
        if value_ctx.jsonArray() is not None:
            arr = value_ctx.jsonArray()
            if arr.QUOTEDID() is not None:
                self._add_member(arr.QUOTEDID().getText())
            else:
                for val in arr.jsonValue():
                    if val.jsonstring() is not None:
                        self._add_member(val.jsonstring().STRING().getText())
        elif value_ctx.jsonstring() is not None:
            self._add_member(value_ctx.jsonstring().STRING().getText())

    # ------------------------------------------------------------------
    # Filters — depth management
    # ------------------------------------------------------------------

    def enterMember_measure_filter_set(self, ctx: o9IBPLParser.Member_measure_filter_setContext):
        if self._qi_active():
            self._filter_depth += 1

    def exitMember_measure_filter_set(self, ctx: o9IBPLParser.Member_measure_filter_setContext):
        if self._qi_active():
            self._filter_depth -= 1

    def enterMember_filter_set(self, ctx: o9IBPLParser.Member_filter_setContext):
        if self._qi_active():
            self._filter_depth += 1

    def exitMember_filter_set(self, ctx: o9IBPLParser.Member_filter_setContext):
        if self._qi_active():
            self._filter_depth -= 1

    def enterGraph_filter_set(self, ctx: o9IBPLParser.Graph_filter_setContext):
        if self._qi_active():
            self._filter_depth += 1

    def exitGraph_filter_set(self, ctx: o9IBPLParser.Graph_filter_setContext):
        if self._qi_active():
            self._filter_depth -= 1

    def enterGraph_path_filter_set(self, ctx: o9IBPLParser.Graph_path_filter_setContext):
        if self._qi_active():
            self._filter_depth += 1

    def exitGraph_path_filter_set(self, ctx: o9IBPLParser.Graph_path_filter_setContext):
        if self._qi_active():
            self._filter_depth -= 1

    # ------------------------------------------------------------------
    # Filters — WHERE clause element handlers
    # ------------------------------------------------------------------

    def enterMember_measure_filter(self, ctx: o9IBPLParser.Member_measure_filterContext):
        """
        Grammar alternatives:
            member_expression | graph_identifier | graphNodeMembersStatement
            | ASSOCIATION? scalar_expression | measureZeroClause
        MemberFilter and MemberLevelAttribute are skipped — handled by their
        own dedicated listeners to avoid duplicate entries.
        """
        if not self._in_filter_ctx():
            return
        mem    = ctx.member_expression()
        scalar = ctx.scalar_expression()
        graph  = ctx.graph_identifier()
        if mem is not None:
            if isinstance(mem, (o9IBPLParser.MemberFilterContext,
                                o9IBPLParser.MemberLevelAttributeContext)):
                return
            self._set_filter(self._base_subject(mem), mem.getText())
        elif scalar is not None:
            self._set_filter(self._scalar_subject(scalar), scalar.getText())
        elif graph is not None:
            self._set_filter(None, graph.getText())

    def enterMember_filter(self, ctx: o9IBPLParser.Member_filterContext):
        """Grammar alternatives (SPREAD SELECT WHERE): member_expression | graph_identifier …"""
        if not self._in_filter_ctx():
            return
        mem   = ctx.member_expression()
        graph = ctx.graph_identifier()
        if mem is not None:
            if isinstance(mem, (o9IBPLParser.MemberFilterContext,
                                o9IBPLParser.MemberLevelAttributeContext)):
                return
            self._set_filter(self._base_subject(mem), mem.getText())
        elif graph is not None:
            self._set_filter(None, graph.getText())

    def enterMemberLevelAttribute(self, ctx: o9IBPLParser.MemberLevelAttributeContext):
        """
        Grammar (#MemberLevelAttribute): member_expression DOT identifier

        Member collection fires unconditionally (before the filter-chain guard)
        so that members inside chains like Item.[Item Type].[FG].filter(…)
        are not dropped.

        Filter emission fires only outside MemberFilter chains — inside chains
        _base_subject(emit=True) in enterMemberFilter already handles it.
        In members_only mode filter emission is skipped entirely.
        """
        if not self._active():
            return
        # Member collection — always, regardless of mode or filter chain context.
        dim = self._extract_dimension(ctx.member_expression().getText())
        if not self._is_excluded_dimension(dim):
            ident = self._extract_identifier_text(ctx)
            if ident:
                self._add_member(ident)
        # Filter emission — query-info mode only, and not inside filter chains.
        if not self._qi_active():
            return
        if self._find_parent_of_type(ctx, o9IBPLParser.MemberFilterContext) is not None:
            return
        subject    = ctx.member_expression().getText()
        expression = self._strip(ctx.identifier().getText())
        self._set_filter(subject, expression)

    def enterMemberFilter(self, ctx: o9IBPLParser.MemberFilterContext):
        """
        Grammar (#MemberFilter):
            member_expression DOT FILTER LPAREN scalar_expression RPAREN
        _base_subject(emit=True) emits a filter entry for every
        MemberLevelAttribute stripped along the chain.
        """
        if not self._qi_active():
            return
        subject    = self._base_subject(ctx.member_expression(), emit=True)
        expression = ctx.scalar_expression().getText()
        self._set_filter(subject, expression)

    def enterSelectCrossJoinStatementWithPostFilter(self, ctx: o9IBPLParser.SelectCrossJoinStatementWithPostFilterContext):
        """Grammar: (…selectCrossJoinStatement…) DOT FILTER LPAREN scalar_expression RPAREN"""
        if not self._qi_active():
            return
        self._set_filter('Post Filter', ctx.scalar_expression().getText())

    def enterSelectCrossJoinStatement(self, ctx: o9IBPLParser.SelectCrossJoinStatementContext):
        """Captures include_subtotals and include_nulls query options."""
        if not self._qi_active():
            return
        obj = self._current['object'] or {}
        qol = ctx.query_option_list()
        if qol is not None:
            for qo in (qol.query_option() or []):
                if qo.include_subtotals() is not None:
                    issq = ctx.include_subtotals_sub_query()
                    obj['include_subtotals'] = (
                        issq.getText() if issq is not None else True
                    )
                if qo.include_nulls() is not None:
                    obj['include_nulls'] = True
        if obj:
            self._current['object'] = obj

    def enterAdornmentInfo(self, ctx: o9IBPLParser.AdornmentInfoContext):
        """Captures member_properties and use_aliases from SELECT adornment."""
        if not self._qi_active():
            return
        obj = self._current['object'] or {}
        for prop in (ctx.include_properties() or []):
            imp = prop.include_member_properties()
            if imp is None:
                continue
            for ap in (imp.attribute_properties() or []):
                la  = ap.levelattribute()
                ids = ap.identifier() or []
                obj.setdefault('member_properties', []).append({
                    'attribute':  la.getText() if la else '',
                    'properties': [i.getText() for i in ids],
                })
        ua = ctx.use_aliases()
        if ua is not None:
            aliases = {}
            for a in (ua.alias() or []):
                daa = a.dimension_attribute_alias()
                if daa is None:
                    continue
                dim_ctx = daa.dimension()      if hasattr(daa, 'dimension')      else None
                lat_ctx = daa.levelattribute() if hasattr(daa, 'levelattribute') else None
                key_ctx  = dim_ctx or lat_ctx
                key_text = key_ctx.getText() if key_ctx else ''
                aliases[key_text] = self._strip(daa.identifier().getText())
            if aliases:
                obj['use_aliases'] = aliases
        if obj:
            self._current['object'] = obj

    def enterRel_edgePredicate_expression(self, ctx: o9IBPLParser.Rel_edgePredicate_expressionContext):
        """Grammar: LPAREN graph_identifier COMMA edgePredicate_expression RPAREN"""
        if not self._qi_active():
            return
        self._set_filter(
            ctx.graph_identifier().getText(),
            ctx.edgePredicate_expression().getText(),
        )

    def enterDimgraph_where_clause(self, ctx: o9IBPLParser.Dimgraph_where_clauseContext):
        """Grammar: WHERE LBRACE edgePredicate_expression RBRACE (PARENTCHILD select)"""
        if not self._qi_active():
            return
        parent = self._find_parent_of_type(
            ctx, o9IBPLParser.SelectDimensionGraphEdgesStatementContext
        )
        subject = parent.dimension_name().getText() if parent is not None else 'parentchild'
        self._set_filter(subject, ctx.edgePredicate_expression().getText())

    def enterEdgeProjectPredicate_expression(self, ctx: o9IBPLParser.EdgeProjectPredicate_expressionContext):
        """Grammar: WHERE LBRACE edgeProjectPredicate_expression RBRACE"""
        if not self._qi_active():
            return
        scalar  = ctx.scalar_expression()
        subject = self._scalar_subject(scalar) if scalar is not None else None
        self._set_filter(subject, ctx.getText())

    def enterMeasureFilterStatement(self, ctx: o9IBPLParser.MeasureFilterStatementContext):
        """Grammar: FILTERBY LBRACE scalar_expression RBRACE (cellAccessStatement)"""
        if not self._qi_active():
            return
        cell_parent = self._find_parent_of_type(
            ctx, o9IBPLParser.CellAccessStatementContext
        )
        if cell_parent is not None:
            if cell_parent.plan_name() is not None:
                subject = self._strip(cell_parent.plan_name().getText())
            elif cell_parent.measure_group_name() is not None:
                subject = self._strip(cell_parent.measure_group_name().getText())
            elif cell_parent.unqualified_measure_name() is not None:
                identifiers = cell_parent.unqualified_measure_name().identifier()
                subject = self._strip(identifiers[-1].getText())
            else:
                subject = 'filterby'
        else:
            subject = 'filterby'
        self._set_filter(subject, ctx.scalar_expression().getText())

    def enterAttributeAccessStatement(self, ctx: o9IBPLParser.AttributeAccessStatementContext):
        """Grammar: LEVELATTRIBUTE levelattribute_name … FILTERBY LBRACE measure_name RBRACE"""
        if not self._qi_active():
            return
        self._set_filter(ctx.levelattribute_name().getText(), ctx.measure_name().getText())

    def enterCopyMeasureStatement(self, ctx: o9IBPLParser.CopyMeasureStatementContext):
        """Grammar: COPYMEASURE (…) (WHERE member_expression)"""
        if not self._qi_active():
            return
        mem = ctx.member_expression()
        if mem is None:
            return
        self._set_filter('copymeasure', mem.getText())

    def enterSelectScenarioScopedMemberStatement(self, ctx: o9IBPLParser.SelectScenarioScopedMemberStatementContext):
        """Grammar: SELECT member_expression … WHERE LBRACE member_expression RBRACE"""
        if not self._qi_active():
            return
        exprs = ctx.member_expression()
        if len(exprs) >= 2:
            self._set_filter(exprs[0].getText(), exprs[1].getText())

    def enterSyncExternalModelsStatement(self, ctx: o9IBPLParser.SyncExternalModelsStatementContext):
        if not self._qi_active():
            return
        mem = ctx.member_expression()
        if mem is not None:
            self._set_filter('sync_external', mem.getText())

    def enterSyncLocalModelsStatement(self, ctx: o9IBPLParser.SyncLocalModelsStatementContext):
        if not self._qi_active():
            return
        mem = ctx.member_expression()
        if mem is not None:
            self._set_filter('sync_local', mem.getText())

    def enterRefreshMaterializedViewsStatement(self, ctx: o9IBPLParser.RefreshMaterializedViewsStatementContext):
        if not self._qi_active():
            return
        mem = ctx.member_expression()
        if mem is not None:
            self._set_filter('refresh_views', mem.getText())

    def enterReleaseTableMemoryStatement(self, ctx: o9IBPLParser.ReleaseTableMemoryStatementContext):
        if not self._qi_active():
            return
        mem = ctx.member_expression()
        if mem is not None:
            self._set_filter('release_memory', mem.getText())

    def enterNamedNode_Filter_clause(self, ctx: o9IBPLParser.NamedNode_Filter_clauseContext):
        """Grammar: identifier COLON scalar_expression (inside multifilter_clause)"""
        if not self._qi_active():
            return
        filter_key = self._strip(ctx.identifier().getText())
        expression = ctx.scalar_expression().getText()
        named_node_types = (
            o9IBPLParser.NamedNodeReferenceContext,
            o9IBPLParser.NamedNodeFilterSetReferenceContext,
            o9IBPLParser.NamedNodeGraphReferenceContext,
            o9IBPLParser.NamedNodeFilterSetGraphReferenceContext,
        )
        parent = self._find_parent_of_type(ctx, named_node_types)
        if parent is not None:
            token = (parent.NAMEDNODE() or parent.NAMEDNODEFILTERSET()
                     if hasattr(parent, 'NAMEDNODE') else None)
            set_name = token.getText().lstrip('$%') if token else parent.getText()
        else:
            set_name = 'named_set'
        self._set_filter(f'{set_name}.{filter_key}', expression)

    def enterGraphEdgePropertyUpdate_member(self, ctx: o9IBPLParser.GraphEdgePropertyUpdate_memberContext):
        """Grammar: (from_tail | to_head) DOT member_expression | graphVersions_expression"""
        if not self._qi_active():
            return
        if self._find_parent_of_type(ctx, o9IBPLParser.SyncLocalModelsStatementContext) is None:
            return
        mem = ctx.member_expression()
        ver = ctx.graphVersions_expression()
        if mem is not None:
            direction = ctx.from_tail() or ctx.to_head()
            self._set_filter(direction.getText() if direction else 'sync_local_node', mem.getText())
        elif ver is not None:
            self._set_filter('version', ver.getText())

    def enterDeleteEdgesFilterClause(self, ctx: o9IBPLParser.DeleteEdgesFilterClauseContext):
        """Grammar: WHERE LBRACE graphVersions_expression (COMMA rel_deleteEdgesFilter…)* RBRACE"""
        if not self._qi_active():
            return
        ver = ctx.graphVersions_expression()
        if ver is not None:
            self._set_filter('version', ver.getText())

    def enterRel_deleteEdgesFilter_expression(self, ctx: o9IBPLParser.Rel_deleteEdgesFilter_expressionContext):
        """Grammar: LPAREN graphNameOrIdentfier (COMMA member_expression)* … RPAREN"""
        if not self._qi_active():
            return
        subject = ctx.graphNameOrIdentfier().getText()
        parts   = (
            [m.getText() for m in ctx.member_expression()]
            + [e.getText() for e in ctx.edgePredicate_expression()]
        )
        self._set_filter(subject, ', '.join(parts) if parts else subject)

    def enterMember_crossjoin(self, ctx: o9IBPLParser.Member_crossjoinContext):
        """
        Grammar alternative 1 (filter):
            member_crossjoin DOT FILTER LPAREN exprBool=scalar_expression RPAREN
        exprBool is None on the other two alternatives.
        """
        if not self._qi_active():
            return
        expr_bool = getattr(ctx, 'exprBool', None)
        if expr_bool is None:
            return
        self._set_filter(ctx.member_crossjoin().getText(), expr_bool.getText())