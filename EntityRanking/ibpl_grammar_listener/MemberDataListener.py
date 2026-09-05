from .o9IBPLListener import o9IBPLListener
from .o9IBPLParser import o9IBPLParser


# Dimension names that should never contribute collected members
_EXCLUDED_DIMENSIONS = frozenset({'version', 'time'})


class MemberCollectorListener(o9IBPLListener):
    """Collects member/fact values by walking the o9IBPL parse tree."""

    def __init__(self):
        self.members: set = set()
        self.in_exec_proc: bool = False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _extract_dimension(self, text: str) -> str:
        """Return the leading dimension name from a dotted expression,
        stripping any surrounding square brackets."""
        part = text.split('.')[0] if '.' in text else text
        return part.replace('[', '').replace(']', '').strip()

    def _is_excluded_dimension(self, dim: str) -> bool:
        """Return True if the dimension should be skipped during collection."""
        return dim.strip().lower() in _EXCLUDED_DIMENSIONS

    def _should_collect(self, lhs_clean: str, dim_clean: str) -> bool:
        """Return True when the LHS/dimension combination warrants member collection.

        Excludes:
        - current-member hash references  (#.key)
        - time-prefixed LHS expressions
        - excluded dimensions (time, version)
        """
        if "#.key" in lhs_clean or lhs_clean.startswith("time"):
            return False
        return dim_clean not in _EXCLUDED_DIMENSIONS

    def _is_measure_or_transient(self, lhs_clean: str) -> bool:
        """Return True when the LHS refers to a measure or transient measure."""
        return "measure" in lhs_clean or "transient" in lhs_clean

    def extract_identifier_text(self, expr_ctx) -> str | None:
        """Extract a member/fact identifier string from an expression context.

        Checks children for .identifier(), .QUOTEDID(), or .STRING() accessors
        in that order, then falls back to inspecting the raw text for quoted
        or bracket-wrapped values.
        """
        for child in expr_ctx.getChildren():
            if callable(getattr(child, "identifier", None)):
                id_node = child.identifier()
                if id_node:
                    return id_node.getText()
            elif callable(getattr(child, "QUOTEDID", None)):
                id_node = child.QUOTEDID()
                if id_node:
                    return id_node.getText()
            elif callable(getattr(child, "STRING", None)):
                id_node = child.STRING()
                if id_node:
                    return id_node.getText()

        # Fallback: raw text is itself a quoted or bracketed literal
        text = expr_ctx.getText()
        if (text.startswith('"') and text.endswith('"')) or \
           (text.startswith('[') and text.endswith(']')):
            return text
        return None

    def find_parent_of_type(self, ctx, target_type):
        """Walk up the parse tree and return the first ancestor of target_type,
        or None if no such ancestor exists."""
        parent = ctx.parentCtx
        while parent is not None:
            if isinstance(parent, target_type):
                return parent
            parent = parent.parentCtx
        return None

    def get_dimension_name_from_member_filter(self, ctx) -> str | None:
        """Walk up to the nearest MemberFilter context and return its dimension name."""
        filter_ctx = self.find_parent_of_type(ctx, o9IBPLParser.MemberFilterContext)
        if not filter_ctx:
            return None

        member_expr = filter_ctx.member_expression()
        if not member_expr:
            return None

        return self._extract_dimension(member_expr.getText())

    # ------------------------------------------------------------------
    # Exec-procedure JSON flag
    # ------------------------------------------------------------------

    def enterExecProcedureStatement(self, ctx: o9IBPLParser.ExecProcedureStatementContext):
        """Enable JSON pair extraction only while inside an exec procedure."""
        self.in_exec_proc = True

    def exitExecProcedureStatement(self, ctx: o9IBPLParser.ExecProcedureStatementContext):
        self.in_exec_proc = False

    # ------------------------------------------------------------------
    # Member expression listeners
    # ------------------------------------------------------------------

    def enterMemberFind(self, ctx: o9IBPLParser.MemberFindContext):
        """dimension.attribute.find(member) / dimension.find(member)"""
        dim = self._extract_dimension(ctx.member_expression().getText())
        if self._is_excluded_dimension(dim):
            return
        ident = self.extract_identifier_text(ctx)
        if ident:
            self.members.add(ident)

    def enterMemberLevelAttribute(self, ctx: o9IBPLParser.MemberLevelAttributeContext):
        """dimension.attribute.member"""
        dim = self._extract_dimension(ctx.member_expression().getText())
        if self._is_excluded_dimension(dim):
            return
        ident = self.extract_identifier_text(ctx)
        if ident:
            self.members.add(ident)

    # ------------------------------------------------------------------
    # Scalar comparison expression listeners
    # ------------------------------------------------------------------

    def enterRelExprString(self, ctx: o9IBPLParser.RelExprStringContext):
        """LIKE / CONTAINS / STARTSWITH / ENDSWITH comparisons."""
        if len(ctx.addExpr()) < 2:
            return
        lhs_clean = ctx.addExpr(0).getText().strip().lower()
        rhs = self.extract_identifier_text(ctx.addExpr(1))
        if not rhs:
            return
        dim_clean = (self.get_dimension_name_from_member_filter(ctx) or "").strip().lower()
        if self._should_collect(lhs_clean, dim_clean) or self._is_measure_or_transient(lhs_clean):
            self.members.add(rhs)

    def enterRelExprNumeric(self, ctx: o9IBPLParser.RelExprNumericContext):
        """<, <=, >, >= comparisons."""
        if len(ctx.relStrExpr()) < 2:
            return
        lhs_clean = ctx.relStrExpr(0).getText().strip().lower()
        rhs = self.extract_identifier_text(ctx.relStrExpr(1))
        if not rhs:
            return
        dim_clean = (self.get_dimension_name_from_member_filter(ctx) or "").strip().lower()
        if self._should_collect(lhs_clean, dim_clean) or self._is_measure_or_transient(lhs_clean):
            self.members.add(rhs)

    def enterEquExpr(self, ctx: o9IBPLParser.EquExprContext):
        """== comparisons."""
        if len(ctx.notEquExpr()) < 2:
            return
        lhs_clean = ctx.notEquExpr(0).getText().strip().lower()
        rhs = self.extract_identifier_text(ctx.notEquExpr(1))
        if not rhs:
            return
        dim_clean = (self.get_dimension_name_from_member_filter(ctx) or "").strip().lower()
        if self._should_collect(lhs_clean, dim_clean) or self._is_measure_or_transient(lhs_clean):
            self.members.add(rhs)

    def enterNotEquExpr(self, ctx: o9IBPLParser.NotEquExprContext):
        """<> / != comparisons."""
        if len(ctx.inScalarSetExpr()) < 2:
            return
        lhs_clean = ctx.inScalarSetExpr(0).getText().strip().lower()
        # FIX: use extract_identifier_text instead of raw getText()
        rhs = self.extract_identifier_text(ctx.inScalarSetExpr(1))
        if not rhs:
            return
        dim_clean = (self.get_dimension_name_from_member_filter(ctx) or "").strip().lower()
        if self._should_collect(lhs_clean, dim_clean):
            self.members.add(rhs)

    def enterInScalarSetExpr(self, ctx: o9IBPLParser.InScalarSetExprContext):
        """expr IN {val1, val2, ...} — member sets and measure value sets."""
        if not ctx.IN():
            return
        lhs_clean = ctx.relExpr().getText().strip().lower()
        rhs_list_ctx = ctx.scalar_exprList()
        if not rhs_list_ctx:
            return
        dim_clean = (self.get_dimension_name_from_member_filter(ctx) or "").strip().lower()
        if self._should_collect(lhs_clean, dim_clean) or self._is_measure_or_transient(lhs_clean):
            for s_expr in rhs_list_ctx.scalar_expression():
                value = self.extract_identifier_text(s_expr)
                if value:
                    self.members.add(value)

    def enterAssignment(self, ctx: o9IBPLParser.AssignmentContext):
        """measure.name = <value> assignments."""
        lhs_clean = ctx.scalar_expression().getText().strip().lower()
        if "measure" not in lhs_clean:
            return
        rhs = self.extract_identifier_text(ctx.null_or_scalar_exp())
        if rhs:
            self.members.add(rhs)

    # ------------------------------------------------------------------
    # Member CRUD listeners
    # ------------------------------------------------------------------

    def enterMemberAttributeAssignment(self, ctx: o9IBPLParser.MemberAttributeAssignmentContext):
        """CREATEMEMBER / UPDATEMEMBER / DELETEMEMBER attribute assignments."""
        dim = self._extract_dimension(ctx.levelattribute_name().getText())
        if self._is_excluded_dimension(dim):
            return
        # FIX: ANTLR context methods always exist — guard with None check only
        if ctx.valueExpr() is not None:
            self.members.add(ctx.valueExpr().getText())
        if ctx.identifier() is not None:
            self.members.add(ctx.identifier().getText())

    # ------------------------------------------------------------------
    # JSON pair listener (exec procedure only)
    # ------------------------------------------------------------------

    def enterJsonPair(self, ctx: o9IBPLParser.JsonPairContext):
        """Extract string values from JSON pairs inside exec procedure calls.
        Booleans and numbers are intentionally ignored."""
        if not self.in_exec_proc:
            return

        value_ctx = ctx.jsonValue()

        # Skip nested objects — they will re-enter this listener recursively
        if value_ctx.jsonObject() is not None:
            return

        # FIX: strip quotes before whitespace so "  time  " normalises correctly
        key = ctx.jsonstring().STRING().getText().strip('"').strip().lower()
        if key in _EXCLUDED_DIMENSIONS:
            return

        if value_ctx.jsonArray() is not None:
            # Array value: may be a single QUOTEDID or a list of jsonstring values
            arr = value_ctx.jsonArray()
            if arr.QUOTEDID() is not None:
                self.members.add(arr.QUOTEDID().getText())
            else:
                for val in arr.jsonValue():
                    if val.jsonstring() is not None:
                        self.members.add(val.jsonstring().STRING().getText())

        elif value_ctx.jsonstring() is not None:
            # Scalar string value
            self.members.add(value_ctx.jsonstring().STRING().getText())
