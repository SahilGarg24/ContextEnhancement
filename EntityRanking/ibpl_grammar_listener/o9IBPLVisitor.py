# Generated from C:/Users/sahil.garg/PycharmProjects/Performance_Analyzer/ibpl_grammar_listener/o9IBPL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .o9IBPLParser import o9IBPLParser
else:
    from .o9IBPLParser import o9IBPLParser

# This class defines a complete generic visitor for a parse tree produced by o9IBPLParser.

class o9IBPLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by o9IBPLParser#block.
    def visitBlock(self, ctx:o9IBPLParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#statement.
    def visitStatement(self, ctx:o9IBPLParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#execExternalStatement.
    def visitExecExternalStatement(self, ctx:o9IBPLParser.ExecExternalStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#haRedisPassThroughStatement.
    def visitHaRedisPassThroughStatement(self, ctx:o9IBPLParser.HaRedisPassThroughStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#replayStatement.
    def visitReplayStatement(self, ctx:o9IBPLParser.ReplayStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#batchStartStatement.
    def visitBatchStartStatement(self, ctx:o9IBPLParser.BatchStartStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#batchEndStatement.
    def visitBatchEndStatement(self, ctx:o9IBPLParser.BatchEndStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ddlStatement.
    def visitDdlStatement(self, ctx:o9IBPLParser.DdlStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#dmlStatement.
    def visitDmlStatement(self, ctx:o9IBPLParser.DmlStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#json.
    def visitJson(self, ctx:o9IBPLParser.JsonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#jsonObject.
    def visitJsonObject(self, ctx:o9IBPLParser.JsonObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#jsonPair.
    def visitJsonPair(self, ctx:o9IBPLParser.JsonPairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#jsonArray.
    def visitJsonArray(self, ctx:o9IBPLParser.JsonArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#jsonValue.
    def visitJsonValue(self, ctx:o9IBPLParser.JsonValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#jsonstring.
    def visitJsonstring(self, ctx:o9IBPLParser.JsonstringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#jsonnumber.
    def visitJsonnumber(self, ctx:o9IBPLParser.JsonnumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#garbageCollectStatement.
    def visitGarbageCollectStatement(self, ctx:o9IBPLParser.GarbageCollectStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#registerAlertStatement.
    def visitRegisterAlertStatement(self, ctx:o9IBPLParser.RegisterAlertStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#deregisterAlertStatement.
    def visitDeregisterAlertStatement(self, ctx:o9IBPLParser.DeregisterAlertStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#from_tail.
    def visitFrom_tail(self, ctx:o9IBPLParser.From_tailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#to_head.
    def visitTo_head(self, ctx:o9IBPLParser.To_headContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edgeDirection.
    def visitEdgeDirection(self, ctx:o9IBPLParser.EdgeDirectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#traverseDirection.
    def visitTraverseDirection(self, ctx:o9IBPLParser.TraverseDirectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#traverseDistance.
    def visitTraverseDistance(self, ctx:o9IBPLParser.TraverseDistanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphNameOrIdentfier.
    def visitGraphNameOrIdentfier(self, ctx:o9IBPLParser.GraphNameOrIdentfierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graph_identifier.
    def visitGraph_identifier(self, ctx:o9IBPLParser.Graph_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphName.
    def visitGraphName(self, ctx:o9IBPLParser.GraphNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edge_property.
    def visitEdge_property(self, ctx:o9IBPLParser.Edge_propertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edgePropertyName.
    def visitEdgePropertyName(self, ctx:o9IBPLParser.EdgePropertyNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#nameSpace.
    def visitNameSpace(self, ctx:o9IBPLParser.NameSpaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#fully_qualified_edge_property.
    def visitFully_qualified_edge_property(self, ctx:o9IBPLParser.Fully_qualified_edge_propertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#fully_qualified_edge_property_with_vertex_coordinates.
    def visitFully_qualified_edge_property_with_vertex_coordinates(self, ctx:o9IBPLParser.Fully_qualified_edge_property_with_vertex_coordinatesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edge_node_member_property.
    def visitEdge_node_member_property(self, ctx:o9IBPLParser.Edge_node_member_propertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#node_member_property.
    def visitNode_member_property(self, ctx:o9IBPLParser.Node_member_propertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#nameValue.
    def visitNameValue(self, ctx:o9IBPLParser.NameValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#genericNameValue.
    def visitGenericNameValue(self, ctx:o9IBPLParser.GenericNameValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edgePredicate_expression.
    def visitEdgePredicate_expression(self, ctx:o9IBPLParser.EdgePredicate_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#vertexPredicate_expression.
    def visitVertexPredicate_expression(self, ctx:o9IBPLParser.VertexPredicate_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphLevelAttributeName.
    def visitGraphLevelAttributeName(self, ctx:o9IBPLParser.GraphLevelAttributeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphVersion_expression.
    def visitGraphVersion_expression(self, ctx:o9IBPLParser.GraphVersion_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#updateGraphStatement.
    def visitUpdateGraphStatement(self, ctx:o9IBPLParser.UpdateGraphStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#EdgeCreate.
    def visitEdgeCreate(self, ctx:o9IBPLParser.EdgeCreateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#EdgeModify.
    def visitEdgeModify(self, ctx:o9IBPLParser.EdgeModifyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#EdgeDelete.
    def visitEdgeDelete(self, ctx:o9IBPLParser.EdgeDeleteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphNodePairClause.
    def visitGraphNodePairClause(self, ctx:o9IBPLParser.GraphNodePairClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphNodeClause.
    def visitGraphNodeClause(self, ctx:o9IBPLParser.GraphNodeClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphMemberNode.
    def visitGraphMemberNode(self, ctx:o9IBPLParser.GraphMemberNodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edgePropertiesClause.
    def visitEdgePropertiesClause(self, ctx:o9IBPLParser.EdgePropertiesClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#VertexSetName.
    def visitVertexSetName(self, ctx:o9IBPLParser.VertexSetNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#VertexSetExpr.
    def visitVertexSetExpr(self, ctx:o9IBPLParser.VertexSetExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#VertexSetFromMemberSets.
    def visitVertexSetFromMemberSets(self, ctx:o9IBPLParser.VertexSetFromMemberSetsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#VertexSetFromMemberSet.
    def visitVertexSetFromMemberSet(self, ctx:o9IBPLParser.VertexSetFromMemberSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#SubGraphName.
    def visitSubGraphName(self, ctx:o9IBPLParser.SubGraphNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#SubGraphExpr.
    def visitSubGraphExpr(self, ctx:o9IBPLParser.SubGraphExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#subGraphVertexSet_expression.
    def visitSubGraphVertexSet_expression(self, ctx:o9IBPLParser.SubGraphVertexSet_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#TraverseGraphName.
    def visitTraverseGraphName(self, ctx:o9IBPLParser.TraverseGraphNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#TraverseGraphExp.
    def visitTraverseGraphExp(self, ctx:o9IBPLParser.TraverseGraphExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edgeSet_expression.
    def visitEdgeSet_expression(self, ctx:o9IBPLParser.EdgeSet_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphNodeMembersStatement.
    def visitGraphNodeMembersStatement(self, ctx:o9IBPLParser.GraphNodeMembersStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#selectGraphEdgeProjectStatement.
    def visitSelectGraphEdgeProjectStatement(self, ctx:o9IBPLParser.SelectGraphEdgeProjectStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edgeProjectPredicate_expression.
    def visitEdgeProjectPredicate_expression(self, ctx:o9IBPLParser.EdgeProjectPredicate_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#selectGraphEdgesStatement.
    def visitSelectGraphEdgesStatement(self, ctx:o9IBPLParser.SelectGraphEdgesStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edge_crossjoin.
    def visitEdge_crossjoin(self, ctx:o9IBPLParser.Edge_crossjoinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edge_crossjoin_element.
    def visitEdge_crossjoin_element(self, ctx:o9IBPLParser.Edge_crossjoin_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graph_traversal_options.
    def visitGraph_traversal_options(self, ctx:o9IBPLParser.Graph_traversal_optionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graph_traversal_start_set.
    def visitGraph_traversal_start_set(self, ctx:o9IBPLParser.Graph_traversal_start_setContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graph_filter_set.
    def visitGraph_filter_set(self, ctx:o9IBPLParser.Graph_filter_setContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graph_filter_element.
    def visitGraph_filter_element(self, ctx:o9IBPLParser.Graph_filter_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#rel_edgePredicate_expression.
    def visitRel_edgePredicate_expression(self, ctx:o9IBPLParser.Rel_edgePredicate_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#selectGraphPathsStatement.
    def visitSelectGraphPathsStatement(self, ctx:o9IBPLParser.SelectGraphPathsStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graph_path_filter_set.
    def visitGraph_path_filter_set(self, ctx:o9IBPLParser.Graph_path_filter_setContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graph_path_filter_element.
    def visitGraph_path_filter_element(self, ctx:o9IBPLParser.Graph_path_filter_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#selectDimensionGraphEdgesStatement.
    def visitSelectDimensionGraphEdgesStatement(self, ctx:o9IBPLParser.SelectDimensionGraphEdgesStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#dimgraph_where_clause.
    def visitDimgraph_where_clause(self, ctx:o9IBPLParser.Dimgraph_where_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#blockStatement.
    def visitBlockStatement(self, ctx:o9IBPLParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#execParallelStatement.
    def visitExecParallelStatement(self, ctx:o9IBPLParser.ExecParallelStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#denyAccessStatement.
    def visitDenyAccessStatement(self, ctx:o9IBPLParser.DenyAccessStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#DenyDimensionReadAccessAtMemberSet.
    def visitDenyDimensionReadAccessAtMemberSet(self, ctx:o9IBPLParser.DenyDimensionReadAccessAtMemberSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#DenyDimensionReadAccessAtDimension.
    def visitDenyDimensionReadAccessAtDimension(self, ctx:o9IBPLParser.DenyDimensionReadAccessAtDimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#DenyDimensionReadAccessAtAttribute.
    def visitDenyDimensionReadAccessAtAttribute(self, ctx:o9IBPLParser.DenyDimensionReadAccessAtAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#denyReadPrefixStatement.
    def visitDenyReadPrefixStatement(self, ctx:o9IBPLParser.DenyReadPrefixStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#grantAccessStatement.
    def visitGrantAccessStatement(self, ctx:o9IBPLParser.GrantAccessStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#accessDeclarationStatement.
    def visitAccessDeclarationStatement(self, ctx:o9IBPLParser.AccessDeclarationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#grantWriteAccessPrefixStatement.
    def visitGrantWriteAccessPrefixStatement(self, ctx:o9IBPLParser.GrantWriteAccessPrefixStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#grantReadAccessPrefixStatement.
    def visitGrantReadAccessPrefixStatement(self, ctx:o9IBPLParser.GrantReadAccessPrefixStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#grantExclusiveReadAccessPrefixStatement.
    def visitGrantExclusiveReadAccessPrefixStatement(self, ctx:o9IBPLParser.GrantExclusiveReadAccessPrefixStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GrantDimensionWriteAccess.
    def visitGrantDimensionWriteAccess(self, ctx:o9IBPLParser.GrantDimensionWriteAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GrantCellWriteAccess.
    def visitGrantCellWriteAccess(self, ctx:o9IBPLParser.GrantCellWriteAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GrantDimensionWriteAccessAtMemberSet.
    def visitGrantDimensionWriteAccessAtMemberSet(self, ctx:o9IBPLParser.GrantDimensionWriteAccessAtMemberSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GrantDimensionWriteAccessAtDimension.
    def visitGrantDimensionWriteAccessAtDimension(self, ctx:o9IBPLParser.GrantDimensionWriteAccessAtDimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GrantDimensionWriteAccessAtAttribute.
    def visitGrantDimensionWriteAccessAtAttribute(self, ctx:o9IBPLParser.GrantDimensionWriteAccessAtAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GrantDimensionExclusiveReadAccessAtMemberSet.
    def visitGrantDimensionExclusiveReadAccessAtMemberSet(self, ctx:o9IBPLParser.GrantDimensionExclusiveReadAccessAtMemberSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GrantDimensionExclusiveReadAccessAtDimension.
    def visitGrantDimensionExclusiveReadAccessAtDimension(self, ctx:o9IBPLParser.GrantDimensionExclusiveReadAccessAtDimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GrantDimensionExclusiveReadAccessAtAttribute.
    def visitGrantDimensionExclusiveReadAccessAtAttribute(self, ctx:o9IBPLParser.GrantDimensionExclusiveReadAccessAtAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#grantCellWriteAccessStatement.
    def visitGrantCellWriteAccessStatement(self, ctx:o9IBPLParser.GrantCellWriteAccessStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#grantCellReadAccessStatement.
    def visitGrantCellReadAccessStatement(self, ctx:o9IBPLParser.GrantCellReadAccessStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GrantDimensionReadAccessAtMemberSet.
    def visitGrantDimensionReadAccessAtMemberSet(self, ctx:o9IBPLParser.GrantDimensionReadAccessAtMemberSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GrantDimensionReadAccessAtDimension.
    def visitGrantDimensionReadAccessAtDimension(self, ctx:o9IBPLParser.GrantDimensionReadAccessAtDimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GrantDimensionReadAccessAtAttribute.
    def visitGrantDimensionReadAccessAtAttribute(self, ctx:o9IBPLParser.GrantDimensionReadAccessAtAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GrantDimensionReadAccessAtAttributeBasedOnMeasure.
    def visitGrantDimensionReadAccessAtAttributeBasedOnMeasure(self, ctx:o9IBPLParser.GrantDimensionReadAccessAtAttributeBasedOnMeasureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#attributeAccessStatement.
    def visitAttributeAccessStatement(self, ctx:o9IBPLParser.AttributeAccessStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#denyCellWriteAccessStatement.
    def visitDenyCellWriteAccessStatement(self, ctx:o9IBPLParser.DenyCellWriteAccessStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#denyWritePrefixStatement.
    def visitDenyWritePrefixStatement(self, ctx:o9IBPLParser.DenyWritePrefixStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#PlanAccess.
    def visitPlanAccess(self, ctx:o9IBPLParser.PlanAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MeasureGroupAccess.
    def visitMeasureGroupAccess(self, ctx:o9IBPLParser.MeasureGroupAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MeasureAccess.
    def visitMeasureAccess(self, ctx:o9IBPLParser.MeasureAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#getAccessControlRulesInfo.
    def visitGetAccessControlRulesInfo(self, ctx:o9IBPLParser.GetAccessControlRulesInfoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measureFilterStatement.
    def visitMeasureFilterStatement(self, ctx:o9IBPLParser.MeasureFilterStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#activePluginStatement.
    def visitActivePluginStatement(self, ctx:o9IBPLParser.ActivePluginStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#onDemandPluginStatement.
    def visitOnDemandPluginStatement(self, ctx:o9IBPLParser.OnDemandPluginStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#executePowershellPluginStatement.
    def visitExecutePowershellPluginStatement(self, ctx:o9IBPLParser.ExecutePowershellPluginStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#operatingScopeStatement.
    def visitOperatingScopeStatement(self, ctx:o9IBPLParser.OperatingScopeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#usingArgumentsClause.
    def visitUsingArgumentsClause(self, ctx:o9IBPLParser.UsingArgumentsClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#argumentsClause.
    def visitArgumentsClause(self, ctx:o9IBPLParser.ArgumentsClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#postActionClause.
    def visitPostActionClause(self, ctx:o9IBPLParser.PostActionClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#scenarioScopeStatement.
    def visitScenarioScopeStatement(self, ctx:o9IBPLParser.ScenarioScopeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#usingScopeStatement.
    def visitUsingScopeStatement(self, ctx:o9IBPLParser.UsingScopeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#scopeClause.
    def visitScopeClause(self, ctx:o9IBPLParser.ScopeClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#globalScenarioScopeStatement.
    def visitGlobalScenarioScopeStatement(self, ctx:o9IBPLParser.GlobalScenarioScopeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measureList.
    def visitMeasureList(self, ctx:o9IBPLParser.MeasureListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#identifierList.
    def visitIdentifierList(self, ctx:o9IBPLParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#referMeasuresInParent.
    def visitReferMeasuresInParent(self, ctx:o9IBPLParser.ReferMeasuresInParentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#mgOverriddenLocalScopeList.
    def visitMgOverriddenLocalScopeList(self, ctx:o9IBPLParser.MgOverriddenLocalScopeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#mgOverriddenScopeList.
    def visitMgOverriddenScopeList(self, ctx:o9IBPLParser.MgOverriddenScopeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#includeModelsStatement.
    def visitIncludeModelsStatement(self, ctx:o9IBPLParser.IncludeModelsStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#mgNewOverriddenLocalScopeList.
    def visitMgNewOverriddenLocalScopeList(self, ctx:o9IBPLParser.MgNewOverriddenLocalScopeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#planLocalScopeList.
    def visitPlanLocalScopeList(self, ctx:o9IBPLParser.PlanLocalScopeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#planOveriddenScopeList.
    def visitPlanOveriddenScopeList(self, ctx:o9IBPLParser.PlanOveriddenScopeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#mgNewOverriddenScopeList.
    def visitMgNewOverriddenScopeList(self, ctx:o9IBPLParser.MgNewOverriddenScopeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#includeMeasuresStatement.
    def visitIncludeMeasuresStatement(self, ctx:o9IBPLParser.IncludeMeasuresStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#includePointerMeasuresStatement.
    def visitIncludePointerMeasuresStatement(self, ctx:o9IBPLParser.IncludePointerMeasuresStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#includePointerMeasuresList.
    def visitIncludePointerMeasuresList(self, ctx:o9IBPLParser.IncludePointerMeasuresListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#mgScopeList.
    def visitMgScopeList(self, ctx:o9IBPLParser.MgScopeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#mgScopeStatement.
    def visitMgScopeStatement(self, ctx:o9IBPLParser.MgScopeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphScopeList.
    def visitGraphScopeList(self, ctx:o9IBPLParser.GraphScopeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphScopeStatement.
    def visitGraphScopeStatement(self, ctx:o9IBPLParser.GraphScopeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#includePlanStatement.
    def visitIncludePlanStatement(self, ctx:o9IBPLParser.IncludePlanStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#includePlanStatementList.
    def visitIncludePlanStatementList(self, ctx:o9IBPLParser.IncludePlanStatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#fromVertexStatement.
    def visitFromVertexStatement(self, ctx:o9IBPLParser.FromVertexStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#toVertexStatement.
    def visitToVertexStatement(self, ctx:o9IBPLParser.ToVertexStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#usingVertexScopeStatement.
    def visitUsingVertexScopeStatement(self, ctx:o9IBPLParser.UsingVertexScopeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edgeList.
    def visitEdgeList(self, ctx:o9IBPLParser.EdgeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#fullyQualifiedEdgeList.
    def visitFullyQualifiedEdgeList(self, ctx:o9IBPLParser.FullyQualifiedEdgeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#referEdgePropInParent.
    def visitReferEdgePropInParent(self, ctx:o9IBPLParser.ReferEdgePropInParentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphOverriddenLocalScopeList.
    def visitGraphOverriddenLocalScopeList(self, ctx:o9IBPLParser.GraphOverriddenLocalScopeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphOverriddenScopeList.
    def visitGraphOverriddenScopeList(self, ctx:o9IBPLParser.GraphOverriddenScopeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#includeGraphsStatement.
    def visitIncludeGraphsStatement(self, ctx:o9IBPLParser.IncludeGraphsStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edgeOverriddenLocalScopeList.
    def visitEdgeOverriddenLocalScopeList(self, ctx:o9IBPLParser.EdgeOverriddenLocalScopeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edgeOverriddenScopeList.
    def visitEdgeOverriddenScopeList(self, ctx:o9IBPLParser.EdgeOverriddenScopeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#includeEdgesStatement.
    def visitIncludeEdgesStatement(self, ctx:o9IBPLParser.IncludeEdgesStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#pointerEdgeStatement.
    def visitPointerEdgeStatement(self, ctx:o9IBPLParser.PointerEdgeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#pointerEdgeStatementList.
    def visitPointerEdgeStatementList(self, ctx:o9IBPLParser.PointerEdgeStatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#includeDependentEntities.
    def visitIncludeDependentEntities(self, ctx:o9IBPLParser.IncludeDependentEntitiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#initializeScenarioStatement.
    def visitInitializeScenarioStatement(self, ctx:o9IBPLParser.InitializeScenarioStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#initializeMeasureGroupStatement.
    def visitInitializeMeasureGroupStatement(self, ctx:o9IBPLParser.InitializeMeasureGroupStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#initializeMeasuresStatement.
    def visitInitializeMeasuresStatement(self, ctx:o9IBPLParser.InitializeMeasuresStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#initializeGraphStatement.
    def visitInitializeGraphStatement(self, ctx:o9IBPLParser.InitializeGraphStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#initializeEdgeStatement.
    def visitInitializeEdgeStatement(self, ctx:o9IBPLParser.InitializeEdgeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#versionArgs.
    def visitVersionArgs(self, ctx:o9IBPLParser.VersionArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#genericVersionArgs.
    def visitGenericVersionArgs(self, ctx:o9IBPLParser.GenericVersionArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#argValuePair.
    def visitArgValuePair(self, ctx:o9IBPLParser.ArgValuePairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#versionNameOrExp.
    def visitVersionNameOrExp(self, ctx:o9IBPLParser.VersionNameOrExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#createVersionStatement.
    def visitCreateVersionStatement(self, ctx:o9IBPLParser.CreateVersionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#createScenarioStatement.
    def visitCreateScenarioStatement(self, ctx:o9IBPLParser.CreateScenarioStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#createScopedScenarioStatement.
    def visitCreateScopedScenarioStatement(self, ctx:o9IBPLParser.CreateScopedScenarioStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#createLWScenarioStatement.
    def visitCreateLWScenarioStatement(self, ctx:o9IBPLParser.CreateLWScenarioStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#createEphemeralScenarioStatement.
    def visitCreateEphemeralScenarioStatement(self, ctx:o9IBPLParser.CreateEphemeralScenarioStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#scenarioSourceExpression.
    def visitScenarioSourceExpression(self, ctx:o9IBPLParser.ScenarioSourceExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#deleteVersionStatement.
    def visitDeleteVersionStatement(self, ctx:o9IBPLParser.DeleteVersionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#updateScenarioStatement.
    def visitUpdateScenarioStatement(self, ctx:o9IBPLParser.UpdateScenarioStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#updateVersionPropertyStatement.
    def visitUpdateVersionPropertyStatement(self, ctx:o9IBPLParser.UpdateVersionPropertyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#shareScenarioStatement.
    def visitShareScenarioStatement(self, ctx:o9IBPLParser.ShareScenarioStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#unshareScenarioStatement.
    def visitUnshareScenarioStatement(self, ctx:o9IBPLParser.UnshareScenarioStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#versionExpressionStatement.
    def visitVersionExpressionStatement(self, ctx:o9IBPLParser.VersionExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#createMemberStatement.
    def visitCreateMemberStatement(self, ctx:o9IBPLParser.CreateMemberStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#updateMemberStatement.
    def visitUpdateMemberStatement(self, ctx:o9IBPLParser.UpdateMemberStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#deleteMemberStatement.
    def visitDeleteMemberStatement(self, ctx:o9IBPLParser.DeleteMemberStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#copyMemberStatement.
    def visitCopyMemberStatement(self, ctx:o9IBPLParser.CopyMemberStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#copyMemberSourceMembers.
    def visitCopyMemberSourceMembers(self, ctx:o9IBPLParser.CopyMemberSourceMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#copyMemberParentMembers.
    def visitCopyMemberParentMembers(self, ctx:o9IBPLParser.CopyMemberParentMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#copyMeasureStatement.
    def visitCopyMeasureStatement(self, ctx:o9IBPLParser.CopyMeasureStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#copyMeasureOptions.
    def visitCopyMeasureOptions(self, ctx:o9IBPLParser.CopyMeasureOptionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#crudMemberStatement.
    def visitCrudMemberStatement(self, ctx:o9IBPLParser.CrudMemberStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#crudMemberStatementSet.
    def visitCrudMemberStatementSet(self, ctx:o9IBPLParser.CrudMemberStatementSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#purgeMemberStatement.
    def visitPurgeMemberStatement(self, ctx:o9IBPLParser.PurgeMemberStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#bulkMemberCreateStatement.
    def visitBulkMemberCreateStatement(self, ctx:o9IBPLParser.BulkMemberCreateStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#filePaths.
    def visitFilePaths(self, ctx:o9IBPLParser.FilePathsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#uploadDatafileStatement.
    def visitUploadDatafileStatement(self, ctx:o9IBPLParser.UploadDatafileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#downloadDatafileStatement.
    def visitDownloadDatafileStatement(self, ctx:o9IBPLParser.DownloadDatafileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#commandOption.
    def visitCommandOption(self, ctx:o9IBPLParser.CommandOptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#exportAllStatement.
    def visitExportAllStatement(self, ctx:o9IBPLParser.ExportAllStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#importAllStatement.
    def visitImportAllStatement(self, ctx:o9IBPLParser.ImportAllStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#saveStatement.
    def visitSaveStatement(self, ctx:o9IBPLParser.SaveStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#serviceCommandStatement.
    def visitServiceCommandStatement(self, ctx:o9IBPLParser.ServiceCommandStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#restoreExternalDataStatement.
    def visitRestoreExternalDataStatement(self, ctx:o9IBPLParser.RestoreExternalDataStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#syncExternalModelsStatement.
    def visitSyncExternalModelsStatement(self, ctx:o9IBPLParser.SyncExternalModelsStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#syncLocalModelsStatement.
    def visitSyncLocalModelsStatement(self, ctx:o9IBPLParser.SyncLocalModelsStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#syncLocalExcludePropertyList.
    def visitSyncLocalExcludePropertyList(self, ctx:o9IBPLParser.SyncLocalExcludePropertyListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#refreshMaterializedViewsStatement.
    def visitRefreshMaterializedViewsStatement(self, ctx:o9IBPLParser.RefreshMaterializedViewsStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#releaseTableMemoryStatement.
    def visitReleaseTableMemoryStatement(self, ctx:o9IBPLParser.ReleaseTableMemoryStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#mergeDeltaModelsStatement.
    def visitMergeDeltaModelsStatement(self, ctx:o9IBPLParser.MergeDeltaModelsStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#resetAccessControlStatement.
    def visitResetAccessControlStatement(self, ctx:o9IBPLParser.ResetAccessControlStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#generateGraphStatement.
    def visitGenerateGraphStatement(self, ctx:o9IBPLParser.GenerateGraphStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#netChangeAclStatement.
    def visitNetChangeAclStatement(self, ctx:o9IBPLParser.NetChangeAclStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#netChangeAclRoleStatement.
    def visitNetChangeAclRoleStatement(self, ctx:o9IBPLParser.NetChangeAclRoleStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#rolePropertyValuePair.
    def visitRolePropertyValuePair(self, ctx:o9IBPLParser.RolePropertyValuePairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#netChangeAclRuleStatement.
    def visitNetChangeAclRuleStatement(self, ctx:o9IBPLParser.NetChangeAclRuleStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#simulateWriteStatement.
    def visitSimulateWriteStatement(self, ctx:o9IBPLParser.SimulateWriteStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#memberAttributeAssignment.
    def visitMemberAttributeAssignment(self, ctx:o9IBPLParser.MemberAttributeAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#memberNameAssignmentPairs.
    def visitMemberNameAssignmentPairs(self, ctx:o9IBPLParser.MemberNameAssignmentPairsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#memberAssignmentPairs.
    def visitMemberAssignmentPairs(self, ctx:o9IBPLParser.MemberAssignmentPairsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#memberNamePair.
    def visitMemberNamePair(self, ctx:o9IBPLParser.MemberNamePairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#currentUserStatement.
    def visitCurrentUserStatement(self, ctx:o9IBPLParser.CurrentUserStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#selectMemberExprStatement.
    def visitSelectMemberExprStatement(self, ctx:o9IBPLParser.SelectMemberExprStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#selectCrossJoinStatement.
    def visitSelectCrossJoinStatement(self, ctx:o9IBPLParser.SelectCrossJoinStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#selectCrossJoinStatementWithPostFilter.
    def visitSelectCrossJoinStatementWithPostFilter(self, ctx:o9IBPLParser.SelectCrossJoinStatementWithPostFilterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#selectMemberStatement.
    def visitSelectMemberStatement(self, ctx:o9IBPLParser.SelectMemberStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#selectScenarioScopedMemberStatement.
    def visitSelectScenarioScopedMemberStatement(self, ctx:o9IBPLParser.SelectScenarioScopedMemberStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#countSelectMemberExprStatement.
    def visitCountSelectMemberExprStatement(self, ctx:o9IBPLParser.CountSelectMemberExprStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#spreadSelectCrossJoinStatement.
    def visitSpreadSelectCrossJoinStatement(self, ctx:o9IBPLParser.SpreadSelectCrossJoinStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#member_filter_set.
    def visitMember_filter_set(self, ctx:o9IBPLParser.Member_filter_setContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#member_filter.
    def visitMember_filter(self, ctx:o9IBPLParser.Member_filterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#withCalcMembersClause.
    def visitWithCalcMembersClause(self, ctx:o9IBPLParser.WithCalcMembersClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#calcMemberClause.
    def visitCalcMemberClause(self, ctx:o9IBPLParser.CalcMemberClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#calcMemberCellPropertiesClause.
    def visitCalcMemberCellPropertiesClause(self, ctx:o9IBPLParser.CalcMemberCellPropertiesClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measure_cell_properties_pair.
    def visitMeasure_cell_properties_pair(self, ctx:o9IBPLParser.Measure_cell_properties_pairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#cell_property_override.
    def visitCell_property_override(self, ctx:o9IBPLParser.Cell_property_overrideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#calcMemberOverridesClause.
    def visitCalcMemberOverridesClause(self, ctx:o9IBPLParser.CalcMemberOverridesClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measure_calcmemberexpression_pair.
    def visitMeasure_calcmemberexpression_pair(self, ctx:o9IBPLParser.Measure_calcmemberexpression_pairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#withTransientMeasureClause.
    def visitWithTransientMeasureClause(self, ctx:o9IBPLParser.WithTransientMeasureClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#transientMeasureClause.
    def visitTransientMeasureClause(self, ctx:o9IBPLParser.TransientMeasureClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#transientMeasurePropertyClause.
    def visitTransientMeasurePropertyClause(self, ctx:o9IBPLParser.TransientMeasurePropertyClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#cellPropertyClause.
    def visitCellPropertyClause(self, ctx:o9IBPLParser.CellPropertyClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#orderByClause.
    def visitOrderByClause(self, ctx:o9IBPLParser.OrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#limitClause.
    def visitLimitClause(self, ctx:o9IBPLParser.LimitClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#topClause.
    def visitTopClause(self, ctx:o9IBPLParser.TopClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#bottomClause.
    def visitBottomClause(self, ctx:o9IBPLParser.BottomClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#offsetClause.
    def visitOffsetClause(self, ctx:o9IBPLParser.OffsetClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#memberOrMeasureNameOrderByClause.
    def visitMemberOrMeasureNameOrderByClause(self, ctx:o9IBPLParser.MemberOrMeasureNameOrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#memberPropertyOrderByClause.
    def visitMemberPropertyOrderByClause(self, ctx:o9IBPLParser.MemberPropertyOrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measureNameOrderByClause.
    def visitMeasureNameOrderByClause(self, ctx:o9IBPLParser.MeasureNameOrderByClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#join_on_clause.
    def visitJoin_on_clause(self, ctx:o9IBPLParser.Join_on_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#join_expression.
    def visitJoin_expression(self, ctx:o9IBPLParser.Join_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#convert_using_clause.
    def visitConvert_using_clause(self, ctx:o9IBPLParser.Convert_using_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#adornmentInfo.
    def visitAdornmentInfo(self, ctx:o9IBPLParser.AdornmentInfoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#use_aliases.
    def visitUse_aliases(self, ctx:o9IBPLParser.Use_aliasesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#alias.
    def visitAlias(self, ctx:o9IBPLParser.AliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#dimension_attribute_alias.
    def visitDimension_attribute_alias(self, ctx:o9IBPLParser.Dimension_attribute_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#node_alias.
    def visitNode_alias(self, ctx:o9IBPLParser.Node_aliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#include_properties.
    def visitInclude_properties(self, ctx:o9IBPLParser.Include_propertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#include_member_properties.
    def visitInclude_member_properties(self, ctx:o9IBPLParser.Include_member_propertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#include_anchor_members.
    def visitInclude_anchor_members(self, ctx:o9IBPLParser.Include_anchor_membersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#anchor_members.
    def visitAnchor_members(self, ctx:o9IBPLParser.Anchor_membersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#query_option_list.
    def visitQuery_option_list(self, ctx:o9IBPLParser.Query_option_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#query_option.
    def visitQuery_option(self, ctx:o9IBPLParser.Query_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#include_nullmember.
    def visitInclude_nullmember(self, ctx:o9IBPLParser.Include_nullmemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#include_subtotals.
    def visitInclude_subtotals(self, ctx:o9IBPLParser.Include_subtotalsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#include_subtotals_sub_query.
    def visitInclude_subtotals_sub_query(self, ctx:o9IBPLParser.Include_subtotals_sub_queryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#sub_query.
    def visitSub_query(self, ctx:o9IBPLParser.Sub_queryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#sub_query_element.
    def visitSub_query_element(self, ctx:o9IBPLParser.Sub_query_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#include_nulls.
    def visitInclude_nulls(self, ctx:o9IBPLParser.Include_nullsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#member_measure_filter_set.
    def visitMember_measure_filter_set(self, ctx:o9IBPLParser.Member_measure_filter_setContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#member_measure_filter.
    def visitMember_measure_filter(self, ctx:o9IBPLParser.Member_measure_filterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measureZeroClause.
    def visitMeasureZeroClause(self, ctx:o9IBPLParser.MeasureZeroClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#attribute_properties.
    def visitAttribute_properties(self, ctx:o9IBPLParser.Attribute_propertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#computePlanStatement.
    def visitComputePlanStatement(self, ctx:o9IBPLParser.ComputePlanStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#enableDisablePlanStatement.
    def visitEnableDisablePlanStatement(self, ctx:o9IBPLParser.EnableDisablePlanStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#beginTransactionStatement.
    def visitBeginTransactionStatement(self, ctx:o9IBPLParser.BeginTransactionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#commitTransactionStatement.
    def visitCommitTransactionStatement(self, ctx:o9IBPLParser.CommitTransactionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#DiscardTransaction.
    def visitDiscardTransaction(self, ctx:o9IBPLParser.DiscardTransactionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#DiscardTransactionWithImpact.
    def visitDiscardTransactionWithImpact(self, ctx:o9IBPLParser.DiscardTransactionWithImpactContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#abortTransaction.
    def visitAbortTransaction(self, ctx:o9IBPLParser.AbortTransactionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#UpdateAssignment.
    def visitUpdateAssignment(self, ctx:o9IBPLParser.UpdateAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#UpdateSingleTupleSet.
    def visitUpdateSingleTupleSet(self, ctx:o9IBPLParser.UpdateSingleTupleSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#UpdateMultiTupleSet.
    def visitUpdateMultiTupleSet(self, ctx:o9IBPLParser.UpdateMultiTupleSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#updateStatementWithImpact.
    def visitUpdateStatementWithImpact(self, ctx:o9IBPLParser.UpdateStatementWithImpactContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#respreadStatement.
    def visitRespreadStatement(self, ctx:o9IBPLParser.RespreadStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#respreadStatementWithImpact.
    def visitRespreadStatementWithImpact(self, ctx:o9IBPLParser.RespreadStatementWithImpactContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measure_or_edge_property_update.
    def visitMeasure_or_edge_property_update(self, ctx:o9IBPLParser.Measure_or_edge_property_updateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#tuple_cell_assignment.
    def visitTuple_cell_assignment(self, ctx:o9IBPLParser.Tuple_cell_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#cell_property_assignment.
    def visitCell_property_assignment(self, ctx:o9IBPLParser.Cell_property_assignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#massUpdateStatement.
    def visitMassUpdateStatement(self, ctx:o9IBPLParser.MassUpdateStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#sanityCheckStatement.
    def visitSanityCheckStatement(self, ctx:o9IBPLParser.SanityCheckStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GatherColumnStatsForMeasureGroup.
    def visitGatherColumnStatsForMeasureGroup(self, ctx:o9IBPLParser.GatherColumnStatsForMeasureGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#GatherColumnStatsForDimension.
    def visitGatherColumnStatsForDimension(self, ctx:o9IBPLParser.GatherColumnStatsForDimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#explainStatement.
    def visitExplainStatement(self, ctx:o9IBPLParser.ExplainStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#AmplifyRedo.
    def visitAmplifyRedo(self, ctx:o9IBPLParser.AmplifyRedoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#DeleteFactMeasureGroup.
    def visitDeleteFactMeasureGroup(self, ctx:o9IBPLParser.DeleteFactMeasureGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#DeleteFactMembers.
    def visitDeleteFactMembers(self, ctx:o9IBPLParser.DeleteFactMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#DeleteGraphEdges.
    def visitDeleteGraphEdges(self, ctx:o9IBPLParser.DeleteGraphEdgesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measureGroupSet.
    def visitMeasureGroupSet(self, ctx:o9IBPLParser.MeasureGroupSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measureGroupList.
    def visitMeasureGroupList(self, ctx:o9IBPLParser.MeasureGroupListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphSet.
    def visitGraphSet(self, ctx:o9IBPLParser.GraphSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphList.
    def visitGraphList(self, ctx:o9IBPLParser.GraphListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#planList.
    def visitPlanList(self, ctx:o9IBPLParser.PlanListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#mgAndGraphGroupSet.
    def visitMgAndGraphGroupSet(self, ctx:o9IBPLParser.MgAndGraphGroupSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#deleteEdgesFilterClause.
    def visitDeleteEdgesFilterClause(self, ctx:o9IBPLParser.DeleteEdgesFilterClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#rel_deleteEdgesFilter_expression.
    def visitRel_deleteEdgesFilter_expression(self, ctx:o9IBPLParser.Rel_deleteEdgesFilter_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#TruncateMeasureGroup.
    def visitTruncateMeasureGroup(self, ctx:o9IBPLParser.TruncateMeasureGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#TruncateGraph.
    def visitTruncateGraph(self, ctx:o9IBPLParser.TruncateGraphContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#flushDataStatement.
    def visitFlushDataStatement(self, ctx:o9IBPLParser.FlushDataStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#nullifyFactStatement.
    def visitNullifyFactStatement(self, ctx:o9IBPLParser.NullifyFactStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#recurrenceScopeStatement.
    def visitRecurrenceScopeStatement(self, ctx:o9IBPLParser.RecurrenceScopeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#insertScopeStatement.
    def visitInsertScopeStatement(self, ctx:o9IBPLParser.InsertScopeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#blockScopeStatement.
    def visitBlockScopeStatement(self, ctx:o9IBPLParser.BlockScopeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#blockScopeGraphStatement.
    def visitBlockScopeGraphStatement(self, ctx:o9IBPLParser.BlockScopeGraphStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#scopeStatement.
    def visitScopeStatement(self, ctx:o9IBPLParser.ScopeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#scopePrefix.
    def visitScopePrefix(self, ctx:o9IBPLParser.ScopePrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#scopeStatementWithImpact.
    def visitScopeStatementWithImpact(self, ctx:o9IBPLParser.ScopeStatementWithImpactContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#scopedGraphEdgePropertyAssignments.
    def visitScopedGraphEdgePropertyAssignments(self, ctx:o9IBPLParser.ScopedGraphEdgePropertyAssignmentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#vertexScopeForGraphAssignmentStatement.
    def visitVertexScopeForGraphAssignmentStatement(self, ctx:o9IBPLParser.VertexScopeForGraphAssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphVersions_expression.
    def visitGraphVersions_expression(self, ctx:o9IBPLParser.GraphVersions_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#vertexScopeStatement.
    def visitVertexScopeStatement(self, ctx:o9IBPLParser.VertexScopeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#member_expressions_or_expression.
    def visitMember_expressions_or_expression(self, ctx:o9IBPLParser.Member_expressions_or_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphEdgePropertyAssignment.
    def visitGraphEdgePropertyAssignment(self, ctx:o9IBPLParser.GraphEdgePropertyAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphEdgePropertyUpdate.
    def visitGraphEdgePropertyUpdate(self, ctx:o9IBPLParser.GraphEdgePropertyUpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphEdgePropertyUpdate_coordinates.
    def visitGraphEdgePropertyUpdate_coordinates(self, ctx:o9IBPLParser.GraphEdgePropertyUpdate_coordinatesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#graphEdgePropertyUpdate_member.
    def visitGraphEdgePropertyUpdate_member(self, ctx:o9IBPLParser.GraphEdgePropertyUpdate_memberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#foreachStatement.
    def visitForeachStatement(self, ctx:o9IBPLParser.ForeachStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ifStatement.
    def visitIfStatement(self, ctx:o9IBPLParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ifStat.
    def visitIfStat(self, ctx:o9IBPLParser.IfStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#elseIfStat.
    def visitElseIfStat(self, ctx:o9IBPLParser.ElseIfStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#elseStat.
    def visitElseStat(self, ctx:o9IBPLParser.ElseStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#assignment.
    def visitAssignment(self, ctx:o9IBPLParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#edgePropertyAssignment.
    def visitEdgePropertyAssignment(self, ctx:o9IBPLParser.EdgePropertyAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#CreateSetMemberSet.
    def visitCreateSetMemberSet(self, ctx:o9IBPLParser.CreateSetMemberSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#CreateSetMemberSetCrossJoin.
    def visitCreateSetMemberSetCrossJoin(self, ctx:o9IBPLParser.CreateSetMemberSetCrossJoinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#CreateProcedure.
    def visitCreateProcedure(self, ctx:o9IBPLParser.CreateProcedureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#CreateParameterizedProcedure.
    def visitCreateParameterizedProcedure(self, ctx:o9IBPLParser.CreateParameterizedProcedureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#sequentialStatement.
    def visitSequentialStatement(self, ctx:o9IBPLParser.SequentialStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#createFunctionStatement.
    def visitCreateFunctionStatement(self, ctx:o9IBPLParser.CreateFunctionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#execScriptStatement.
    def visitExecScriptStatement(self, ctx:o9IBPLParser.ExecScriptStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#execProcedureStatement.
    def visitExecProcedureStatement(self, ctx:o9IBPLParser.ExecProcedureStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#createRelStatement.
    def visitCreateRelStatement(self, ctx:o9IBPLParser.CreateRelStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#deleteRelStatement.
    def visitDeleteRelStatement(self, ctx:o9IBPLParser.DeleteRelStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#updateRelAttrStatement.
    def visitUpdateRelAttrStatement(self, ctx:o9IBPLParser.UpdateRelAttrStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#getRelAttrStatement.
    def visitGetRelAttrStatement(self, ctx:o9IBPLParser.GetRelAttrStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#enableDisableCaeStatement.
    def visitEnableDisableCaeStatement(self, ctx:o9IBPLParser.EnableDisableCaeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#set_modifier.
    def visitSet_modifier(self, ctx:o9IBPLParser.Set_modifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#member_exprList.
    def visitMember_exprList(self, ctx:o9IBPLParser.Member_exprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#scalar_exprList.
    def visitScalar_exprList(self, ctx:o9IBPLParser.Scalar_exprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#literal_exprSet.
    def visitLiteral_exprSet(self, ctx:o9IBPLParser.Literal_exprSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#expression.
    def visitExpression(self, ctx:o9IBPLParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#null_or_scalar_exp.
    def visitNull_or_scalar_exp(self, ctx:o9IBPLParser.Null_or_scalar_expContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#scalar_expression.
    def visitScalar_expression(self, ctx:o9IBPLParser.Scalar_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#condExpr.
    def visitCondExpr(self, ctx:o9IBPLParser.CondExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#orExpr.
    def visitOrExpr(self, ctx:o9IBPLParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#andExpr.
    def visitAndExpr(self, ctx:o9IBPLParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#equExpr.
    def visitEquExpr(self, ctx:o9IBPLParser.EquExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#notEquExpr.
    def visitNotEquExpr(self, ctx:o9IBPLParser.NotEquExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#inScalarSetExpr.
    def visitInScalarSetExpr(self, ctx:o9IBPLParser.InScalarSetExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#RelExprNumeric.
    def visitRelExprNumeric(self, ctx:o9IBPLParser.RelExprNumericContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#RelExprString.
    def visitRelExprString(self, ctx:o9IBPLParser.RelExprStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#addExpr.
    def visitAddExpr(self, ctx:o9IBPLParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#subExpr.
    def visitSubExpr(self, ctx:o9IBPLParser.SubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#mulExpr.
    def visitMulExpr(self, ctx:o9IBPLParser.MulExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#divExpr.
    def visitDivExpr(self, ctx:o9IBPLParser.DivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#modExpr.
    def visitModExpr(self, ctx:o9IBPLParser.ModExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#powExpr.
    def visitPowExpr(self, ctx:o9IBPLParser.PowExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#unaryExpr.
    def visitUnaryExpr(self, ctx:o9IBPLParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueScalar.
    def visitValueScalar(self, ctx:o9IBPLParser.ValueScalarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueLiteral.
    def visitValueLiteral(self, ctx:o9IBPLParser.ValueLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueNamedMember.
    def visitValueNamedMember(self, ctx:o9IBPLParser.ValueNamedMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueMemberProperty.
    def visitValueMemberProperty(self, ctx:o9IBPLParser.ValueMemberPropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueMeasureProperty.
    def visitValueMeasureProperty(self, ctx:o9IBPLParser.ValueMeasurePropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueMeasure.
    def visitValueMeasure(self, ctx:o9IBPLParser.ValueMeasureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueTupleComputedAggregateMeasure.
    def visitValueTupleComputedAggregateMeasure(self, ctx:o9IBPLParser.ValueTupleComputedAggregateMeasureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueFullyQualifiedEdgeProperty.
    def visitValueFullyQualifiedEdgeProperty(self, ctx:o9IBPLParser.ValueFullyQualifiedEdgePropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueEdgeProperty.
    def visitValueEdgeProperty(self, ctx:o9IBPLParser.ValueEdgePropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueFullyQualifiedEdgePropertyWithVertexCoordinates.
    def visitValueFullyQualifiedEdgePropertyWithVertexCoordinates(self, ctx:o9IBPLParser.ValueFullyQualifiedEdgePropertyWithVertexCoordinatesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueEdgeNodeMemberProperty.
    def visitValueEdgeNodeMemberProperty(self, ctx:o9IBPLParser.ValueEdgeNodeMemberPropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueNodeMemberProperty.
    def visitValueNodeMemberProperty(self, ctx:o9IBPLParser.ValueNodeMemberPropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueId.
    def visitValueId(self, ctx:o9IBPLParser.ValueIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#ValueLiteralSet.
    def visitValueLiteralSet(self, ctx:o9IBPLParser.ValueLiteralSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralNumber.
    def visitLiteralNumber(self, ctx:o9IBPLParser.LiteralNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralBool.
    def visitLiteralBool(self, ctx:o9IBPLParser.LiteralBoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralNull.
    def visitLiteralNull(self, ctx:o9IBPLParser.LiteralNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralDateNow.
    def visitLiteralDateNow(self, ctx:o9IBPLParser.LiteralDateNowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralLastCommitTime.
    def visitLiteralLastCommitTime(self, ctx:o9IBPLParser.LiteralLastCommitTimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralLastUpdateTime.
    def visitLiteralLastUpdateTime(self, ctx:o9IBPLParser.LiteralLastUpdateTimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralToDateTime.
    def visitLiteralToDateTime(self, ctx:o9IBPLParser.LiteralToDateTimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralDateAdd.
    def visitLiteralDateAdd(self, ctx:o9IBPLParser.LiteralDateAddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralDateDiff.
    def visitLiteralDateDiff(self, ctx:o9IBPLParser.LiteralDateDiffContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralNextCount.
    def visitLiteralNextCount(self, ctx:o9IBPLParser.LiteralNextCountContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralNextLabel.
    def visitLiteralNextLabel(self, ctx:o9IBPLParser.LiteralNextLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralAbs.
    def visitLiteralAbs(self, ctx:o9IBPLParser.LiteralAbsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralCeiling.
    def visitLiteralCeiling(self, ctx:o9IBPLParser.LiteralCeilingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralDiv.
    def visitLiteralDiv(self, ctx:o9IBPLParser.LiteralDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralFloor.
    def visitLiteralFloor(self, ctx:o9IBPLParser.LiteralFloorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralFloat.
    def visitLiteralFloat(self, ctx:o9IBPLParser.LiteralFloatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralInteger.
    def visitLiteralInteger(self, ctx:o9IBPLParser.LiteralIntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralToString.
    def visitLiteralToString(self, ctx:o9IBPLParser.LiteralToStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralUpper.
    def visitLiteralUpper(self, ctx:o9IBPLParser.LiteralUpperContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralLower.
    def visitLiteralLower(self, ctx:o9IBPLParser.LiteralLowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralLog.
    def visitLiteralLog(self, ctx:o9IBPLParser.LiteralLogContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralExponential.
    def visitLiteralExponential(self, ctx:o9IBPLParser.LiteralExponentialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralPow.
    def visitLiteralPow(self, ctx:o9IBPLParser.LiteralPowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralRandom.
    def visitLiteralRandom(self, ctx:o9IBPLParser.LiteralRandomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralRound.
    def visitLiteralRound(self, ctx:o9IBPLParser.LiteralRoundContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralSum.
    def visitLiteralSum(self, ctx:o9IBPLParser.LiteralSumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralSumProduct.
    def visitLiteralSumProduct(self, ctx:o9IBPLParser.LiteralSumProductContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralAvg.
    def visitLiteralAvg(self, ctx:o9IBPLParser.LiteralAvgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralAvgWithNulls.
    def visitLiteralAvgWithNulls(self, ctx:o9IBPLParser.LiteralAvgWithNullsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralCorrel.
    def visitLiteralCorrel(self, ctx:o9IBPLParser.LiteralCorrelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralCount.
    def visitLiteralCount(self, ctx:o9IBPLParser.LiteralCountContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralMin.
    def visitLiteralMin(self, ctx:o9IBPLParser.LiteralMinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralMax.
    def visitLiteralMax(self, ctx:o9IBPLParser.LiteralMaxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralConcat.
    def visitLiteralConcat(self, ctx:o9IBPLParser.LiteralConcatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralLength.
    def visitLiteralLength(self, ctx:o9IBPLParser.LiteralLengthContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralLen.
    def visitLiteralLen(self, ctx:o9IBPLParser.LiteralLenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralLeft.
    def visitLiteralLeft(self, ctx:o9IBPLParser.LiteralLeftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralRight.
    def visitLiteralRight(self, ctx:o9IBPLParser.LiteralRightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralMid.
    def visitLiteralMid(self, ctx:o9IBPLParser.LiteralMidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralCoalesce.
    def visitLiteralCoalesce(self, ctx:o9IBPLParser.LiteralCoalesceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralIfThen.
    def visitLiteralIfThen(self, ctx:o9IBPLParser.LiteralIfThenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralMemberCount.
    def visitLiteralMemberCount(self, ctx:o9IBPLParser.LiteralMemberCountContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralMemberIndex.
    def visitLiteralMemberIndex(self, ctx:o9IBPLParser.LiteralMemberIndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralGetValue.
    def visitLiteralGetValue(self, ctx:o9IBPLParser.LiteralGetValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralARGB.
    def visitLiteralARGB(self, ctx:o9IBPLParser.LiteralARGBContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralIsNull.
    def visitLiteralIsNull(self, ctx:o9IBPLParser.LiteralIsNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralIsEmpty.
    def visitLiteralIsEmpty(self, ctx:o9IBPLParser.LiteralIsEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralIsWhiteSpace.
    def visitLiteralIsWhiteSpace(self, ctx:o9IBPLParser.LiteralIsWhiteSpaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralSafeDivide.
    def visitLiteralSafeDivide(self, ctx:o9IBPLParser.LiteralSafeDivideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#LiteralSubString.
    def visitLiteralSubString(self, ctx:o9IBPLParser.LiteralSubStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#distinct.
    def visitDistinct(self, ctx:o9IBPLParser.DistinctContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#member_measure_crossjoin.
    def visitMember_measure_crossjoin(self, ctx:o9IBPLParser.Member_measure_crossjoinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#CrossJoinMembers.
    def visitCrossJoinMembers(self, ctx:o9IBPLParser.CrossJoinMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#CrossJoinMember.
    def visitCrossJoinMember(self, ctx:o9IBPLParser.CrossJoinMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#CrossJoinGraphNode.
    def visitCrossJoinGraphNode(self, ctx:o9IBPLParser.CrossJoinGraphNodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#CrossJoinMeasure.
    def visitCrossJoinMeasure(self, ctx:o9IBPLParser.CrossJoinMeasureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#NamedNodeReference.
    def visitNamedNodeReference(self, ctx:o9IBPLParser.NamedNodeReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#NamedNodeFilterSetReference.
    def visitNamedNodeFilterSetReference(self, ctx:o9IBPLParser.NamedNodeFilterSetReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#NamedNodeGraphReference.
    def visitNamedNodeGraphReference(self, ctx:o9IBPLParser.NamedNodeGraphReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#NamedNodeFilterSetGraphReference.
    def visitNamedNodeFilterSetGraphReference(self, ctx:o9IBPLParser.NamedNodeFilterSetGraphReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#multifilter_clause.
    def visitMultifilter_clause(self, ctx:o9IBPLParser.Multifilter_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#namedNode_Filter_clause.
    def visitNamedNode_Filter_clause(self, ctx:o9IBPLParser.NamedNode_Filter_clauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#member_crossjoin.
    def visitMember_crossjoin(self, ctx:o9IBPLParser.Member_crossjoinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberMeta.
    def visitMemberMeta(self, ctx:o9IBPLParser.MemberMetaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberPrevMember.
    def visitMemberPrevMember(self, ctx:o9IBPLParser.MemberPrevMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberDescendantsAtLevel.
    def visitMemberDescendantsAtLevel(self, ctx:o9IBPLParser.MemberDescendantsAtLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberFind.
    def visitMemberFind(self, ctx:o9IBPLParser.MemberFindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberLeadOffset.
    def visitMemberLeadOffset(self, ctx:o9IBPLParser.MemberLeadOffsetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberCurrentUser.
    def visitMemberCurrentUser(self, ctx:o9IBPLParser.MemberCurrentUserContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberAncestorsAtLevel.
    def visitMemberAncestorsAtLevel(self, ctx:o9IBPLParser.MemberAncestorsAtLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberFirstOrDefault.
    def visitMemberFirstOrDefault(self, ctx:o9IBPLParser.MemberFirstOrDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberFirstElement.
    def visitMemberFirstElement(self, ctx:o9IBPLParser.MemberFirstElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberChildren.
    def visitMemberChildren(self, ctx:o9IBPLParser.MemberChildrenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberNextMember.
    def visitMemberNextMember(self, ctx:o9IBPLParser.MemberNextMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberDifference.
    def visitMemberDifference(self, ctx:o9IBPLParser.MemberDifferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberIntersect.
    def visitMemberIntersect(self, ctx:o9IBPLParser.MemberIntersectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberList.
    def visitMemberList(self, ctx:o9IBPLParser.MemberListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#CurrentVertexCoordinateMember.
    def visitCurrentVertexCoordinateMember(self, ctx:o9IBPLParser.CurrentVertexCoordinateMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberOrderBy.
    def visitMemberOrderBy(self, ctx:o9IBPLParser.MemberOrderByContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberUnion.
    def visitMemberUnion(self, ctx:o9IBPLParser.MemberUnionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberRelatedMembers.
    def visitMemberRelatedMembers(self, ctx:o9IBPLParser.MemberRelatedMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberFindWithKey.
    def visitMemberFindWithKey(self, ctx:o9IBPLParser.MemberFindWithKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberAncestors.
    def visitMemberAncestors(self, ctx:o9IBPLParser.MemberAncestorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberUnoperatedSet.
    def visitMemberUnoperatedSet(self, ctx:o9IBPLParser.MemberUnoperatedSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberLastElement.
    def visitMemberLastElement(self, ctx:o9IBPLParser.MemberLastElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberAncestor.
    def visitMemberAncestor(self, ctx:o9IBPLParser.MemberAncestorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberLevelAttribute.
    def visitMemberLevelAttribute(self, ctx:o9IBPLParser.MemberLevelAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberUnoperated.
    def visitMemberUnoperated(self, ctx:o9IBPLParser.MemberUnoperatedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberFilter.
    def visitMemberFilter(self, ctx:o9IBPLParser.MemberFilterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberElement.
    def visitMemberElement(self, ctx:o9IBPLParser.MemberElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberBetween.
    def visitMemberBetween(self, ctx:o9IBPLParser.MemberBetweenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#unoperated_member.
    def visitUnoperated_member(self, ctx:o9IBPLParser.Unoperated_memberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#current_vertex_coordinate_member.
    def visitCurrent_vertex_coordinate_member(self, ctx:o9IBPLParser.Current_vertex_coordinate_memberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberSetReference.
    def visitMemberSetReference(self, ctx:o9IBPLParser.MemberSetReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#MemberArgument.
    def visitMemberArgument(self, ctx:o9IBPLParser.MemberArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#HierarchyLeafMembers.
    def visitHierarchyLeafMembers(self, ctx:o9IBPLParser.HierarchyLeafMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#HierarchyMembers.
    def visitHierarchyMembers(self, ctx:o9IBPLParser.HierarchyMembersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#AttributeMemberSet.
    def visitAttributeMemberSet(self, ctx:o9IBPLParser.AttributeMemberSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#AttributeMemberSetFromGraphNode.
    def visitAttributeMemberSetFromGraphNode(self, ctx:o9IBPLParser.AttributeMemberSetFromGraphNodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#current_member_expression.
    def visitCurrent_member_expression(self, ctx:o9IBPLParser.Current_member_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#named_member_expression.
    def visitNamed_member_expression(self, ctx:o9IBPLParser.Named_member_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#member_property.
    def visitMember_property(self, ctx:o9IBPLParser.Member_propertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#meta_element.
    def visitMeta_element(self, ctx:o9IBPLParser.Meta_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#meta_member_property.
    def visitMeta_member_property(self, ctx:o9IBPLParser.Meta_member_propertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#metaMemberIn.
    def visitMetaMemberIn(self, ctx:o9IBPLParser.MetaMemberInContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#metaMember.
    def visitMetaMember(self, ctx:o9IBPLParser.MetaMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#dimension.
    def visitDimension(self, ctx:o9IBPLParser.DimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#dimensionSet.
    def visitDimensionSet(self, ctx:o9IBPLParser.DimensionSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#dimensionList.
    def visitDimensionList(self, ctx:o9IBPLParser.DimensionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#dimension_name.
    def visitDimension_name(self, ctx:o9IBPLParser.Dimension_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#dimension_expression.
    def visitDimension_expression(self, ctx:o9IBPLParser.Dimension_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#hierarchy.
    def visitHierarchy(self, ctx:o9IBPLParser.HierarchyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#levelattribute.
    def visitLevelattribute(self, ctx:o9IBPLParser.LevelattributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#levelattribute_name.
    def visitLevelattribute_name(self, ctx:o9IBPLParser.Levelattribute_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#levelattribute_expression.
    def visitLevelattribute_expression(self, ctx:o9IBPLParser.Levelattribute_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#meta_levelattribute_name.
    def visitMeta_levelattribute_name(self, ctx:o9IBPLParser.Meta_levelattribute_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#plan_name.
    def visitPlan_name(self, ctx:o9IBPLParser.Plan_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measure_group_name.
    def visitMeasure_group_name(self, ctx:o9IBPLParser.Measure_group_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#unqualified_measure_name.
    def visitUnqualified_measure_name(self, ctx:o9IBPLParser.Unqualified_measure_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measure_element_list.
    def visitMeasure_element_list(self, ctx:o9IBPLParser.Measure_element_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measure_element.
    def visitMeasure_element(self, ctx:o9IBPLParser.Measure_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#simple_measure_element.
    def visitSimple_measure_element(self, ctx:o9IBPLParser.Simple_measure_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measure.
    def visitMeasure(self, ctx:o9IBPLParser.MeasureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measure_name.
    def visitMeasure_name(self, ctx:o9IBPLParser.Measure_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#transient_measure_name.
    def visitTransient_measure_name(self, ctx:o9IBPLParser.Transient_measure_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#computed_plugin_measure.
    def visitComputed_plugin_measure(self, ctx:o9IBPLParser.Computed_plugin_measureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#usingArgsScopeClause.
    def visitUsingArgsScopeClause(self, ctx:o9IBPLParser.UsingArgsScopeClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#CumulativeMeasure.
    def visitCumulativeMeasure(self, ctx:o9IBPLParser.CumulativeMeasureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#transient_computed_measure.
    def visitTransient_computed_measure(self, ctx:o9IBPLParser.Transient_computed_measureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#tuple_aggregate_measure.
    def visitTuple_aggregate_measure(self, ctx:o9IBPLParser.Tuple_aggregate_measureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#tuple_agg_measure_crossjoin.
    def visitTuple_agg_measure_crossjoin(self, ctx:o9IBPLParser.Tuple_agg_measure_crossjoinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#tuple_computed_aggregate_measure.
    def visitTuple_computed_aggregate_measure(self, ctx:o9IBPLParser.Tuple_computed_aggregate_measureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measure_with_scope_or_graph_coordinates.
    def visitMeasure_with_scope_or_graph_coordinates(self, ctx:o9IBPLParser.Measure_with_scope_or_graph_coordinatesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#vertex_coordinate.
    def visitVertex_coordinate(self, ctx:o9IBPLParser.Vertex_coordinateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#vertex_coordinate_target.
    def visitVertex_coordinate_target(self, ctx:o9IBPLParser.Vertex_coordinate_targetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#namenode_expression.
    def visitNamenode_expression(self, ctx:o9IBPLParser.Namenode_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#measure_property.
    def visitMeasure_property(self, ctx:o9IBPLParser.Measure_propertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#cell_properties.
    def visitCell_properties(self, ctx:o9IBPLParser.Cell_propertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#node_properties.
    def visitNode_properties(self, ctx:o9IBPLParser.Node_propertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#tuple_aggregation_meas_func.
    def visitTuple_aggregation_meas_func(self, ctx:o9IBPLParser.Tuple_aggregation_meas_funcContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#String.
    def visitString(self, ctx:o9IBPLParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#Argument.
    def visitArgument(self, ctx:o9IBPLParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#QuotedId.
    def visitQuotedId(self, ctx:o9IBPLParser.QuotedIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#Id.
    def visitId(self, ctx:o9IBPLParser.IdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#PositiveInt.
    def visitPositiveInt(self, ctx:o9IBPLParser.PositiveIntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#NegInteger.
    def visitNegInteger(self, ctx:o9IBPLParser.NegIntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#Integer.
    def visitInteger(self, ctx:o9IBPLParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#NegDecimal.
    def visitNegDecimal(self, ctx:o9IBPLParser.NegDecimalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#Decimal.
    def visitDecimal(self, ctx:o9IBPLParser.DecimalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#TrueBool.
    def visitTrueBool(self, ctx:o9IBPLParser.TrueBoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by o9IBPLParser#FalseBool.
    def visitFalseBool(self, ctx:o9IBPLParser.FalseBoolContext):
        return self.visitChildren(ctx)



del o9IBPLParser