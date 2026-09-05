from antlr4.error.ErrorStrategy import DefaultErrorStrategy, InputMismatchException
from antlr4.atn.ATNState import ATNState
from antlr4.error.ErrorListener import ErrorListener
from antlr4.IntervalSet import IntervalSet

from .o9IBPLListener import o9IBPLListener
from .o9IBPLParser import o9IBPLParser

import re


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




class CustomPluginListener(o9IBPLListener):
    def __init__(self, error_reporter=None):
        self.error_reporter = error_reporter if error_reporter else ListErrorReporter()
        self.rule = {
            'Query': '',    # done
            'Formulae': [], # done
            'Scope': '', # done
            'ScopeType': '',   # done
            'Measure_Name': [],  # done
            'isCoalesce': [],  
            'rhs_measures_coalesce': [], 
            'LHS_measure': [], #
            'LeadOffsets': [],
            'FilterExpr': '' # done
        }
        self.select = {
            'Query Type': '', # done
            'graphName': '', # done
            'namedSetExpr': [], # done
            'dimList': [], # done
            'measureList': [], # done
            'edgeList': [], # done
            'FilterExpr': '' # done
        }
        self.plugin = {
            'Query' : '', # done
            'Plugin Type': '', # not used
            'Plugin Name': '',
            'Measure Name': '',
            'Scope': '',
            'Arguments': {}	# done
        }
        self.parent_names = set()
        self.identifiers = set()
        self.is_from_interested_rule = False
        self._is_interested_level_attribute = False
        self._current_dimension_name = None
        self._is_interested_member_expression = False\
        

    def enterStatement(self, ctx: o9IBPLParser.StatementContext):
        formula = ctx.getText()
        self.rule['Formulae'].append(formula)
        pass

    def enterMember_measure_crossjoin(self, ctx: o9IBPLParser.Member_measure_crossjoinContext):
        self.rule['Scope'] = ctx.getText()
        pass

    def enterMeasure_name(self, ctx: o9IBPLParser.Measure_nameContext):
        # Assuming ctx1 is a previous context object from Member_measure_crossjoin
        # Corrected this line assuming you want to pair Measure_Name with Scope
        self.rule['Measure_Name'].append(ctx.getText())
        pass
        
        
    def enterValueLiteral(self, ctx:o9IBPLParser.ValueLiteralContext):
        text = ctx.getText().lower()
        if text.startswith('coalesce'):
            # Update pattern to capture measure names with any numeric constant
            # coalesce(m.[], int) / coalesce(int, m.[])
            # r'coalesce\(measure\.\[([^\]]+)\],\s*\d+\) ?(+/-/*///) coalesce\(measure\.\[([^\]]+)\], \s*\d+\)'
            pattern = r'coalesce\(measure\.\[([^\]]+)\],\s*\d+\)|coalesce\(\d+,\s*measure\.\[([^\]]+)\]\)'
            match = re.search(pattern, ctx.getText(), re.IGNORECASE)
            if match:
                self.rule['isCoalesce'].append(True)
                extracted_args = match.groups()
                non_zero_arg = next(arg for arg in extracted_args if arg is not None)
                self.rule['rhs_measures_coalesce'].append(non_zero_arg)
        pass



    def enterScopeStatement(self, ctx:o9IBPLParser.ScopeStatementContext):
        self.rule['ScopeType'] = 'Regular Scope'
        self.select['Query Type'] = 'Regular Scope'
        pass

    def enterBlockScopeStatement(self, ctx:o9IBPLParser.BlockScopeStatementContext):
        self.rule['ScopeType'] = 'Block Scope'
        self.select['Query Type'] = 'Block Scope'
        pass

    def enterScopePrefix(self, ctx:o9IBPLParser.ScopePrefixContext):
        scope = ctx.getText()
        
        self.rule['ScopeType'] = f"{scope} Scope"
        self.select['Query Type'] = f"{scope} Scope"
        pass

    def enterMeasure_with_scope_or_graph_coordinates(self, ctx:o9IBPLParser.Measure_with_scope_or_graph_coordinatesContext):
        self.rule['LeadOffsets'].append(ctx.getText())
        pass

    def enterRecurrenceScopeStatement(self, ctx:o9IBPLParser.RecurrenceScopeStatementContext):
        self.rule['ScopeType'] = 'Recurrence Scope'	
        self.select['Query Type'] = 'Recurrence Scope'
        pass

    def enterDimension_name(self, ctx):
        dim_name = ctx.getText().replace("[", "").replace("]", "")
        self._current_dimension_name = dim_name
        self.is_from_interested_rule = True
        pass

    def enterLevelattribute_name(self, ctx):
        dim_name = ctx.dimension_name().getText().replace("[", "").replace("]", "")
        attr_name = ctx.identifier().getText().replace("[", "").replace("]", "")
        self.select['dimList'].append({'dimName': dim_name, 'attrName': attr_name})
        self._is_interested_level_attribute = True
        pass

    def enterMemberSetReference(self, ctx):
        namedsetexpr = ctx.getText()
        pass

    def enterSelectMemberExprStatement(self, ctx:o9IBPLParser.SelectMemberExprStatementContext):
        self.select['Query Type'] = 'Select'
        pass

    def enterSelectGraphEdgeProjectStatement(self, ctx:o9IBPLParser.SelectGraphEdgeProjectStatementContext):
        self.select['Query Type'] = 'Select'
        pass

    def enterSelectGraphEdgesStatement(self, ctx:o9IBPLParser.SelectGraphEdgesStatementContext):
        self.select['Query Type'] = 'Select'
        pass

    def enterSelectGraphPathsStatement(self, ctx:o9IBPLParser.SelectGraphPathsStatementContext):
        self.select['Query Type'] = 'Select'
        pass
    
    def enterSelectDimensionGraphEdgesStatement(self, ctx:o9IBPLParser.SelectDimensionGraphEdgesStatementContext):
        self.select['Query Type'] = 'Select'
        pass

    def exitLevelattribute_name(self, ctx):
        self.is_from_interested_rule = False
        self._is_interested_level_attribute = False
        pass

    def enterMemberAncestorsAtLevel(self, ctx):
        self._is_interested_member_expression = True
        pass

    def enterMemberDescendantsAtLevel(self, ctx):
        self._is_interested_member_expression = True
        pass

    def enterMemberRelatedMembers(self, ctx):
        self._is_interested_member_expression = True
        pass

    def exitMemberAncestorsAtLevel(self, ctx):
        if self._is_interested_member_expression:
            str_name = ctx.identifier().getText().replace("[", "").replace("]", "")
            self.add_identifier(str_name)
        pass

    def exitMemberDescendantsAtLevel(self, ctx):
        if self._is_interested_member_expression:
            str_name = ctx.identifier().getText().replace("[", "").replace("]", "")
            self.add_identifier(str_name)
        pass

    def exitMemberRelatedMembers(self, ctx):
        if self._is_interested_member_expression:
            str_name = ctx.identifier().getText().replace("[", "").replace("]", "")
            self.add_identifier(str_name)
        pass

    def enterMemberSetReference(self, ctx):
        self.is_from_interested_rule = True
        self.select['namedSetExpr'].append(ctx.getText().strip('&'))
        pass

    def exitMemberSetReference(self, ctx):
        self.is_from_interested_rule = False
        pass

    def enterMeasure_with_scope_or_graph_coordinates(self, ctx):
        self.is_from_interested_rule = True
        pass

    def enterMeasure_name(self, ctx):
        self.is_from_interested_rule = True
        measureName = ctx.getText().split('.')[1]
        self.select['measureList'].append({'measure': measureName})
        pass

    def enterUnqualified_measure_name(self, ctx):
        self.is_from_interested_rule = True
        pass

    def exitMeasure_with_scope_or_graph_coordinates(self, ctx):
        self.is_from_interested_rule = False
        pass

    def exitMeasure_name(self, ctx):
        self.is_from_interested_rule = False
        pass

    def exitUnqualified_measure_name(self, ctx):
        self.is_from_interested_rule = False
        pass

    def add_identifier(self, identifier_name):
        self.identifiers.add(f"[{self._current_dimension_name}].[{identifier_name}]")
        self.is_from_interested_rule = False
        pass

    def enterGraphName(self, ctx):
        self.select['graphName'] = ctx.getText()
        pass

    def enterDimList(self, ctx):
        dim_name = ctx.getText().replace("[", "").replace("]", "")
        self.select['dimList'].append({'dimName': dim_name})
        pass

    def enterMeasureList(self, ctx):
        measure_name = ctx.getText().replace("[", "").replace("]", "")
        self.select['measureList'].append({'measureName': measure_name})
        pass

    def enterMeasure(self, ctx: o9IBPLParser.MeasureContext):
        measure_name = ctx.getText()
        pattern = r"Measure\.\[[^\]]+\]"
        match = re.search(pattern, measure_name)
        if match:
            result = match.group(0).split('.')[1]
        else:
            result = None
        self.select['measureList'].append({'measureName': result})
        pass

    def enterFully_qualified_edge_property(self, ctx: o9IBPLParser.Fully_qualified_edge_propertyContext):
        edge_name = ctx.getText().split('.')[2]
        self.select['edgeList'].append(edge_name)
        pass

    def enterEdgeList(self, ctx):
        edge_name = ctx.getText().replace("[", "").replace("]", "")
        self.select['edgeList'].append(edge_name)
        pass

    def enterStatement(self, ctx:o9IBPLParser.StatementContext):
        self.plugin['Query'] = ctx.getText()
        pass
    
    def enterOnDemandPluginStatement(self, ctx:o9IBPLParser.OnDemandPluginStatementContext):
        plugin_instance = ctx.identifier().getText()
        match = re.search(r'\[(.*?)\]', plugin_instance)
        if match:
            self.plugin['Plugin Name'] = match.group(1)
        else:
            self.plugin['Plugin Name'] = plugin_instance
        pass

    def enterUnqualified_measure_name(self, ctx:o9IBPLParser.Unqualified_measure_nameContext):
        measure_name = ctx.getText()[1:-1]
        self.plugin['Measure Name'] = measure_name
        pass

    def enterMember_crossjoin(self, ctx:o9IBPLParser.Member_crossjoinContext):
        scope = ctx.getText()[1:-1]
        self.plugin['Scope'] = scope
        pass

    def enterGenericNameValue(self, ctx:o9IBPLParser.GenericNameValueContext):
        arg = ctx.getText().replace('""',"").replace("[]", "").replace("[", "").replace("]", "")
        parts = arg[1:-1]
        key, value = parts.split(',')[0], parts.split(',')[1]  
        self.plugin['Arguments'][key] = value
        pass

    def enterMemberFilter(self, ctx:o9IBPLParser.MemberFilterContext):
        self.rule['FilterExpr'] = ctx.getText()
        self.select['FilterExpr'] = ctx.getText() 
        pass


    def enterMeasureFilterStatement(self, ctx:o9IBPLParser.MeasureFilterStatementContext):
        self.rule['FilterExpr'] = ctx.getText()
        self.select['FilterExpr'] = ctx.getText() 
        pass

    def enterMemberFilter(self, ctx:o9IBPLParser.MemberFilterContext):
        self.rule['FilterExpr'] = ctx.getText()
        self.select['FilterExpr'] = ctx.getText() 
        pass

    def enterMemberRelatedMembers(self, ctx:o9IBPLParser.MemberRelatedMembersContext):
        self.rule['FilterExpr'] = ctx.getText()
        self.select['FilterExpr'] = ctx.getText() 
        pass