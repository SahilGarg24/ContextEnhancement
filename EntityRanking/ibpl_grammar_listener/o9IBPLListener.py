# Generated from C:/Users/sahil.garg/PycharmProjects/Performance_Analyzer/ibpl_grammar_listener/o9IBPL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .o9IBPLParser import o9IBPLParser
else:
    from .o9IBPLParser import o9IBPLParser

# This class defines a complete listener for a parse tree produced by o9IBPLParser.
class o9IBPLListener(ParseTreeListener):

    # Enter a parse tree produced by o9IBPLParser#block.
    def enterBlock(self, ctx:o9IBPLParser.BlockContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#block.
    def exitBlock(self, ctx:o9IBPLParser.BlockContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#statement.
    def enterStatement(self, ctx:o9IBPLParser.StatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#statement.
    def exitStatement(self, ctx:o9IBPLParser.StatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#execExternalStatement.
    def enterExecExternalStatement(self, ctx:o9IBPLParser.ExecExternalStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#execExternalStatement.
    def exitExecExternalStatement(self, ctx:o9IBPLParser.ExecExternalStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#haRedisPassThroughStatement.
    def enterHaRedisPassThroughStatement(self, ctx:o9IBPLParser.HaRedisPassThroughStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#haRedisPassThroughStatement.
    def exitHaRedisPassThroughStatement(self, ctx:o9IBPLParser.HaRedisPassThroughStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#replayStatement.
    def enterReplayStatement(self, ctx:o9IBPLParser.ReplayStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#replayStatement.
    def exitReplayStatement(self, ctx:o9IBPLParser.ReplayStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#batchStartStatement.
    def enterBatchStartStatement(self, ctx:o9IBPLParser.BatchStartStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#batchStartStatement.
    def exitBatchStartStatement(self, ctx:o9IBPLParser.BatchStartStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#batchEndStatement.
    def enterBatchEndStatement(self, ctx:o9IBPLParser.BatchEndStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#batchEndStatement.
    def exitBatchEndStatement(self, ctx:o9IBPLParser.BatchEndStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ddlStatement.
    def enterDdlStatement(self, ctx:o9IBPLParser.DdlStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ddlStatement.
    def exitDdlStatement(self, ctx:o9IBPLParser.DdlStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#dmlStatement.
    def enterDmlStatement(self, ctx:o9IBPLParser.DmlStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#dmlStatement.
    def exitDmlStatement(self, ctx:o9IBPLParser.DmlStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#json.
    def enterJson(self, ctx:o9IBPLParser.JsonContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#json.
    def exitJson(self, ctx:o9IBPLParser.JsonContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#jsonObject.
    def enterJsonObject(self, ctx:o9IBPLParser.JsonObjectContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#jsonObject.
    def exitJsonObject(self, ctx:o9IBPLParser.JsonObjectContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#jsonPair.
    def enterJsonPair(self, ctx:o9IBPLParser.JsonPairContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#jsonPair.
    def exitJsonPair(self, ctx:o9IBPLParser.JsonPairContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#jsonArray.
    def enterJsonArray(self, ctx:o9IBPLParser.JsonArrayContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#jsonArray.
    def exitJsonArray(self, ctx:o9IBPLParser.JsonArrayContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#jsonValue.
    def enterJsonValue(self, ctx:o9IBPLParser.JsonValueContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#jsonValue.
    def exitJsonValue(self, ctx:o9IBPLParser.JsonValueContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#jsonstring.
    def enterJsonstring(self, ctx:o9IBPLParser.JsonstringContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#jsonstring.
    def exitJsonstring(self, ctx:o9IBPLParser.JsonstringContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#jsonnumber.
    def enterJsonnumber(self, ctx:o9IBPLParser.JsonnumberContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#jsonnumber.
    def exitJsonnumber(self, ctx:o9IBPLParser.JsonnumberContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#garbageCollectStatement.
    def enterGarbageCollectStatement(self, ctx:o9IBPLParser.GarbageCollectStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#garbageCollectStatement.
    def exitGarbageCollectStatement(self, ctx:o9IBPLParser.GarbageCollectStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#registerAlertStatement.
    def enterRegisterAlertStatement(self, ctx:o9IBPLParser.RegisterAlertStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#registerAlertStatement.
    def exitRegisterAlertStatement(self, ctx:o9IBPLParser.RegisterAlertStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#deregisterAlertStatement.
    def enterDeregisterAlertStatement(self, ctx:o9IBPLParser.DeregisterAlertStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#deregisterAlertStatement.
    def exitDeregisterAlertStatement(self, ctx:o9IBPLParser.DeregisterAlertStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#from_tail.
    def enterFrom_tail(self, ctx:o9IBPLParser.From_tailContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#from_tail.
    def exitFrom_tail(self, ctx:o9IBPLParser.From_tailContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#to_head.
    def enterTo_head(self, ctx:o9IBPLParser.To_headContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#to_head.
    def exitTo_head(self, ctx:o9IBPLParser.To_headContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edgeDirection.
    def enterEdgeDirection(self, ctx:o9IBPLParser.EdgeDirectionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edgeDirection.
    def exitEdgeDirection(self, ctx:o9IBPLParser.EdgeDirectionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#traverseDirection.
    def enterTraverseDirection(self, ctx:o9IBPLParser.TraverseDirectionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#traverseDirection.
    def exitTraverseDirection(self, ctx:o9IBPLParser.TraverseDirectionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#traverseDistance.
    def enterTraverseDistance(self, ctx:o9IBPLParser.TraverseDistanceContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#traverseDistance.
    def exitTraverseDistance(self, ctx:o9IBPLParser.TraverseDistanceContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphNameOrIdentfier.
    def enterGraphNameOrIdentfier(self, ctx:o9IBPLParser.GraphNameOrIdentfierContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphNameOrIdentfier.
    def exitGraphNameOrIdentfier(self, ctx:o9IBPLParser.GraphNameOrIdentfierContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graph_identifier.
    def enterGraph_identifier(self, ctx:o9IBPLParser.Graph_identifierContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graph_identifier.
    def exitGraph_identifier(self, ctx:o9IBPLParser.Graph_identifierContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphName.
    def enterGraphName(self, ctx:o9IBPLParser.GraphNameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphName.
    def exitGraphName(self, ctx:o9IBPLParser.GraphNameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edge_property.
    def enterEdge_property(self, ctx:o9IBPLParser.Edge_propertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edge_property.
    def exitEdge_property(self, ctx:o9IBPLParser.Edge_propertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edgePropertyName.
    def enterEdgePropertyName(self, ctx:o9IBPLParser.EdgePropertyNameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edgePropertyName.
    def exitEdgePropertyName(self, ctx:o9IBPLParser.EdgePropertyNameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#nameSpace.
    def enterNameSpace(self, ctx:o9IBPLParser.NameSpaceContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#nameSpace.
    def exitNameSpace(self, ctx:o9IBPLParser.NameSpaceContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#fully_qualified_edge_property.
    def enterFully_qualified_edge_property(self, ctx:o9IBPLParser.Fully_qualified_edge_propertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#fully_qualified_edge_property.
    def exitFully_qualified_edge_property(self, ctx:o9IBPLParser.Fully_qualified_edge_propertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#fully_qualified_edge_property_with_vertex_coordinates.
    def enterFully_qualified_edge_property_with_vertex_coordinates(self, ctx:o9IBPLParser.Fully_qualified_edge_property_with_vertex_coordinatesContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#fully_qualified_edge_property_with_vertex_coordinates.
    def exitFully_qualified_edge_property_with_vertex_coordinates(self, ctx:o9IBPLParser.Fully_qualified_edge_property_with_vertex_coordinatesContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edge_node_member_property.
    def enterEdge_node_member_property(self, ctx:o9IBPLParser.Edge_node_member_propertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edge_node_member_property.
    def exitEdge_node_member_property(self, ctx:o9IBPLParser.Edge_node_member_propertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#node_member_property.
    def enterNode_member_property(self, ctx:o9IBPLParser.Node_member_propertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#node_member_property.
    def exitNode_member_property(self, ctx:o9IBPLParser.Node_member_propertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#nameValue.
    def enterNameValue(self, ctx:o9IBPLParser.NameValueContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#nameValue.
    def exitNameValue(self, ctx:o9IBPLParser.NameValueContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#genericNameValue.
    def enterGenericNameValue(self, ctx:o9IBPLParser.GenericNameValueContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#genericNameValue.
    def exitGenericNameValue(self, ctx:o9IBPLParser.GenericNameValueContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edgePredicate_expression.
    def enterEdgePredicate_expression(self, ctx:o9IBPLParser.EdgePredicate_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edgePredicate_expression.
    def exitEdgePredicate_expression(self, ctx:o9IBPLParser.EdgePredicate_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#vertexPredicate_expression.
    def enterVertexPredicate_expression(self, ctx:o9IBPLParser.VertexPredicate_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#vertexPredicate_expression.
    def exitVertexPredicate_expression(self, ctx:o9IBPLParser.VertexPredicate_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphLevelAttributeName.
    def enterGraphLevelAttributeName(self, ctx:o9IBPLParser.GraphLevelAttributeNameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphLevelAttributeName.
    def exitGraphLevelAttributeName(self, ctx:o9IBPLParser.GraphLevelAttributeNameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphVersion_expression.
    def enterGraphVersion_expression(self, ctx:o9IBPLParser.GraphVersion_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphVersion_expression.
    def exitGraphVersion_expression(self, ctx:o9IBPLParser.GraphVersion_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#updateGraphStatement.
    def enterUpdateGraphStatement(self, ctx:o9IBPLParser.UpdateGraphStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#updateGraphStatement.
    def exitUpdateGraphStatement(self, ctx:o9IBPLParser.UpdateGraphStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#EdgeCreate.
    def enterEdgeCreate(self, ctx:o9IBPLParser.EdgeCreateContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#EdgeCreate.
    def exitEdgeCreate(self, ctx:o9IBPLParser.EdgeCreateContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#EdgeModify.
    def enterEdgeModify(self, ctx:o9IBPLParser.EdgeModifyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#EdgeModify.
    def exitEdgeModify(self, ctx:o9IBPLParser.EdgeModifyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#EdgeDelete.
    def enterEdgeDelete(self, ctx:o9IBPLParser.EdgeDeleteContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#EdgeDelete.
    def exitEdgeDelete(self, ctx:o9IBPLParser.EdgeDeleteContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphNodePairClause.
    def enterGraphNodePairClause(self, ctx:o9IBPLParser.GraphNodePairClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphNodePairClause.
    def exitGraphNodePairClause(self, ctx:o9IBPLParser.GraphNodePairClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphNodeClause.
    def enterGraphNodeClause(self, ctx:o9IBPLParser.GraphNodeClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphNodeClause.
    def exitGraphNodeClause(self, ctx:o9IBPLParser.GraphNodeClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphMemberNode.
    def enterGraphMemberNode(self, ctx:o9IBPLParser.GraphMemberNodeContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphMemberNode.
    def exitGraphMemberNode(self, ctx:o9IBPLParser.GraphMemberNodeContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edgePropertiesClause.
    def enterEdgePropertiesClause(self, ctx:o9IBPLParser.EdgePropertiesClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edgePropertiesClause.
    def exitEdgePropertiesClause(self, ctx:o9IBPLParser.EdgePropertiesClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#VertexSetName.
    def enterVertexSetName(self, ctx:o9IBPLParser.VertexSetNameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#VertexSetName.
    def exitVertexSetName(self, ctx:o9IBPLParser.VertexSetNameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#VertexSetExpr.
    def enterVertexSetExpr(self, ctx:o9IBPLParser.VertexSetExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#VertexSetExpr.
    def exitVertexSetExpr(self, ctx:o9IBPLParser.VertexSetExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#VertexSetFromMemberSets.
    def enterVertexSetFromMemberSets(self, ctx:o9IBPLParser.VertexSetFromMemberSetsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#VertexSetFromMemberSets.
    def exitVertexSetFromMemberSets(self, ctx:o9IBPLParser.VertexSetFromMemberSetsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#VertexSetFromMemberSet.
    def enterVertexSetFromMemberSet(self, ctx:o9IBPLParser.VertexSetFromMemberSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#VertexSetFromMemberSet.
    def exitVertexSetFromMemberSet(self, ctx:o9IBPLParser.VertexSetFromMemberSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#SubGraphName.
    def enterSubGraphName(self, ctx:o9IBPLParser.SubGraphNameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#SubGraphName.
    def exitSubGraphName(self, ctx:o9IBPLParser.SubGraphNameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#SubGraphExpr.
    def enterSubGraphExpr(self, ctx:o9IBPLParser.SubGraphExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#SubGraphExpr.
    def exitSubGraphExpr(self, ctx:o9IBPLParser.SubGraphExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#subGraphVertexSet_expression.
    def enterSubGraphVertexSet_expression(self, ctx:o9IBPLParser.SubGraphVertexSet_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#subGraphVertexSet_expression.
    def exitSubGraphVertexSet_expression(self, ctx:o9IBPLParser.SubGraphVertexSet_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#TraverseGraphName.
    def enterTraverseGraphName(self, ctx:o9IBPLParser.TraverseGraphNameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#TraverseGraphName.
    def exitTraverseGraphName(self, ctx:o9IBPLParser.TraverseGraphNameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#TraverseGraphExp.
    def enterTraverseGraphExp(self, ctx:o9IBPLParser.TraverseGraphExpContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#TraverseGraphExp.
    def exitTraverseGraphExp(self, ctx:o9IBPLParser.TraverseGraphExpContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edgeSet_expression.
    def enterEdgeSet_expression(self, ctx:o9IBPLParser.EdgeSet_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edgeSet_expression.
    def exitEdgeSet_expression(self, ctx:o9IBPLParser.EdgeSet_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphNodeMembersStatement.
    def enterGraphNodeMembersStatement(self, ctx:o9IBPLParser.GraphNodeMembersStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphNodeMembersStatement.
    def exitGraphNodeMembersStatement(self, ctx:o9IBPLParser.GraphNodeMembersStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#selectGraphEdgeProjectStatement.
    def enterSelectGraphEdgeProjectStatement(self, ctx:o9IBPLParser.SelectGraphEdgeProjectStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#selectGraphEdgeProjectStatement.
    def exitSelectGraphEdgeProjectStatement(self, ctx:o9IBPLParser.SelectGraphEdgeProjectStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edgeProjectPredicate_expression.
    def enterEdgeProjectPredicate_expression(self, ctx:o9IBPLParser.EdgeProjectPredicate_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edgeProjectPredicate_expression.
    def exitEdgeProjectPredicate_expression(self, ctx:o9IBPLParser.EdgeProjectPredicate_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#selectGraphEdgesStatement.
    def enterSelectGraphEdgesStatement(self, ctx:o9IBPLParser.SelectGraphEdgesStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#selectGraphEdgesStatement.
    def exitSelectGraphEdgesStatement(self, ctx:o9IBPLParser.SelectGraphEdgesStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edge_crossjoin.
    def enterEdge_crossjoin(self, ctx:o9IBPLParser.Edge_crossjoinContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edge_crossjoin.
    def exitEdge_crossjoin(self, ctx:o9IBPLParser.Edge_crossjoinContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edge_crossjoin_element.
    def enterEdge_crossjoin_element(self, ctx:o9IBPLParser.Edge_crossjoin_elementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edge_crossjoin_element.
    def exitEdge_crossjoin_element(self, ctx:o9IBPLParser.Edge_crossjoin_elementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graph_traversal_options.
    def enterGraph_traversal_options(self, ctx:o9IBPLParser.Graph_traversal_optionsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graph_traversal_options.
    def exitGraph_traversal_options(self, ctx:o9IBPLParser.Graph_traversal_optionsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graph_traversal_start_set.
    def enterGraph_traversal_start_set(self, ctx:o9IBPLParser.Graph_traversal_start_setContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graph_traversal_start_set.
    def exitGraph_traversal_start_set(self, ctx:o9IBPLParser.Graph_traversal_start_setContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graph_filter_set.
    def enterGraph_filter_set(self, ctx:o9IBPLParser.Graph_filter_setContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graph_filter_set.
    def exitGraph_filter_set(self, ctx:o9IBPLParser.Graph_filter_setContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graph_filter_element.
    def enterGraph_filter_element(self, ctx:o9IBPLParser.Graph_filter_elementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graph_filter_element.
    def exitGraph_filter_element(self, ctx:o9IBPLParser.Graph_filter_elementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#rel_edgePredicate_expression.
    def enterRel_edgePredicate_expression(self, ctx:o9IBPLParser.Rel_edgePredicate_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#rel_edgePredicate_expression.
    def exitRel_edgePredicate_expression(self, ctx:o9IBPLParser.Rel_edgePredicate_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#selectGraphPathsStatement.
    def enterSelectGraphPathsStatement(self, ctx:o9IBPLParser.SelectGraphPathsStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#selectGraphPathsStatement.
    def exitSelectGraphPathsStatement(self, ctx:o9IBPLParser.SelectGraphPathsStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graph_path_filter_set.
    def enterGraph_path_filter_set(self, ctx:o9IBPLParser.Graph_path_filter_setContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graph_path_filter_set.
    def exitGraph_path_filter_set(self, ctx:o9IBPLParser.Graph_path_filter_setContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graph_path_filter_element.
    def enterGraph_path_filter_element(self, ctx:o9IBPLParser.Graph_path_filter_elementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graph_path_filter_element.
    def exitGraph_path_filter_element(self, ctx:o9IBPLParser.Graph_path_filter_elementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#selectDimensionGraphEdgesStatement.
    def enterSelectDimensionGraphEdgesStatement(self, ctx:o9IBPLParser.SelectDimensionGraphEdgesStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#selectDimensionGraphEdgesStatement.
    def exitSelectDimensionGraphEdgesStatement(self, ctx:o9IBPLParser.SelectDimensionGraphEdgesStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#dimgraph_where_clause.
    def enterDimgraph_where_clause(self, ctx:o9IBPLParser.Dimgraph_where_clauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#dimgraph_where_clause.
    def exitDimgraph_where_clause(self, ctx:o9IBPLParser.Dimgraph_where_clauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#blockStatement.
    def enterBlockStatement(self, ctx:o9IBPLParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#blockStatement.
    def exitBlockStatement(self, ctx:o9IBPLParser.BlockStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#execParallelStatement.
    def enterExecParallelStatement(self, ctx:o9IBPLParser.ExecParallelStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#execParallelStatement.
    def exitExecParallelStatement(self, ctx:o9IBPLParser.ExecParallelStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#denyAccessStatement.
    def enterDenyAccessStatement(self, ctx:o9IBPLParser.DenyAccessStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#denyAccessStatement.
    def exitDenyAccessStatement(self, ctx:o9IBPLParser.DenyAccessStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#DenyDimensionReadAccessAtMemberSet.
    def enterDenyDimensionReadAccessAtMemberSet(self, ctx:o9IBPLParser.DenyDimensionReadAccessAtMemberSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#DenyDimensionReadAccessAtMemberSet.
    def exitDenyDimensionReadAccessAtMemberSet(self, ctx:o9IBPLParser.DenyDimensionReadAccessAtMemberSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#DenyDimensionReadAccessAtDimension.
    def enterDenyDimensionReadAccessAtDimension(self, ctx:o9IBPLParser.DenyDimensionReadAccessAtDimensionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#DenyDimensionReadAccessAtDimension.
    def exitDenyDimensionReadAccessAtDimension(self, ctx:o9IBPLParser.DenyDimensionReadAccessAtDimensionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#DenyDimensionReadAccessAtAttribute.
    def enterDenyDimensionReadAccessAtAttribute(self, ctx:o9IBPLParser.DenyDimensionReadAccessAtAttributeContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#DenyDimensionReadAccessAtAttribute.
    def exitDenyDimensionReadAccessAtAttribute(self, ctx:o9IBPLParser.DenyDimensionReadAccessAtAttributeContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#denyReadPrefixStatement.
    def enterDenyReadPrefixStatement(self, ctx:o9IBPLParser.DenyReadPrefixStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#denyReadPrefixStatement.
    def exitDenyReadPrefixStatement(self, ctx:o9IBPLParser.DenyReadPrefixStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#grantAccessStatement.
    def enterGrantAccessStatement(self, ctx:o9IBPLParser.GrantAccessStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#grantAccessStatement.
    def exitGrantAccessStatement(self, ctx:o9IBPLParser.GrantAccessStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#accessDeclarationStatement.
    def enterAccessDeclarationStatement(self, ctx:o9IBPLParser.AccessDeclarationStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#accessDeclarationStatement.
    def exitAccessDeclarationStatement(self, ctx:o9IBPLParser.AccessDeclarationStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#grantWriteAccessPrefixStatement.
    def enterGrantWriteAccessPrefixStatement(self, ctx:o9IBPLParser.GrantWriteAccessPrefixStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#grantWriteAccessPrefixStatement.
    def exitGrantWriteAccessPrefixStatement(self, ctx:o9IBPLParser.GrantWriteAccessPrefixStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#grantReadAccessPrefixStatement.
    def enterGrantReadAccessPrefixStatement(self, ctx:o9IBPLParser.GrantReadAccessPrefixStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#grantReadAccessPrefixStatement.
    def exitGrantReadAccessPrefixStatement(self, ctx:o9IBPLParser.GrantReadAccessPrefixStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#grantExclusiveReadAccessPrefixStatement.
    def enterGrantExclusiveReadAccessPrefixStatement(self, ctx:o9IBPLParser.GrantExclusiveReadAccessPrefixStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#grantExclusiveReadAccessPrefixStatement.
    def exitGrantExclusiveReadAccessPrefixStatement(self, ctx:o9IBPLParser.GrantExclusiveReadAccessPrefixStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GrantDimensionWriteAccess.
    def enterGrantDimensionWriteAccess(self, ctx:o9IBPLParser.GrantDimensionWriteAccessContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GrantDimensionWriteAccess.
    def exitGrantDimensionWriteAccess(self, ctx:o9IBPLParser.GrantDimensionWriteAccessContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GrantCellWriteAccess.
    def enterGrantCellWriteAccess(self, ctx:o9IBPLParser.GrantCellWriteAccessContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GrantCellWriteAccess.
    def exitGrantCellWriteAccess(self, ctx:o9IBPLParser.GrantCellWriteAccessContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GrantDimensionWriteAccessAtMemberSet.
    def enterGrantDimensionWriteAccessAtMemberSet(self, ctx:o9IBPLParser.GrantDimensionWriteAccessAtMemberSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GrantDimensionWriteAccessAtMemberSet.
    def exitGrantDimensionWriteAccessAtMemberSet(self, ctx:o9IBPLParser.GrantDimensionWriteAccessAtMemberSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GrantDimensionWriteAccessAtDimension.
    def enterGrantDimensionWriteAccessAtDimension(self, ctx:o9IBPLParser.GrantDimensionWriteAccessAtDimensionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GrantDimensionWriteAccessAtDimension.
    def exitGrantDimensionWriteAccessAtDimension(self, ctx:o9IBPLParser.GrantDimensionWriteAccessAtDimensionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GrantDimensionWriteAccessAtAttribute.
    def enterGrantDimensionWriteAccessAtAttribute(self, ctx:o9IBPLParser.GrantDimensionWriteAccessAtAttributeContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GrantDimensionWriteAccessAtAttribute.
    def exitGrantDimensionWriteAccessAtAttribute(self, ctx:o9IBPLParser.GrantDimensionWriteAccessAtAttributeContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GrantDimensionExclusiveReadAccessAtMemberSet.
    def enterGrantDimensionExclusiveReadAccessAtMemberSet(self, ctx:o9IBPLParser.GrantDimensionExclusiveReadAccessAtMemberSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GrantDimensionExclusiveReadAccessAtMemberSet.
    def exitGrantDimensionExclusiveReadAccessAtMemberSet(self, ctx:o9IBPLParser.GrantDimensionExclusiveReadAccessAtMemberSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GrantDimensionExclusiveReadAccessAtDimension.
    def enterGrantDimensionExclusiveReadAccessAtDimension(self, ctx:o9IBPLParser.GrantDimensionExclusiveReadAccessAtDimensionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GrantDimensionExclusiveReadAccessAtDimension.
    def exitGrantDimensionExclusiveReadAccessAtDimension(self, ctx:o9IBPLParser.GrantDimensionExclusiveReadAccessAtDimensionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GrantDimensionExclusiveReadAccessAtAttribute.
    def enterGrantDimensionExclusiveReadAccessAtAttribute(self, ctx:o9IBPLParser.GrantDimensionExclusiveReadAccessAtAttributeContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GrantDimensionExclusiveReadAccessAtAttribute.
    def exitGrantDimensionExclusiveReadAccessAtAttribute(self, ctx:o9IBPLParser.GrantDimensionExclusiveReadAccessAtAttributeContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#grantCellWriteAccessStatement.
    def enterGrantCellWriteAccessStatement(self, ctx:o9IBPLParser.GrantCellWriteAccessStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#grantCellWriteAccessStatement.
    def exitGrantCellWriteAccessStatement(self, ctx:o9IBPLParser.GrantCellWriteAccessStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#grantCellReadAccessStatement.
    def enterGrantCellReadAccessStatement(self, ctx:o9IBPLParser.GrantCellReadAccessStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#grantCellReadAccessStatement.
    def exitGrantCellReadAccessStatement(self, ctx:o9IBPLParser.GrantCellReadAccessStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GrantDimensionReadAccessAtMemberSet.
    def enterGrantDimensionReadAccessAtMemberSet(self, ctx:o9IBPLParser.GrantDimensionReadAccessAtMemberSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GrantDimensionReadAccessAtMemberSet.
    def exitGrantDimensionReadAccessAtMemberSet(self, ctx:o9IBPLParser.GrantDimensionReadAccessAtMemberSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GrantDimensionReadAccessAtDimension.
    def enterGrantDimensionReadAccessAtDimension(self, ctx:o9IBPLParser.GrantDimensionReadAccessAtDimensionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GrantDimensionReadAccessAtDimension.
    def exitGrantDimensionReadAccessAtDimension(self, ctx:o9IBPLParser.GrantDimensionReadAccessAtDimensionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GrantDimensionReadAccessAtAttribute.
    def enterGrantDimensionReadAccessAtAttribute(self, ctx:o9IBPLParser.GrantDimensionReadAccessAtAttributeContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GrantDimensionReadAccessAtAttribute.
    def exitGrantDimensionReadAccessAtAttribute(self, ctx:o9IBPLParser.GrantDimensionReadAccessAtAttributeContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GrantDimensionReadAccessAtAttributeBasedOnMeasure.
    def enterGrantDimensionReadAccessAtAttributeBasedOnMeasure(self, ctx:o9IBPLParser.GrantDimensionReadAccessAtAttributeBasedOnMeasureContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GrantDimensionReadAccessAtAttributeBasedOnMeasure.
    def exitGrantDimensionReadAccessAtAttributeBasedOnMeasure(self, ctx:o9IBPLParser.GrantDimensionReadAccessAtAttributeBasedOnMeasureContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#attributeAccessStatement.
    def enterAttributeAccessStatement(self, ctx:o9IBPLParser.AttributeAccessStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#attributeAccessStatement.
    def exitAttributeAccessStatement(self, ctx:o9IBPLParser.AttributeAccessStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#denyCellWriteAccessStatement.
    def enterDenyCellWriteAccessStatement(self, ctx:o9IBPLParser.DenyCellWriteAccessStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#denyCellWriteAccessStatement.
    def exitDenyCellWriteAccessStatement(self, ctx:o9IBPLParser.DenyCellWriteAccessStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#denyWritePrefixStatement.
    def enterDenyWritePrefixStatement(self, ctx:o9IBPLParser.DenyWritePrefixStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#denyWritePrefixStatement.
    def exitDenyWritePrefixStatement(self, ctx:o9IBPLParser.DenyWritePrefixStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#PlanAccess.
    def enterPlanAccess(self, ctx:o9IBPLParser.PlanAccessContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#PlanAccess.
    def exitPlanAccess(self, ctx:o9IBPLParser.PlanAccessContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MeasureGroupAccess.
    def enterMeasureGroupAccess(self, ctx:o9IBPLParser.MeasureGroupAccessContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MeasureGroupAccess.
    def exitMeasureGroupAccess(self, ctx:o9IBPLParser.MeasureGroupAccessContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MeasureAccess.
    def enterMeasureAccess(self, ctx:o9IBPLParser.MeasureAccessContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MeasureAccess.
    def exitMeasureAccess(self, ctx:o9IBPLParser.MeasureAccessContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#getAccessControlRulesInfo.
    def enterGetAccessControlRulesInfo(self, ctx:o9IBPLParser.GetAccessControlRulesInfoContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#getAccessControlRulesInfo.
    def exitGetAccessControlRulesInfo(self, ctx:o9IBPLParser.GetAccessControlRulesInfoContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measureFilterStatement.
    def enterMeasureFilterStatement(self, ctx:o9IBPLParser.MeasureFilterStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measureFilterStatement.
    def exitMeasureFilterStatement(self, ctx:o9IBPLParser.MeasureFilterStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#activePluginStatement.
    def enterActivePluginStatement(self, ctx:o9IBPLParser.ActivePluginStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#activePluginStatement.
    def exitActivePluginStatement(self, ctx:o9IBPLParser.ActivePluginStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#onDemandPluginStatement.
    def enterOnDemandPluginStatement(self, ctx:o9IBPLParser.OnDemandPluginStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#onDemandPluginStatement.
    def exitOnDemandPluginStatement(self, ctx:o9IBPLParser.OnDemandPluginStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#executePowershellPluginStatement.
    def enterExecutePowershellPluginStatement(self, ctx:o9IBPLParser.ExecutePowershellPluginStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#executePowershellPluginStatement.
    def exitExecutePowershellPluginStatement(self, ctx:o9IBPLParser.ExecutePowershellPluginStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#operatingScopeStatement.
    def enterOperatingScopeStatement(self, ctx:o9IBPLParser.OperatingScopeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#operatingScopeStatement.
    def exitOperatingScopeStatement(self, ctx:o9IBPLParser.OperatingScopeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#usingArgumentsClause.
    def enterUsingArgumentsClause(self, ctx:o9IBPLParser.UsingArgumentsClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#usingArgumentsClause.
    def exitUsingArgumentsClause(self, ctx:o9IBPLParser.UsingArgumentsClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#argumentsClause.
    def enterArgumentsClause(self, ctx:o9IBPLParser.ArgumentsClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#argumentsClause.
    def exitArgumentsClause(self, ctx:o9IBPLParser.ArgumentsClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#postActionClause.
    def enterPostActionClause(self, ctx:o9IBPLParser.PostActionClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#postActionClause.
    def exitPostActionClause(self, ctx:o9IBPLParser.PostActionClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#scenarioScopeStatement.
    def enterScenarioScopeStatement(self, ctx:o9IBPLParser.ScenarioScopeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#scenarioScopeStatement.
    def exitScenarioScopeStatement(self, ctx:o9IBPLParser.ScenarioScopeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#usingScopeStatement.
    def enterUsingScopeStatement(self, ctx:o9IBPLParser.UsingScopeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#usingScopeStatement.
    def exitUsingScopeStatement(self, ctx:o9IBPLParser.UsingScopeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#scopeClause.
    def enterScopeClause(self, ctx:o9IBPLParser.ScopeClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#scopeClause.
    def exitScopeClause(self, ctx:o9IBPLParser.ScopeClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#globalScenarioScopeStatement.
    def enterGlobalScenarioScopeStatement(self, ctx:o9IBPLParser.GlobalScenarioScopeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#globalScenarioScopeStatement.
    def exitGlobalScenarioScopeStatement(self, ctx:o9IBPLParser.GlobalScenarioScopeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measureList.
    def enterMeasureList(self, ctx:o9IBPLParser.MeasureListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measureList.
    def exitMeasureList(self, ctx:o9IBPLParser.MeasureListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#identifierList.
    def enterIdentifierList(self, ctx:o9IBPLParser.IdentifierListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#identifierList.
    def exitIdentifierList(self, ctx:o9IBPLParser.IdentifierListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#referMeasuresInParent.
    def enterReferMeasuresInParent(self, ctx:o9IBPLParser.ReferMeasuresInParentContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#referMeasuresInParent.
    def exitReferMeasuresInParent(self, ctx:o9IBPLParser.ReferMeasuresInParentContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#mgOverriddenLocalScopeList.
    def enterMgOverriddenLocalScopeList(self, ctx:o9IBPLParser.MgOverriddenLocalScopeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#mgOverriddenLocalScopeList.
    def exitMgOverriddenLocalScopeList(self, ctx:o9IBPLParser.MgOverriddenLocalScopeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#mgOverriddenScopeList.
    def enterMgOverriddenScopeList(self, ctx:o9IBPLParser.MgOverriddenScopeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#mgOverriddenScopeList.
    def exitMgOverriddenScopeList(self, ctx:o9IBPLParser.MgOverriddenScopeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#includeModelsStatement.
    def enterIncludeModelsStatement(self, ctx:o9IBPLParser.IncludeModelsStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#includeModelsStatement.
    def exitIncludeModelsStatement(self, ctx:o9IBPLParser.IncludeModelsStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#mgNewOverriddenLocalScopeList.
    def enterMgNewOverriddenLocalScopeList(self, ctx:o9IBPLParser.MgNewOverriddenLocalScopeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#mgNewOverriddenLocalScopeList.
    def exitMgNewOverriddenLocalScopeList(self, ctx:o9IBPLParser.MgNewOverriddenLocalScopeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#planLocalScopeList.
    def enterPlanLocalScopeList(self, ctx:o9IBPLParser.PlanLocalScopeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#planLocalScopeList.
    def exitPlanLocalScopeList(self, ctx:o9IBPLParser.PlanLocalScopeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#planOveriddenScopeList.
    def enterPlanOveriddenScopeList(self, ctx:o9IBPLParser.PlanOveriddenScopeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#planOveriddenScopeList.
    def exitPlanOveriddenScopeList(self, ctx:o9IBPLParser.PlanOveriddenScopeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#mgNewOverriddenScopeList.
    def enterMgNewOverriddenScopeList(self, ctx:o9IBPLParser.MgNewOverriddenScopeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#mgNewOverriddenScopeList.
    def exitMgNewOverriddenScopeList(self, ctx:o9IBPLParser.MgNewOverriddenScopeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#includeMeasuresStatement.
    def enterIncludeMeasuresStatement(self, ctx:o9IBPLParser.IncludeMeasuresStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#includeMeasuresStatement.
    def exitIncludeMeasuresStatement(self, ctx:o9IBPLParser.IncludeMeasuresStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#includePointerMeasuresStatement.
    def enterIncludePointerMeasuresStatement(self, ctx:o9IBPLParser.IncludePointerMeasuresStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#includePointerMeasuresStatement.
    def exitIncludePointerMeasuresStatement(self, ctx:o9IBPLParser.IncludePointerMeasuresStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#includePointerMeasuresList.
    def enterIncludePointerMeasuresList(self, ctx:o9IBPLParser.IncludePointerMeasuresListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#includePointerMeasuresList.
    def exitIncludePointerMeasuresList(self, ctx:o9IBPLParser.IncludePointerMeasuresListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#mgScopeList.
    def enterMgScopeList(self, ctx:o9IBPLParser.MgScopeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#mgScopeList.
    def exitMgScopeList(self, ctx:o9IBPLParser.MgScopeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#mgScopeStatement.
    def enterMgScopeStatement(self, ctx:o9IBPLParser.MgScopeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#mgScopeStatement.
    def exitMgScopeStatement(self, ctx:o9IBPLParser.MgScopeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphScopeList.
    def enterGraphScopeList(self, ctx:o9IBPLParser.GraphScopeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphScopeList.
    def exitGraphScopeList(self, ctx:o9IBPLParser.GraphScopeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphScopeStatement.
    def enterGraphScopeStatement(self, ctx:o9IBPLParser.GraphScopeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphScopeStatement.
    def exitGraphScopeStatement(self, ctx:o9IBPLParser.GraphScopeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#includePlanStatement.
    def enterIncludePlanStatement(self, ctx:o9IBPLParser.IncludePlanStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#includePlanStatement.
    def exitIncludePlanStatement(self, ctx:o9IBPLParser.IncludePlanStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#includePlanStatementList.
    def enterIncludePlanStatementList(self, ctx:o9IBPLParser.IncludePlanStatementListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#includePlanStatementList.
    def exitIncludePlanStatementList(self, ctx:o9IBPLParser.IncludePlanStatementListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#fromVertexStatement.
    def enterFromVertexStatement(self, ctx:o9IBPLParser.FromVertexStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#fromVertexStatement.
    def exitFromVertexStatement(self, ctx:o9IBPLParser.FromVertexStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#toVertexStatement.
    def enterToVertexStatement(self, ctx:o9IBPLParser.ToVertexStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#toVertexStatement.
    def exitToVertexStatement(self, ctx:o9IBPLParser.ToVertexStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#usingVertexScopeStatement.
    def enterUsingVertexScopeStatement(self, ctx:o9IBPLParser.UsingVertexScopeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#usingVertexScopeStatement.
    def exitUsingVertexScopeStatement(self, ctx:o9IBPLParser.UsingVertexScopeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edgeList.
    def enterEdgeList(self, ctx:o9IBPLParser.EdgeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edgeList.
    def exitEdgeList(self, ctx:o9IBPLParser.EdgeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#fullyQualifiedEdgeList.
    def enterFullyQualifiedEdgeList(self, ctx:o9IBPLParser.FullyQualifiedEdgeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#fullyQualifiedEdgeList.
    def exitFullyQualifiedEdgeList(self, ctx:o9IBPLParser.FullyQualifiedEdgeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#referEdgePropInParent.
    def enterReferEdgePropInParent(self, ctx:o9IBPLParser.ReferEdgePropInParentContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#referEdgePropInParent.
    def exitReferEdgePropInParent(self, ctx:o9IBPLParser.ReferEdgePropInParentContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphOverriddenLocalScopeList.
    def enterGraphOverriddenLocalScopeList(self, ctx:o9IBPLParser.GraphOverriddenLocalScopeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphOverriddenLocalScopeList.
    def exitGraphOverriddenLocalScopeList(self, ctx:o9IBPLParser.GraphOverriddenLocalScopeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphOverriddenScopeList.
    def enterGraphOverriddenScopeList(self, ctx:o9IBPLParser.GraphOverriddenScopeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphOverriddenScopeList.
    def exitGraphOverriddenScopeList(self, ctx:o9IBPLParser.GraphOverriddenScopeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#includeGraphsStatement.
    def enterIncludeGraphsStatement(self, ctx:o9IBPLParser.IncludeGraphsStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#includeGraphsStatement.
    def exitIncludeGraphsStatement(self, ctx:o9IBPLParser.IncludeGraphsStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edgeOverriddenLocalScopeList.
    def enterEdgeOverriddenLocalScopeList(self, ctx:o9IBPLParser.EdgeOverriddenLocalScopeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edgeOverriddenLocalScopeList.
    def exitEdgeOverriddenLocalScopeList(self, ctx:o9IBPLParser.EdgeOverriddenLocalScopeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edgeOverriddenScopeList.
    def enterEdgeOverriddenScopeList(self, ctx:o9IBPLParser.EdgeOverriddenScopeListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edgeOverriddenScopeList.
    def exitEdgeOverriddenScopeList(self, ctx:o9IBPLParser.EdgeOverriddenScopeListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#includeEdgesStatement.
    def enterIncludeEdgesStatement(self, ctx:o9IBPLParser.IncludeEdgesStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#includeEdgesStatement.
    def exitIncludeEdgesStatement(self, ctx:o9IBPLParser.IncludeEdgesStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#pointerEdgeStatement.
    def enterPointerEdgeStatement(self, ctx:o9IBPLParser.PointerEdgeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#pointerEdgeStatement.
    def exitPointerEdgeStatement(self, ctx:o9IBPLParser.PointerEdgeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#pointerEdgeStatementList.
    def enterPointerEdgeStatementList(self, ctx:o9IBPLParser.PointerEdgeStatementListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#pointerEdgeStatementList.
    def exitPointerEdgeStatementList(self, ctx:o9IBPLParser.PointerEdgeStatementListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#includeDependentEntities.
    def enterIncludeDependentEntities(self, ctx:o9IBPLParser.IncludeDependentEntitiesContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#includeDependentEntities.
    def exitIncludeDependentEntities(self, ctx:o9IBPLParser.IncludeDependentEntitiesContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#initializeScenarioStatement.
    def enterInitializeScenarioStatement(self, ctx:o9IBPLParser.InitializeScenarioStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#initializeScenarioStatement.
    def exitInitializeScenarioStatement(self, ctx:o9IBPLParser.InitializeScenarioStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#initializeMeasureGroupStatement.
    def enterInitializeMeasureGroupStatement(self, ctx:o9IBPLParser.InitializeMeasureGroupStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#initializeMeasureGroupStatement.
    def exitInitializeMeasureGroupStatement(self, ctx:o9IBPLParser.InitializeMeasureGroupStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#initializeMeasuresStatement.
    def enterInitializeMeasuresStatement(self, ctx:o9IBPLParser.InitializeMeasuresStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#initializeMeasuresStatement.
    def exitInitializeMeasuresStatement(self, ctx:o9IBPLParser.InitializeMeasuresStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#initializeGraphStatement.
    def enterInitializeGraphStatement(self, ctx:o9IBPLParser.InitializeGraphStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#initializeGraphStatement.
    def exitInitializeGraphStatement(self, ctx:o9IBPLParser.InitializeGraphStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#initializeEdgeStatement.
    def enterInitializeEdgeStatement(self, ctx:o9IBPLParser.InitializeEdgeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#initializeEdgeStatement.
    def exitInitializeEdgeStatement(self, ctx:o9IBPLParser.InitializeEdgeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#versionArgs.
    def enterVersionArgs(self, ctx:o9IBPLParser.VersionArgsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#versionArgs.
    def exitVersionArgs(self, ctx:o9IBPLParser.VersionArgsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#genericVersionArgs.
    def enterGenericVersionArgs(self, ctx:o9IBPLParser.GenericVersionArgsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#genericVersionArgs.
    def exitGenericVersionArgs(self, ctx:o9IBPLParser.GenericVersionArgsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#argValuePair.
    def enterArgValuePair(self, ctx:o9IBPLParser.ArgValuePairContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#argValuePair.
    def exitArgValuePair(self, ctx:o9IBPLParser.ArgValuePairContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#versionNameOrExp.
    def enterVersionNameOrExp(self, ctx:o9IBPLParser.VersionNameOrExpContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#versionNameOrExp.
    def exitVersionNameOrExp(self, ctx:o9IBPLParser.VersionNameOrExpContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#createVersionStatement.
    def enterCreateVersionStatement(self, ctx:o9IBPLParser.CreateVersionStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#createVersionStatement.
    def exitCreateVersionStatement(self, ctx:o9IBPLParser.CreateVersionStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#createScenarioStatement.
    def enterCreateScenarioStatement(self, ctx:o9IBPLParser.CreateScenarioStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#createScenarioStatement.
    def exitCreateScenarioStatement(self, ctx:o9IBPLParser.CreateScenarioStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#createScopedScenarioStatement.
    def enterCreateScopedScenarioStatement(self, ctx:o9IBPLParser.CreateScopedScenarioStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#createScopedScenarioStatement.
    def exitCreateScopedScenarioStatement(self, ctx:o9IBPLParser.CreateScopedScenarioStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#createLWScenarioStatement.
    def enterCreateLWScenarioStatement(self, ctx:o9IBPLParser.CreateLWScenarioStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#createLWScenarioStatement.
    def exitCreateLWScenarioStatement(self, ctx:o9IBPLParser.CreateLWScenarioStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#createEphemeralScenarioStatement.
    def enterCreateEphemeralScenarioStatement(self, ctx:o9IBPLParser.CreateEphemeralScenarioStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#createEphemeralScenarioStatement.
    def exitCreateEphemeralScenarioStatement(self, ctx:o9IBPLParser.CreateEphemeralScenarioStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#scenarioSourceExpression.
    def enterScenarioSourceExpression(self, ctx:o9IBPLParser.ScenarioSourceExpressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#scenarioSourceExpression.
    def exitScenarioSourceExpression(self, ctx:o9IBPLParser.ScenarioSourceExpressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#deleteVersionStatement.
    def enterDeleteVersionStatement(self, ctx:o9IBPLParser.DeleteVersionStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#deleteVersionStatement.
    def exitDeleteVersionStatement(self, ctx:o9IBPLParser.DeleteVersionStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#updateScenarioStatement.
    def enterUpdateScenarioStatement(self, ctx:o9IBPLParser.UpdateScenarioStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#updateScenarioStatement.
    def exitUpdateScenarioStatement(self, ctx:o9IBPLParser.UpdateScenarioStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#updateVersionPropertyStatement.
    def enterUpdateVersionPropertyStatement(self, ctx:o9IBPLParser.UpdateVersionPropertyStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#updateVersionPropertyStatement.
    def exitUpdateVersionPropertyStatement(self, ctx:o9IBPLParser.UpdateVersionPropertyStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#shareScenarioStatement.
    def enterShareScenarioStatement(self, ctx:o9IBPLParser.ShareScenarioStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#shareScenarioStatement.
    def exitShareScenarioStatement(self, ctx:o9IBPLParser.ShareScenarioStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#unshareScenarioStatement.
    def enterUnshareScenarioStatement(self, ctx:o9IBPLParser.UnshareScenarioStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#unshareScenarioStatement.
    def exitUnshareScenarioStatement(self, ctx:o9IBPLParser.UnshareScenarioStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#versionExpressionStatement.
    def enterVersionExpressionStatement(self, ctx:o9IBPLParser.VersionExpressionStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#versionExpressionStatement.
    def exitVersionExpressionStatement(self, ctx:o9IBPLParser.VersionExpressionStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#createMemberStatement.
    def enterCreateMemberStatement(self, ctx:o9IBPLParser.CreateMemberStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#createMemberStatement.
    def exitCreateMemberStatement(self, ctx:o9IBPLParser.CreateMemberStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#updateMemberStatement.
    def enterUpdateMemberStatement(self, ctx:o9IBPLParser.UpdateMemberStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#updateMemberStatement.
    def exitUpdateMemberStatement(self, ctx:o9IBPLParser.UpdateMemberStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#deleteMemberStatement.
    def enterDeleteMemberStatement(self, ctx:o9IBPLParser.DeleteMemberStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#deleteMemberStatement.
    def exitDeleteMemberStatement(self, ctx:o9IBPLParser.DeleteMemberStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#copyMemberStatement.
    def enterCopyMemberStatement(self, ctx:o9IBPLParser.CopyMemberStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#copyMemberStatement.
    def exitCopyMemberStatement(self, ctx:o9IBPLParser.CopyMemberStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#copyMemberSourceMembers.
    def enterCopyMemberSourceMembers(self, ctx:o9IBPLParser.CopyMemberSourceMembersContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#copyMemberSourceMembers.
    def exitCopyMemberSourceMembers(self, ctx:o9IBPLParser.CopyMemberSourceMembersContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#copyMemberParentMembers.
    def enterCopyMemberParentMembers(self, ctx:o9IBPLParser.CopyMemberParentMembersContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#copyMemberParentMembers.
    def exitCopyMemberParentMembers(self, ctx:o9IBPLParser.CopyMemberParentMembersContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#copyMeasureStatement.
    def enterCopyMeasureStatement(self, ctx:o9IBPLParser.CopyMeasureStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#copyMeasureStatement.
    def exitCopyMeasureStatement(self, ctx:o9IBPLParser.CopyMeasureStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#copyMeasureOptions.
    def enterCopyMeasureOptions(self, ctx:o9IBPLParser.CopyMeasureOptionsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#copyMeasureOptions.
    def exitCopyMeasureOptions(self, ctx:o9IBPLParser.CopyMeasureOptionsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#crudMemberStatement.
    def enterCrudMemberStatement(self, ctx:o9IBPLParser.CrudMemberStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#crudMemberStatement.
    def exitCrudMemberStatement(self, ctx:o9IBPLParser.CrudMemberStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#crudMemberStatementSet.
    def enterCrudMemberStatementSet(self, ctx:o9IBPLParser.CrudMemberStatementSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#crudMemberStatementSet.
    def exitCrudMemberStatementSet(self, ctx:o9IBPLParser.CrudMemberStatementSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#purgeMemberStatement.
    def enterPurgeMemberStatement(self, ctx:o9IBPLParser.PurgeMemberStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#purgeMemberStatement.
    def exitPurgeMemberStatement(self, ctx:o9IBPLParser.PurgeMemberStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#bulkMemberCreateStatement.
    def enterBulkMemberCreateStatement(self, ctx:o9IBPLParser.BulkMemberCreateStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#bulkMemberCreateStatement.
    def exitBulkMemberCreateStatement(self, ctx:o9IBPLParser.BulkMemberCreateStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#filePaths.
    def enterFilePaths(self, ctx:o9IBPLParser.FilePathsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#filePaths.
    def exitFilePaths(self, ctx:o9IBPLParser.FilePathsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#uploadDatafileStatement.
    def enterUploadDatafileStatement(self, ctx:o9IBPLParser.UploadDatafileStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#uploadDatafileStatement.
    def exitUploadDatafileStatement(self, ctx:o9IBPLParser.UploadDatafileStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#downloadDatafileStatement.
    def enterDownloadDatafileStatement(self, ctx:o9IBPLParser.DownloadDatafileStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#downloadDatafileStatement.
    def exitDownloadDatafileStatement(self, ctx:o9IBPLParser.DownloadDatafileStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#commandOption.
    def enterCommandOption(self, ctx:o9IBPLParser.CommandOptionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#commandOption.
    def exitCommandOption(self, ctx:o9IBPLParser.CommandOptionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#exportAllStatement.
    def enterExportAllStatement(self, ctx:o9IBPLParser.ExportAllStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#exportAllStatement.
    def exitExportAllStatement(self, ctx:o9IBPLParser.ExportAllStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#importAllStatement.
    def enterImportAllStatement(self, ctx:o9IBPLParser.ImportAllStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#importAllStatement.
    def exitImportAllStatement(self, ctx:o9IBPLParser.ImportAllStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#saveStatement.
    def enterSaveStatement(self, ctx:o9IBPLParser.SaveStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#saveStatement.
    def exitSaveStatement(self, ctx:o9IBPLParser.SaveStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#serviceCommandStatement.
    def enterServiceCommandStatement(self, ctx:o9IBPLParser.ServiceCommandStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#serviceCommandStatement.
    def exitServiceCommandStatement(self, ctx:o9IBPLParser.ServiceCommandStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#restoreExternalDataStatement.
    def enterRestoreExternalDataStatement(self, ctx:o9IBPLParser.RestoreExternalDataStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#restoreExternalDataStatement.
    def exitRestoreExternalDataStatement(self, ctx:o9IBPLParser.RestoreExternalDataStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#syncExternalModelsStatement.
    def enterSyncExternalModelsStatement(self, ctx:o9IBPLParser.SyncExternalModelsStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#syncExternalModelsStatement.
    def exitSyncExternalModelsStatement(self, ctx:o9IBPLParser.SyncExternalModelsStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#syncLocalModelsStatement.
    def enterSyncLocalModelsStatement(self, ctx:o9IBPLParser.SyncLocalModelsStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#syncLocalModelsStatement.
    def exitSyncLocalModelsStatement(self, ctx:o9IBPLParser.SyncLocalModelsStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#syncLocalExcludePropertyList.
    def enterSyncLocalExcludePropertyList(self, ctx:o9IBPLParser.SyncLocalExcludePropertyListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#syncLocalExcludePropertyList.
    def exitSyncLocalExcludePropertyList(self, ctx:o9IBPLParser.SyncLocalExcludePropertyListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#refreshMaterializedViewsStatement.
    def enterRefreshMaterializedViewsStatement(self, ctx:o9IBPLParser.RefreshMaterializedViewsStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#refreshMaterializedViewsStatement.
    def exitRefreshMaterializedViewsStatement(self, ctx:o9IBPLParser.RefreshMaterializedViewsStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#releaseTableMemoryStatement.
    def enterReleaseTableMemoryStatement(self, ctx:o9IBPLParser.ReleaseTableMemoryStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#releaseTableMemoryStatement.
    def exitReleaseTableMemoryStatement(self, ctx:o9IBPLParser.ReleaseTableMemoryStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#mergeDeltaModelsStatement.
    def enterMergeDeltaModelsStatement(self, ctx:o9IBPLParser.MergeDeltaModelsStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#mergeDeltaModelsStatement.
    def exitMergeDeltaModelsStatement(self, ctx:o9IBPLParser.MergeDeltaModelsStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#resetAccessControlStatement.
    def enterResetAccessControlStatement(self, ctx:o9IBPLParser.ResetAccessControlStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#resetAccessControlStatement.
    def exitResetAccessControlStatement(self, ctx:o9IBPLParser.ResetAccessControlStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#generateGraphStatement.
    def enterGenerateGraphStatement(self, ctx:o9IBPLParser.GenerateGraphStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#generateGraphStatement.
    def exitGenerateGraphStatement(self, ctx:o9IBPLParser.GenerateGraphStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#netChangeAclStatement.
    def enterNetChangeAclStatement(self, ctx:o9IBPLParser.NetChangeAclStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#netChangeAclStatement.
    def exitNetChangeAclStatement(self, ctx:o9IBPLParser.NetChangeAclStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#netChangeAclRoleStatement.
    def enterNetChangeAclRoleStatement(self, ctx:o9IBPLParser.NetChangeAclRoleStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#netChangeAclRoleStatement.
    def exitNetChangeAclRoleStatement(self, ctx:o9IBPLParser.NetChangeAclRoleStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#rolePropertyValuePair.
    def enterRolePropertyValuePair(self, ctx:o9IBPLParser.RolePropertyValuePairContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#rolePropertyValuePair.
    def exitRolePropertyValuePair(self, ctx:o9IBPLParser.RolePropertyValuePairContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#netChangeAclRuleStatement.
    def enterNetChangeAclRuleStatement(self, ctx:o9IBPLParser.NetChangeAclRuleStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#netChangeAclRuleStatement.
    def exitNetChangeAclRuleStatement(self, ctx:o9IBPLParser.NetChangeAclRuleStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#simulateWriteStatement.
    def enterSimulateWriteStatement(self, ctx:o9IBPLParser.SimulateWriteStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#simulateWriteStatement.
    def exitSimulateWriteStatement(self, ctx:o9IBPLParser.SimulateWriteStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#memberAttributeAssignment.
    def enterMemberAttributeAssignment(self, ctx:o9IBPLParser.MemberAttributeAssignmentContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#memberAttributeAssignment.
    def exitMemberAttributeAssignment(self, ctx:o9IBPLParser.MemberAttributeAssignmentContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#memberNameAssignmentPairs.
    def enterMemberNameAssignmentPairs(self, ctx:o9IBPLParser.MemberNameAssignmentPairsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#memberNameAssignmentPairs.
    def exitMemberNameAssignmentPairs(self, ctx:o9IBPLParser.MemberNameAssignmentPairsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#memberAssignmentPairs.
    def enterMemberAssignmentPairs(self, ctx:o9IBPLParser.MemberAssignmentPairsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#memberAssignmentPairs.
    def exitMemberAssignmentPairs(self, ctx:o9IBPLParser.MemberAssignmentPairsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#memberNamePair.
    def enterMemberNamePair(self, ctx:o9IBPLParser.MemberNamePairContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#memberNamePair.
    def exitMemberNamePair(self, ctx:o9IBPLParser.MemberNamePairContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#currentUserStatement.
    def enterCurrentUserStatement(self, ctx:o9IBPLParser.CurrentUserStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#currentUserStatement.
    def exitCurrentUserStatement(self, ctx:o9IBPLParser.CurrentUserStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#selectMemberExprStatement.
    def enterSelectMemberExprStatement(self, ctx:o9IBPLParser.SelectMemberExprStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#selectMemberExprStatement.
    def exitSelectMemberExprStatement(self, ctx:o9IBPLParser.SelectMemberExprStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#selectCrossJoinStatement.
    def enterSelectCrossJoinStatement(self, ctx:o9IBPLParser.SelectCrossJoinStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#selectCrossJoinStatement.
    def exitSelectCrossJoinStatement(self, ctx:o9IBPLParser.SelectCrossJoinStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#selectCrossJoinStatementWithPostFilter.
    def enterSelectCrossJoinStatementWithPostFilter(self, ctx:o9IBPLParser.SelectCrossJoinStatementWithPostFilterContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#selectCrossJoinStatementWithPostFilter.
    def exitSelectCrossJoinStatementWithPostFilter(self, ctx:o9IBPLParser.SelectCrossJoinStatementWithPostFilterContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#selectMemberStatement.
    def enterSelectMemberStatement(self, ctx:o9IBPLParser.SelectMemberStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#selectMemberStatement.
    def exitSelectMemberStatement(self, ctx:o9IBPLParser.SelectMemberStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#selectScenarioScopedMemberStatement.
    def enterSelectScenarioScopedMemberStatement(self, ctx:o9IBPLParser.SelectScenarioScopedMemberStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#selectScenarioScopedMemberStatement.
    def exitSelectScenarioScopedMemberStatement(self, ctx:o9IBPLParser.SelectScenarioScopedMemberStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#countSelectMemberExprStatement.
    def enterCountSelectMemberExprStatement(self, ctx:o9IBPLParser.CountSelectMemberExprStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#countSelectMemberExprStatement.
    def exitCountSelectMemberExprStatement(self, ctx:o9IBPLParser.CountSelectMemberExprStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#spreadSelectCrossJoinStatement.
    def enterSpreadSelectCrossJoinStatement(self, ctx:o9IBPLParser.SpreadSelectCrossJoinStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#spreadSelectCrossJoinStatement.
    def exitSpreadSelectCrossJoinStatement(self, ctx:o9IBPLParser.SpreadSelectCrossJoinStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#member_filter_set.
    def enterMember_filter_set(self, ctx:o9IBPLParser.Member_filter_setContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#member_filter_set.
    def exitMember_filter_set(self, ctx:o9IBPLParser.Member_filter_setContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#member_filter.
    def enterMember_filter(self, ctx:o9IBPLParser.Member_filterContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#member_filter.
    def exitMember_filter(self, ctx:o9IBPLParser.Member_filterContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#withCalcMembersClause.
    def enterWithCalcMembersClause(self, ctx:o9IBPLParser.WithCalcMembersClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#withCalcMembersClause.
    def exitWithCalcMembersClause(self, ctx:o9IBPLParser.WithCalcMembersClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#calcMemberClause.
    def enterCalcMemberClause(self, ctx:o9IBPLParser.CalcMemberClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#calcMemberClause.
    def exitCalcMemberClause(self, ctx:o9IBPLParser.CalcMemberClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#calcMemberCellPropertiesClause.
    def enterCalcMemberCellPropertiesClause(self, ctx:o9IBPLParser.CalcMemberCellPropertiesClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#calcMemberCellPropertiesClause.
    def exitCalcMemberCellPropertiesClause(self, ctx:o9IBPLParser.CalcMemberCellPropertiesClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measure_cell_properties_pair.
    def enterMeasure_cell_properties_pair(self, ctx:o9IBPLParser.Measure_cell_properties_pairContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measure_cell_properties_pair.
    def exitMeasure_cell_properties_pair(self, ctx:o9IBPLParser.Measure_cell_properties_pairContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#cell_property_override.
    def enterCell_property_override(self, ctx:o9IBPLParser.Cell_property_overrideContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#cell_property_override.
    def exitCell_property_override(self, ctx:o9IBPLParser.Cell_property_overrideContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#calcMemberOverridesClause.
    def enterCalcMemberOverridesClause(self, ctx:o9IBPLParser.CalcMemberOverridesClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#calcMemberOverridesClause.
    def exitCalcMemberOverridesClause(self, ctx:o9IBPLParser.CalcMemberOverridesClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measure_calcmemberexpression_pair.
    def enterMeasure_calcmemberexpression_pair(self, ctx:o9IBPLParser.Measure_calcmemberexpression_pairContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measure_calcmemberexpression_pair.
    def exitMeasure_calcmemberexpression_pair(self, ctx:o9IBPLParser.Measure_calcmemberexpression_pairContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#withTransientMeasureClause.
    def enterWithTransientMeasureClause(self, ctx:o9IBPLParser.WithTransientMeasureClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#withTransientMeasureClause.
    def exitWithTransientMeasureClause(self, ctx:o9IBPLParser.WithTransientMeasureClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#transientMeasureClause.
    def enterTransientMeasureClause(self, ctx:o9IBPLParser.TransientMeasureClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#transientMeasureClause.
    def exitTransientMeasureClause(self, ctx:o9IBPLParser.TransientMeasureClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#transientMeasurePropertyClause.
    def enterTransientMeasurePropertyClause(self, ctx:o9IBPLParser.TransientMeasurePropertyClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#transientMeasurePropertyClause.
    def exitTransientMeasurePropertyClause(self, ctx:o9IBPLParser.TransientMeasurePropertyClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#cellPropertyClause.
    def enterCellPropertyClause(self, ctx:o9IBPLParser.CellPropertyClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#cellPropertyClause.
    def exitCellPropertyClause(self, ctx:o9IBPLParser.CellPropertyClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#orderByClause.
    def enterOrderByClause(self, ctx:o9IBPLParser.OrderByClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#orderByClause.
    def exitOrderByClause(self, ctx:o9IBPLParser.OrderByClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#limitClause.
    def enterLimitClause(self, ctx:o9IBPLParser.LimitClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#limitClause.
    def exitLimitClause(self, ctx:o9IBPLParser.LimitClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#topClause.
    def enterTopClause(self, ctx:o9IBPLParser.TopClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#topClause.
    def exitTopClause(self, ctx:o9IBPLParser.TopClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#bottomClause.
    def enterBottomClause(self, ctx:o9IBPLParser.BottomClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#bottomClause.
    def exitBottomClause(self, ctx:o9IBPLParser.BottomClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#offsetClause.
    def enterOffsetClause(self, ctx:o9IBPLParser.OffsetClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#offsetClause.
    def exitOffsetClause(self, ctx:o9IBPLParser.OffsetClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#memberOrMeasureNameOrderByClause.
    def enterMemberOrMeasureNameOrderByClause(self, ctx:o9IBPLParser.MemberOrMeasureNameOrderByClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#memberOrMeasureNameOrderByClause.
    def exitMemberOrMeasureNameOrderByClause(self, ctx:o9IBPLParser.MemberOrMeasureNameOrderByClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#memberPropertyOrderByClause.
    def enterMemberPropertyOrderByClause(self, ctx:o9IBPLParser.MemberPropertyOrderByClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#memberPropertyOrderByClause.
    def exitMemberPropertyOrderByClause(self, ctx:o9IBPLParser.MemberPropertyOrderByClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measureNameOrderByClause.
    def enterMeasureNameOrderByClause(self, ctx:o9IBPLParser.MeasureNameOrderByClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measureNameOrderByClause.
    def exitMeasureNameOrderByClause(self, ctx:o9IBPLParser.MeasureNameOrderByClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#join_on_clause.
    def enterJoin_on_clause(self, ctx:o9IBPLParser.Join_on_clauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#join_on_clause.
    def exitJoin_on_clause(self, ctx:o9IBPLParser.Join_on_clauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#join_expression.
    def enterJoin_expression(self, ctx:o9IBPLParser.Join_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#join_expression.
    def exitJoin_expression(self, ctx:o9IBPLParser.Join_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#convert_using_clause.
    def enterConvert_using_clause(self, ctx:o9IBPLParser.Convert_using_clauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#convert_using_clause.
    def exitConvert_using_clause(self, ctx:o9IBPLParser.Convert_using_clauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#adornmentInfo.
    def enterAdornmentInfo(self, ctx:o9IBPLParser.AdornmentInfoContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#adornmentInfo.
    def exitAdornmentInfo(self, ctx:o9IBPLParser.AdornmentInfoContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#use_aliases.
    def enterUse_aliases(self, ctx:o9IBPLParser.Use_aliasesContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#use_aliases.
    def exitUse_aliases(self, ctx:o9IBPLParser.Use_aliasesContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#alias.
    def enterAlias(self, ctx:o9IBPLParser.AliasContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#alias.
    def exitAlias(self, ctx:o9IBPLParser.AliasContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#dimension_attribute_alias.
    def enterDimension_attribute_alias(self, ctx:o9IBPLParser.Dimension_attribute_aliasContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#dimension_attribute_alias.
    def exitDimension_attribute_alias(self, ctx:o9IBPLParser.Dimension_attribute_aliasContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#node_alias.
    def enterNode_alias(self, ctx:o9IBPLParser.Node_aliasContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#node_alias.
    def exitNode_alias(self, ctx:o9IBPLParser.Node_aliasContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#include_properties.
    def enterInclude_properties(self, ctx:o9IBPLParser.Include_propertiesContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#include_properties.
    def exitInclude_properties(self, ctx:o9IBPLParser.Include_propertiesContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#include_member_properties.
    def enterInclude_member_properties(self, ctx:o9IBPLParser.Include_member_propertiesContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#include_member_properties.
    def exitInclude_member_properties(self, ctx:o9IBPLParser.Include_member_propertiesContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#include_anchor_members.
    def enterInclude_anchor_members(self, ctx:o9IBPLParser.Include_anchor_membersContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#include_anchor_members.
    def exitInclude_anchor_members(self, ctx:o9IBPLParser.Include_anchor_membersContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#anchor_members.
    def enterAnchor_members(self, ctx:o9IBPLParser.Anchor_membersContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#anchor_members.
    def exitAnchor_members(self, ctx:o9IBPLParser.Anchor_membersContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#query_option_list.
    def enterQuery_option_list(self, ctx:o9IBPLParser.Query_option_listContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#query_option_list.
    def exitQuery_option_list(self, ctx:o9IBPLParser.Query_option_listContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#query_option.
    def enterQuery_option(self, ctx:o9IBPLParser.Query_optionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#query_option.
    def exitQuery_option(self, ctx:o9IBPLParser.Query_optionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#include_nullmember.
    def enterInclude_nullmember(self, ctx:o9IBPLParser.Include_nullmemberContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#include_nullmember.
    def exitInclude_nullmember(self, ctx:o9IBPLParser.Include_nullmemberContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#include_subtotals.
    def enterInclude_subtotals(self, ctx:o9IBPLParser.Include_subtotalsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#include_subtotals.
    def exitInclude_subtotals(self, ctx:o9IBPLParser.Include_subtotalsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#include_subtotals_sub_query.
    def enterInclude_subtotals_sub_query(self, ctx:o9IBPLParser.Include_subtotals_sub_queryContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#include_subtotals_sub_query.
    def exitInclude_subtotals_sub_query(self, ctx:o9IBPLParser.Include_subtotals_sub_queryContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#sub_query.
    def enterSub_query(self, ctx:o9IBPLParser.Sub_queryContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#sub_query.
    def exitSub_query(self, ctx:o9IBPLParser.Sub_queryContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#sub_query_element.
    def enterSub_query_element(self, ctx:o9IBPLParser.Sub_query_elementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#sub_query_element.
    def exitSub_query_element(self, ctx:o9IBPLParser.Sub_query_elementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#include_nulls.
    def enterInclude_nulls(self, ctx:o9IBPLParser.Include_nullsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#include_nulls.
    def exitInclude_nulls(self, ctx:o9IBPLParser.Include_nullsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#member_measure_filter_set.
    def enterMember_measure_filter_set(self, ctx:o9IBPLParser.Member_measure_filter_setContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#member_measure_filter_set.
    def exitMember_measure_filter_set(self, ctx:o9IBPLParser.Member_measure_filter_setContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#member_measure_filter.
    def enterMember_measure_filter(self, ctx:o9IBPLParser.Member_measure_filterContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#member_measure_filter.
    def exitMember_measure_filter(self, ctx:o9IBPLParser.Member_measure_filterContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measureZeroClause.
    def enterMeasureZeroClause(self, ctx:o9IBPLParser.MeasureZeroClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measureZeroClause.
    def exitMeasureZeroClause(self, ctx:o9IBPLParser.MeasureZeroClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#attribute_properties.
    def enterAttribute_properties(self, ctx:o9IBPLParser.Attribute_propertiesContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#attribute_properties.
    def exitAttribute_properties(self, ctx:o9IBPLParser.Attribute_propertiesContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#computePlanStatement.
    def enterComputePlanStatement(self, ctx:o9IBPLParser.ComputePlanStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#computePlanStatement.
    def exitComputePlanStatement(self, ctx:o9IBPLParser.ComputePlanStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#enableDisablePlanStatement.
    def enterEnableDisablePlanStatement(self, ctx:o9IBPLParser.EnableDisablePlanStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#enableDisablePlanStatement.
    def exitEnableDisablePlanStatement(self, ctx:o9IBPLParser.EnableDisablePlanStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#beginTransactionStatement.
    def enterBeginTransactionStatement(self, ctx:o9IBPLParser.BeginTransactionStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#beginTransactionStatement.
    def exitBeginTransactionStatement(self, ctx:o9IBPLParser.BeginTransactionStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#commitTransactionStatement.
    def enterCommitTransactionStatement(self, ctx:o9IBPLParser.CommitTransactionStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#commitTransactionStatement.
    def exitCommitTransactionStatement(self, ctx:o9IBPLParser.CommitTransactionStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#DiscardTransaction.
    def enterDiscardTransaction(self, ctx:o9IBPLParser.DiscardTransactionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#DiscardTransaction.
    def exitDiscardTransaction(self, ctx:o9IBPLParser.DiscardTransactionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#DiscardTransactionWithImpact.
    def enterDiscardTransactionWithImpact(self, ctx:o9IBPLParser.DiscardTransactionWithImpactContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#DiscardTransactionWithImpact.
    def exitDiscardTransactionWithImpact(self, ctx:o9IBPLParser.DiscardTransactionWithImpactContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#abortTransaction.
    def enterAbortTransaction(self, ctx:o9IBPLParser.AbortTransactionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#abortTransaction.
    def exitAbortTransaction(self, ctx:o9IBPLParser.AbortTransactionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#UpdateAssignment.
    def enterUpdateAssignment(self, ctx:o9IBPLParser.UpdateAssignmentContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#UpdateAssignment.
    def exitUpdateAssignment(self, ctx:o9IBPLParser.UpdateAssignmentContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#UpdateSingleTupleSet.
    def enterUpdateSingleTupleSet(self, ctx:o9IBPLParser.UpdateSingleTupleSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#UpdateSingleTupleSet.
    def exitUpdateSingleTupleSet(self, ctx:o9IBPLParser.UpdateSingleTupleSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#UpdateMultiTupleSet.
    def enterUpdateMultiTupleSet(self, ctx:o9IBPLParser.UpdateMultiTupleSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#UpdateMultiTupleSet.
    def exitUpdateMultiTupleSet(self, ctx:o9IBPLParser.UpdateMultiTupleSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#updateStatementWithImpact.
    def enterUpdateStatementWithImpact(self, ctx:o9IBPLParser.UpdateStatementWithImpactContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#updateStatementWithImpact.
    def exitUpdateStatementWithImpact(self, ctx:o9IBPLParser.UpdateStatementWithImpactContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#respreadStatement.
    def enterRespreadStatement(self, ctx:o9IBPLParser.RespreadStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#respreadStatement.
    def exitRespreadStatement(self, ctx:o9IBPLParser.RespreadStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#respreadStatementWithImpact.
    def enterRespreadStatementWithImpact(self, ctx:o9IBPLParser.RespreadStatementWithImpactContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#respreadStatementWithImpact.
    def exitRespreadStatementWithImpact(self, ctx:o9IBPLParser.RespreadStatementWithImpactContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measure_or_edge_property_update.
    def enterMeasure_or_edge_property_update(self, ctx:o9IBPLParser.Measure_or_edge_property_updateContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measure_or_edge_property_update.
    def exitMeasure_or_edge_property_update(self, ctx:o9IBPLParser.Measure_or_edge_property_updateContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#tuple_cell_assignment.
    def enterTuple_cell_assignment(self, ctx:o9IBPLParser.Tuple_cell_assignmentContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#tuple_cell_assignment.
    def exitTuple_cell_assignment(self, ctx:o9IBPLParser.Tuple_cell_assignmentContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#cell_property_assignment.
    def enterCell_property_assignment(self, ctx:o9IBPLParser.Cell_property_assignmentContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#cell_property_assignment.
    def exitCell_property_assignment(self, ctx:o9IBPLParser.Cell_property_assignmentContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#massUpdateStatement.
    def enterMassUpdateStatement(self, ctx:o9IBPLParser.MassUpdateStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#massUpdateStatement.
    def exitMassUpdateStatement(self, ctx:o9IBPLParser.MassUpdateStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#sanityCheckStatement.
    def enterSanityCheckStatement(self, ctx:o9IBPLParser.SanityCheckStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#sanityCheckStatement.
    def exitSanityCheckStatement(self, ctx:o9IBPLParser.SanityCheckStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GatherColumnStatsForMeasureGroup.
    def enterGatherColumnStatsForMeasureGroup(self, ctx:o9IBPLParser.GatherColumnStatsForMeasureGroupContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GatherColumnStatsForMeasureGroup.
    def exitGatherColumnStatsForMeasureGroup(self, ctx:o9IBPLParser.GatherColumnStatsForMeasureGroupContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#GatherColumnStatsForDimension.
    def enterGatherColumnStatsForDimension(self, ctx:o9IBPLParser.GatherColumnStatsForDimensionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#GatherColumnStatsForDimension.
    def exitGatherColumnStatsForDimension(self, ctx:o9IBPLParser.GatherColumnStatsForDimensionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#explainStatement.
    def enterExplainStatement(self, ctx:o9IBPLParser.ExplainStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#explainStatement.
    def exitExplainStatement(self, ctx:o9IBPLParser.ExplainStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#AmplifyRedo.
    def enterAmplifyRedo(self, ctx:o9IBPLParser.AmplifyRedoContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#AmplifyRedo.
    def exitAmplifyRedo(self, ctx:o9IBPLParser.AmplifyRedoContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#DeleteFactMeasureGroup.
    def enterDeleteFactMeasureGroup(self, ctx:o9IBPLParser.DeleteFactMeasureGroupContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#DeleteFactMeasureGroup.
    def exitDeleteFactMeasureGroup(self, ctx:o9IBPLParser.DeleteFactMeasureGroupContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#DeleteFactMembers.
    def enterDeleteFactMembers(self, ctx:o9IBPLParser.DeleteFactMembersContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#DeleteFactMembers.
    def exitDeleteFactMembers(self, ctx:o9IBPLParser.DeleteFactMembersContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#DeleteGraphEdges.
    def enterDeleteGraphEdges(self, ctx:o9IBPLParser.DeleteGraphEdgesContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#DeleteGraphEdges.
    def exitDeleteGraphEdges(self, ctx:o9IBPLParser.DeleteGraphEdgesContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measureGroupSet.
    def enterMeasureGroupSet(self, ctx:o9IBPLParser.MeasureGroupSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measureGroupSet.
    def exitMeasureGroupSet(self, ctx:o9IBPLParser.MeasureGroupSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measureGroupList.
    def enterMeasureGroupList(self, ctx:o9IBPLParser.MeasureGroupListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measureGroupList.
    def exitMeasureGroupList(self, ctx:o9IBPLParser.MeasureGroupListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphSet.
    def enterGraphSet(self, ctx:o9IBPLParser.GraphSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphSet.
    def exitGraphSet(self, ctx:o9IBPLParser.GraphSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphList.
    def enterGraphList(self, ctx:o9IBPLParser.GraphListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphList.
    def exitGraphList(self, ctx:o9IBPLParser.GraphListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#planList.
    def enterPlanList(self, ctx:o9IBPLParser.PlanListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#planList.
    def exitPlanList(self, ctx:o9IBPLParser.PlanListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#mgAndGraphGroupSet.
    def enterMgAndGraphGroupSet(self, ctx:o9IBPLParser.MgAndGraphGroupSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#mgAndGraphGroupSet.
    def exitMgAndGraphGroupSet(self, ctx:o9IBPLParser.MgAndGraphGroupSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#deleteEdgesFilterClause.
    def enterDeleteEdgesFilterClause(self, ctx:o9IBPLParser.DeleteEdgesFilterClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#deleteEdgesFilterClause.
    def exitDeleteEdgesFilterClause(self, ctx:o9IBPLParser.DeleteEdgesFilterClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#rel_deleteEdgesFilter_expression.
    def enterRel_deleteEdgesFilter_expression(self, ctx:o9IBPLParser.Rel_deleteEdgesFilter_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#rel_deleteEdgesFilter_expression.
    def exitRel_deleteEdgesFilter_expression(self, ctx:o9IBPLParser.Rel_deleteEdgesFilter_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#TruncateMeasureGroup.
    def enterTruncateMeasureGroup(self, ctx:o9IBPLParser.TruncateMeasureGroupContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#TruncateMeasureGroup.
    def exitTruncateMeasureGroup(self, ctx:o9IBPLParser.TruncateMeasureGroupContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#TruncateGraph.
    def enterTruncateGraph(self, ctx:o9IBPLParser.TruncateGraphContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#TruncateGraph.
    def exitTruncateGraph(self, ctx:o9IBPLParser.TruncateGraphContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#flushDataStatement.
    def enterFlushDataStatement(self, ctx:o9IBPLParser.FlushDataStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#flushDataStatement.
    def exitFlushDataStatement(self, ctx:o9IBPLParser.FlushDataStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#nullifyFactStatement.
    def enterNullifyFactStatement(self, ctx:o9IBPLParser.NullifyFactStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#nullifyFactStatement.
    def exitNullifyFactStatement(self, ctx:o9IBPLParser.NullifyFactStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#recurrenceScopeStatement.
    def enterRecurrenceScopeStatement(self, ctx:o9IBPLParser.RecurrenceScopeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#recurrenceScopeStatement.
    def exitRecurrenceScopeStatement(self, ctx:o9IBPLParser.RecurrenceScopeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#insertScopeStatement.
    def enterInsertScopeStatement(self, ctx:o9IBPLParser.InsertScopeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#insertScopeStatement.
    def exitInsertScopeStatement(self, ctx:o9IBPLParser.InsertScopeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#blockScopeStatement.
    def enterBlockScopeStatement(self, ctx:o9IBPLParser.BlockScopeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#blockScopeStatement.
    def exitBlockScopeStatement(self, ctx:o9IBPLParser.BlockScopeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#blockScopeGraphStatement.
    def enterBlockScopeGraphStatement(self, ctx:o9IBPLParser.BlockScopeGraphStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#blockScopeGraphStatement.
    def exitBlockScopeGraphStatement(self, ctx:o9IBPLParser.BlockScopeGraphStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#scopeStatement.
    def enterScopeStatement(self, ctx:o9IBPLParser.ScopeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#scopeStatement.
    def exitScopeStatement(self, ctx:o9IBPLParser.ScopeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#scopePrefix.
    def enterScopePrefix(self, ctx:o9IBPLParser.ScopePrefixContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#scopePrefix.
    def exitScopePrefix(self, ctx:o9IBPLParser.ScopePrefixContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#scopeStatementWithImpact.
    def enterScopeStatementWithImpact(self, ctx:o9IBPLParser.ScopeStatementWithImpactContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#scopeStatementWithImpact.
    def exitScopeStatementWithImpact(self, ctx:o9IBPLParser.ScopeStatementWithImpactContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#scopedGraphEdgePropertyAssignments.
    def enterScopedGraphEdgePropertyAssignments(self, ctx:o9IBPLParser.ScopedGraphEdgePropertyAssignmentsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#scopedGraphEdgePropertyAssignments.
    def exitScopedGraphEdgePropertyAssignments(self, ctx:o9IBPLParser.ScopedGraphEdgePropertyAssignmentsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#vertexScopeForGraphAssignmentStatement.
    def enterVertexScopeForGraphAssignmentStatement(self, ctx:o9IBPLParser.VertexScopeForGraphAssignmentStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#vertexScopeForGraphAssignmentStatement.
    def exitVertexScopeForGraphAssignmentStatement(self, ctx:o9IBPLParser.VertexScopeForGraphAssignmentStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphVersions_expression.
    def enterGraphVersions_expression(self, ctx:o9IBPLParser.GraphVersions_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphVersions_expression.
    def exitGraphVersions_expression(self, ctx:o9IBPLParser.GraphVersions_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#vertexScopeStatement.
    def enterVertexScopeStatement(self, ctx:o9IBPLParser.VertexScopeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#vertexScopeStatement.
    def exitVertexScopeStatement(self, ctx:o9IBPLParser.VertexScopeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#member_expressions_or_expression.
    def enterMember_expressions_or_expression(self, ctx:o9IBPLParser.Member_expressions_or_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#member_expressions_or_expression.
    def exitMember_expressions_or_expression(self, ctx:o9IBPLParser.Member_expressions_or_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphEdgePropertyAssignment.
    def enterGraphEdgePropertyAssignment(self, ctx:o9IBPLParser.GraphEdgePropertyAssignmentContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphEdgePropertyAssignment.
    def exitGraphEdgePropertyAssignment(self, ctx:o9IBPLParser.GraphEdgePropertyAssignmentContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphEdgePropertyUpdate.
    def enterGraphEdgePropertyUpdate(self, ctx:o9IBPLParser.GraphEdgePropertyUpdateContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphEdgePropertyUpdate.
    def exitGraphEdgePropertyUpdate(self, ctx:o9IBPLParser.GraphEdgePropertyUpdateContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphEdgePropertyUpdate_coordinates.
    def enterGraphEdgePropertyUpdate_coordinates(self, ctx:o9IBPLParser.GraphEdgePropertyUpdate_coordinatesContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphEdgePropertyUpdate_coordinates.
    def exitGraphEdgePropertyUpdate_coordinates(self, ctx:o9IBPLParser.GraphEdgePropertyUpdate_coordinatesContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#graphEdgePropertyUpdate_member.
    def enterGraphEdgePropertyUpdate_member(self, ctx:o9IBPLParser.GraphEdgePropertyUpdate_memberContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#graphEdgePropertyUpdate_member.
    def exitGraphEdgePropertyUpdate_member(self, ctx:o9IBPLParser.GraphEdgePropertyUpdate_memberContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#foreachStatement.
    def enterForeachStatement(self, ctx:o9IBPLParser.ForeachStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#foreachStatement.
    def exitForeachStatement(self, ctx:o9IBPLParser.ForeachStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ifStatement.
    def enterIfStatement(self, ctx:o9IBPLParser.IfStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ifStatement.
    def exitIfStatement(self, ctx:o9IBPLParser.IfStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ifStat.
    def enterIfStat(self, ctx:o9IBPLParser.IfStatContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ifStat.
    def exitIfStat(self, ctx:o9IBPLParser.IfStatContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#elseIfStat.
    def enterElseIfStat(self, ctx:o9IBPLParser.ElseIfStatContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#elseIfStat.
    def exitElseIfStat(self, ctx:o9IBPLParser.ElseIfStatContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#elseStat.
    def enterElseStat(self, ctx:o9IBPLParser.ElseStatContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#elseStat.
    def exitElseStat(self, ctx:o9IBPLParser.ElseStatContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#assignment.
    def enterAssignment(self, ctx:o9IBPLParser.AssignmentContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#assignment.
    def exitAssignment(self, ctx:o9IBPLParser.AssignmentContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#edgePropertyAssignment.
    def enterEdgePropertyAssignment(self, ctx:o9IBPLParser.EdgePropertyAssignmentContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#edgePropertyAssignment.
    def exitEdgePropertyAssignment(self, ctx:o9IBPLParser.EdgePropertyAssignmentContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#CreateSetMemberSet.
    def enterCreateSetMemberSet(self, ctx:o9IBPLParser.CreateSetMemberSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#CreateSetMemberSet.
    def exitCreateSetMemberSet(self, ctx:o9IBPLParser.CreateSetMemberSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#CreateSetMemberSetCrossJoin.
    def enterCreateSetMemberSetCrossJoin(self, ctx:o9IBPLParser.CreateSetMemberSetCrossJoinContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#CreateSetMemberSetCrossJoin.
    def exitCreateSetMemberSetCrossJoin(self, ctx:o9IBPLParser.CreateSetMemberSetCrossJoinContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#CreateProcedure.
    def enterCreateProcedure(self, ctx:o9IBPLParser.CreateProcedureContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#CreateProcedure.
    def exitCreateProcedure(self, ctx:o9IBPLParser.CreateProcedureContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#CreateParameterizedProcedure.
    def enterCreateParameterizedProcedure(self, ctx:o9IBPLParser.CreateParameterizedProcedureContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#CreateParameterizedProcedure.
    def exitCreateParameterizedProcedure(self, ctx:o9IBPLParser.CreateParameterizedProcedureContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#sequentialStatement.
    def enterSequentialStatement(self, ctx:o9IBPLParser.SequentialStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#sequentialStatement.
    def exitSequentialStatement(self, ctx:o9IBPLParser.SequentialStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#createFunctionStatement.
    def enterCreateFunctionStatement(self, ctx:o9IBPLParser.CreateFunctionStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#createFunctionStatement.
    def exitCreateFunctionStatement(self, ctx:o9IBPLParser.CreateFunctionStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#execScriptStatement.
    def enterExecScriptStatement(self, ctx:o9IBPLParser.ExecScriptStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#execScriptStatement.
    def exitExecScriptStatement(self, ctx:o9IBPLParser.ExecScriptStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#execProcedureStatement.
    def enterExecProcedureStatement(self, ctx:o9IBPLParser.ExecProcedureStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#execProcedureStatement.
    def exitExecProcedureStatement(self, ctx:o9IBPLParser.ExecProcedureStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#createRelStatement.
    def enterCreateRelStatement(self, ctx:o9IBPLParser.CreateRelStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#createRelStatement.
    def exitCreateRelStatement(self, ctx:o9IBPLParser.CreateRelStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#deleteRelStatement.
    def enterDeleteRelStatement(self, ctx:o9IBPLParser.DeleteRelStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#deleteRelStatement.
    def exitDeleteRelStatement(self, ctx:o9IBPLParser.DeleteRelStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#updateRelAttrStatement.
    def enterUpdateRelAttrStatement(self, ctx:o9IBPLParser.UpdateRelAttrStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#updateRelAttrStatement.
    def exitUpdateRelAttrStatement(self, ctx:o9IBPLParser.UpdateRelAttrStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#getRelAttrStatement.
    def enterGetRelAttrStatement(self, ctx:o9IBPLParser.GetRelAttrStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#getRelAttrStatement.
    def exitGetRelAttrStatement(self, ctx:o9IBPLParser.GetRelAttrStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#enableDisableCaeStatement.
    def enterEnableDisableCaeStatement(self, ctx:o9IBPLParser.EnableDisableCaeStatementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#enableDisableCaeStatement.
    def exitEnableDisableCaeStatement(self, ctx:o9IBPLParser.EnableDisableCaeStatementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#set_modifier.
    def enterSet_modifier(self, ctx:o9IBPLParser.Set_modifierContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#set_modifier.
    def exitSet_modifier(self, ctx:o9IBPLParser.Set_modifierContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#member_exprList.
    def enterMember_exprList(self, ctx:o9IBPLParser.Member_exprListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#member_exprList.
    def exitMember_exprList(self, ctx:o9IBPLParser.Member_exprListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#scalar_exprList.
    def enterScalar_exprList(self, ctx:o9IBPLParser.Scalar_exprListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#scalar_exprList.
    def exitScalar_exprList(self, ctx:o9IBPLParser.Scalar_exprListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#literal_exprSet.
    def enterLiteral_exprSet(self, ctx:o9IBPLParser.Literal_exprSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#literal_exprSet.
    def exitLiteral_exprSet(self, ctx:o9IBPLParser.Literal_exprSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#expression.
    def enterExpression(self, ctx:o9IBPLParser.ExpressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#expression.
    def exitExpression(self, ctx:o9IBPLParser.ExpressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#null_or_scalar_exp.
    def enterNull_or_scalar_exp(self, ctx:o9IBPLParser.Null_or_scalar_expContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#null_or_scalar_exp.
    def exitNull_or_scalar_exp(self, ctx:o9IBPLParser.Null_or_scalar_expContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#scalar_expression.
    def enterScalar_expression(self, ctx:o9IBPLParser.Scalar_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#scalar_expression.
    def exitScalar_expression(self, ctx:o9IBPLParser.Scalar_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#condExpr.
    def enterCondExpr(self, ctx:o9IBPLParser.CondExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#condExpr.
    def exitCondExpr(self, ctx:o9IBPLParser.CondExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#orExpr.
    def enterOrExpr(self, ctx:o9IBPLParser.OrExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#orExpr.
    def exitOrExpr(self, ctx:o9IBPLParser.OrExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#andExpr.
    def enterAndExpr(self, ctx:o9IBPLParser.AndExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#andExpr.
    def exitAndExpr(self, ctx:o9IBPLParser.AndExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#equExpr.
    def enterEquExpr(self, ctx:o9IBPLParser.EquExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#equExpr.
    def exitEquExpr(self, ctx:o9IBPLParser.EquExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#notEquExpr.
    def enterNotEquExpr(self, ctx:o9IBPLParser.NotEquExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#notEquExpr.
    def exitNotEquExpr(self, ctx:o9IBPLParser.NotEquExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#inScalarSetExpr.
    def enterInScalarSetExpr(self, ctx:o9IBPLParser.InScalarSetExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#inScalarSetExpr.
    def exitInScalarSetExpr(self, ctx:o9IBPLParser.InScalarSetExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#RelExprNumeric.
    def enterRelExprNumeric(self, ctx:o9IBPLParser.RelExprNumericContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#RelExprNumeric.
    def exitRelExprNumeric(self, ctx:o9IBPLParser.RelExprNumericContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#RelExprString.
    def enterRelExprString(self, ctx:o9IBPLParser.RelExprStringContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#RelExprString.
    def exitRelExprString(self, ctx:o9IBPLParser.RelExprStringContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#addExpr.
    def enterAddExpr(self, ctx:o9IBPLParser.AddExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#addExpr.
    def exitAddExpr(self, ctx:o9IBPLParser.AddExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#subExpr.
    def enterSubExpr(self, ctx:o9IBPLParser.SubExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#subExpr.
    def exitSubExpr(self, ctx:o9IBPLParser.SubExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#mulExpr.
    def enterMulExpr(self, ctx:o9IBPLParser.MulExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#mulExpr.
    def exitMulExpr(self, ctx:o9IBPLParser.MulExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#divExpr.
    def enterDivExpr(self, ctx:o9IBPLParser.DivExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#divExpr.
    def exitDivExpr(self, ctx:o9IBPLParser.DivExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#modExpr.
    def enterModExpr(self, ctx:o9IBPLParser.ModExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#modExpr.
    def exitModExpr(self, ctx:o9IBPLParser.ModExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#powExpr.
    def enterPowExpr(self, ctx:o9IBPLParser.PowExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#powExpr.
    def exitPowExpr(self, ctx:o9IBPLParser.PowExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#unaryExpr.
    def enterUnaryExpr(self, ctx:o9IBPLParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#unaryExpr.
    def exitUnaryExpr(self, ctx:o9IBPLParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueScalar.
    def enterValueScalar(self, ctx:o9IBPLParser.ValueScalarContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueScalar.
    def exitValueScalar(self, ctx:o9IBPLParser.ValueScalarContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueLiteral.
    def enterValueLiteral(self, ctx:o9IBPLParser.ValueLiteralContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueLiteral.
    def exitValueLiteral(self, ctx:o9IBPLParser.ValueLiteralContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueNamedMember.
    def enterValueNamedMember(self, ctx:o9IBPLParser.ValueNamedMemberContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueNamedMember.
    def exitValueNamedMember(self, ctx:o9IBPLParser.ValueNamedMemberContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueMemberProperty.
    def enterValueMemberProperty(self, ctx:o9IBPLParser.ValueMemberPropertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueMemberProperty.
    def exitValueMemberProperty(self, ctx:o9IBPLParser.ValueMemberPropertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueMeasureProperty.
    def enterValueMeasureProperty(self, ctx:o9IBPLParser.ValueMeasurePropertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueMeasureProperty.
    def exitValueMeasureProperty(self, ctx:o9IBPLParser.ValueMeasurePropertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueMeasure.
    def enterValueMeasure(self, ctx:o9IBPLParser.ValueMeasureContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueMeasure.
    def exitValueMeasure(self, ctx:o9IBPLParser.ValueMeasureContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueTupleComputedAggregateMeasure.
    def enterValueTupleComputedAggregateMeasure(self, ctx:o9IBPLParser.ValueTupleComputedAggregateMeasureContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueTupleComputedAggregateMeasure.
    def exitValueTupleComputedAggregateMeasure(self, ctx:o9IBPLParser.ValueTupleComputedAggregateMeasureContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueFullyQualifiedEdgeProperty.
    def enterValueFullyQualifiedEdgeProperty(self, ctx:o9IBPLParser.ValueFullyQualifiedEdgePropertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueFullyQualifiedEdgeProperty.
    def exitValueFullyQualifiedEdgeProperty(self, ctx:o9IBPLParser.ValueFullyQualifiedEdgePropertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueEdgeProperty.
    def enterValueEdgeProperty(self, ctx:o9IBPLParser.ValueEdgePropertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueEdgeProperty.
    def exitValueEdgeProperty(self, ctx:o9IBPLParser.ValueEdgePropertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueFullyQualifiedEdgePropertyWithVertexCoordinates.
    def enterValueFullyQualifiedEdgePropertyWithVertexCoordinates(self, ctx:o9IBPLParser.ValueFullyQualifiedEdgePropertyWithVertexCoordinatesContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueFullyQualifiedEdgePropertyWithVertexCoordinates.
    def exitValueFullyQualifiedEdgePropertyWithVertexCoordinates(self, ctx:o9IBPLParser.ValueFullyQualifiedEdgePropertyWithVertexCoordinatesContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueEdgeNodeMemberProperty.
    def enterValueEdgeNodeMemberProperty(self, ctx:o9IBPLParser.ValueEdgeNodeMemberPropertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueEdgeNodeMemberProperty.
    def exitValueEdgeNodeMemberProperty(self, ctx:o9IBPLParser.ValueEdgeNodeMemberPropertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueNodeMemberProperty.
    def enterValueNodeMemberProperty(self, ctx:o9IBPLParser.ValueNodeMemberPropertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueNodeMemberProperty.
    def exitValueNodeMemberProperty(self, ctx:o9IBPLParser.ValueNodeMemberPropertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueId.
    def enterValueId(self, ctx:o9IBPLParser.ValueIdContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueId.
    def exitValueId(self, ctx:o9IBPLParser.ValueIdContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#ValueLiteralSet.
    def enterValueLiteralSet(self, ctx:o9IBPLParser.ValueLiteralSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#ValueLiteralSet.
    def exitValueLiteralSet(self, ctx:o9IBPLParser.ValueLiteralSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralNumber.
    def enterLiteralNumber(self, ctx:o9IBPLParser.LiteralNumberContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralNumber.
    def exitLiteralNumber(self, ctx:o9IBPLParser.LiteralNumberContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralBool.
    def enterLiteralBool(self, ctx:o9IBPLParser.LiteralBoolContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralBool.
    def exitLiteralBool(self, ctx:o9IBPLParser.LiteralBoolContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralNull.
    def enterLiteralNull(self, ctx:o9IBPLParser.LiteralNullContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralNull.
    def exitLiteralNull(self, ctx:o9IBPLParser.LiteralNullContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralDateNow.
    def enterLiteralDateNow(self, ctx:o9IBPLParser.LiteralDateNowContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralDateNow.
    def exitLiteralDateNow(self, ctx:o9IBPLParser.LiteralDateNowContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralLastCommitTime.
    def enterLiteralLastCommitTime(self, ctx:o9IBPLParser.LiteralLastCommitTimeContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralLastCommitTime.
    def exitLiteralLastCommitTime(self, ctx:o9IBPLParser.LiteralLastCommitTimeContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralLastUpdateTime.
    def enterLiteralLastUpdateTime(self, ctx:o9IBPLParser.LiteralLastUpdateTimeContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralLastUpdateTime.
    def exitLiteralLastUpdateTime(self, ctx:o9IBPLParser.LiteralLastUpdateTimeContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralToDateTime.
    def enterLiteralToDateTime(self, ctx:o9IBPLParser.LiteralToDateTimeContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralToDateTime.
    def exitLiteralToDateTime(self, ctx:o9IBPLParser.LiteralToDateTimeContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralDateAdd.
    def enterLiteralDateAdd(self, ctx:o9IBPLParser.LiteralDateAddContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralDateAdd.
    def exitLiteralDateAdd(self, ctx:o9IBPLParser.LiteralDateAddContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralDateDiff.
    def enterLiteralDateDiff(self, ctx:o9IBPLParser.LiteralDateDiffContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralDateDiff.
    def exitLiteralDateDiff(self, ctx:o9IBPLParser.LiteralDateDiffContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralNextCount.
    def enterLiteralNextCount(self, ctx:o9IBPLParser.LiteralNextCountContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralNextCount.
    def exitLiteralNextCount(self, ctx:o9IBPLParser.LiteralNextCountContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralNextLabel.
    def enterLiteralNextLabel(self, ctx:o9IBPLParser.LiteralNextLabelContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralNextLabel.
    def exitLiteralNextLabel(self, ctx:o9IBPLParser.LiteralNextLabelContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralAbs.
    def enterLiteralAbs(self, ctx:o9IBPLParser.LiteralAbsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralAbs.
    def exitLiteralAbs(self, ctx:o9IBPLParser.LiteralAbsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralCeiling.
    def enterLiteralCeiling(self, ctx:o9IBPLParser.LiteralCeilingContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralCeiling.
    def exitLiteralCeiling(self, ctx:o9IBPLParser.LiteralCeilingContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralDiv.
    def enterLiteralDiv(self, ctx:o9IBPLParser.LiteralDivContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralDiv.
    def exitLiteralDiv(self, ctx:o9IBPLParser.LiteralDivContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralFloor.
    def enterLiteralFloor(self, ctx:o9IBPLParser.LiteralFloorContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralFloor.
    def exitLiteralFloor(self, ctx:o9IBPLParser.LiteralFloorContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralFloat.
    def enterLiteralFloat(self, ctx:o9IBPLParser.LiteralFloatContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralFloat.
    def exitLiteralFloat(self, ctx:o9IBPLParser.LiteralFloatContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralInteger.
    def enterLiteralInteger(self, ctx:o9IBPLParser.LiteralIntegerContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralInteger.
    def exitLiteralInteger(self, ctx:o9IBPLParser.LiteralIntegerContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralToString.
    def enterLiteralToString(self, ctx:o9IBPLParser.LiteralToStringContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralToString.
    def exitLiteralToString(self, ctx:o9IBPLParser.LiteralToStringContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralUpper.
    def enterLiteralUpper(self, ctx:o9IBPLParser.LiteralUpperContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralUpper.
    def exitLiteralUpper(self, ctx:o9IBPLParser.LiteralUpperContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralLower.
    def enterLiteralLower(self, ctx:o9IBPLParser.LiteralLowerContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralLower.
    def exitLiteralLower(self, ctx:o9IBPLParser.LiteralLowerContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralLog.
    def enterLiteralLog(self, ctx:o9IBPLParser.LiteralLogContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralLog.
    def exitLiteralLog(self, ctx:o9IBPLParser.LiteralLogContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralExponential.
    def enterLiteralExponential(self, ctx:o9IBPLParser.LiteralExponentialContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralExponential.
    def exitLiteralExponential(self, ctx:o9IBPLParser.LiteralExponentialContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralPow.
    def enterLiteralPow(self, ctx:o9IBPLParser.LiteralPowContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralPow.
    def exitLiteralPow(self, ctx:o9IBPLParser.LiteralPowContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralRandom.
    def enterLiteralRandom(self, ctx:o9IBPLParser.LiteralRandomContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralRandom.
    def exitLiteralRandom(self, ctx:o9IBPLParser.LiteralRandomContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralRound.
    def enterLiteralRound(self, ctx:o9IBPLParser.LiteralRoundContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralRound.
    def exitLiteralRound(self, ctx:o9IBPLParser.LiteralRoundContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralSum.
    def enterLiteralSum(self, ctx:o9IBPLParser.LiteralSumContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralSum.
    def exitLiteralSum(self, ctx:o9IBPLParser.LiteralSumContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralSumProduct.
    def enterLiteralSumProduct(self, ctx:o9IBPLParser.LiteralSumProductContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralSumProduct.
    def exitLiteralSumProduct(self, ctx:o9IBPLParser.LiteralSumProductContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralAvg.
    def enterLiteralAvg(self, ctx:o9IBPLParser.LiteralAvgContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralAvg.
    def exitLiteralAvg(self, ctx:o9IBPLParser.LiteralAvgContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralAvgWithNulls.
    def enterLiteralAvgWithNulls(self, ctx:o9IBPLParser.LiteralAvgWithNullsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralAvgWithNulls.
    def exitLiteralAvgWithNulls(self, ctx:o9IBPLParser.LiteralAvgWithNullsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralCorrel.
    def enterLiteralCorrel(self, ctx:o9IBPLParser.LiteralCorrelContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralCorrel.
    def exitLiteralCorrel(self, ctx:o9IBPLParser.LiteralCorrelContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralCount.
    def enterLiteralCount(self, ctx:o9IBPLParser.LiteralCountContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralCount.
    def exitLiteralCount(self, ctx:o9IBPLParser.LiteralCountContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralMin.
    def enterLiteralMin(self, ctx:o9IBPLParser.LiteralMinContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralMin.
    def exitLiteralMin(self, ctx:o9IBPLParser.LiteralMinContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralMax.
    def enterLiteralMax(self, ctx:o9IBPLParser.LiteralMaxContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralMax.
    def exitLiteralMax(self, ctx:o9IBPLParser.LiteralMaxContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralConcat.
    def enterLiteralConcat(self, ctx:o9IBPLParser.LiteralConcatContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralConcat.
    def exitLiteralConcat(self, ctx:o9IBPLParser.LiteralConcatContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralLength.
    def enterLiteralLength(self, ctx:o9IBPLParser.LiteralLengthContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralLength.
    def exitLiteralLength(self, ctx:o9IBPLParser.LiteralLengthContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralLen.
    def enterLiteralLen(self, ctx:o9IBPLParser.LiteralLenContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralLen.
    def exitLiteralLen(self, ctx:o9IBPLParser.LiteralLenContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralLeft.
    def enterLiteralLeft(self, ctx:o9IBPLParser.LiteralLeftContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralLeft.
    def exitLiteralLeft(self, ctx:o9IBPLParser.LiteralLeftContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralRight.
    def enterLiteralRight(self, ctx:o9IBPLParser.LiteralRightContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralRight.
    def exitLiteralRight(self, ctx:o9IBPLParser.LiteralRightContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralMid.
    def enterLiteralMid(self, ctx:o9IBPLParser.LiteralMidContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralMid.
    def exitLiteralMid(self, ctx:o9IBPLParser.LiteralMidContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralCoalesce.
    def enterLiteralCoalesce(self, ctx:o9IBPLParser.LiteralCoalesceContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralCoalesce.
    def exitLiteralCoalesce(self, ctx:o9IBPLParser.LiteralCoalesceContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralIfThen.
    def enterLiteralIfThen(self, ctx:o9IBPLParser.LiteralIfThenContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralIfThen.
    def exitLiteralIfThen(self, ctx:o9IBPLParser.LiteralIfThenContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralMemberCount.
    def enterLiteralMemberCount(self, ctx:o9IBPLParser.LiteralMemberCountContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralMemberCount.
    def exitLiteralMemberCount(self, ctx:o9IBPLParser.LiteralMemberCountContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralMemberIndex.
    def enterLiteralMemberIndex(self, ctx:o9IBPLParser.LiteralMemberIndexContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralMemberIndex.
    def exitLiteralMemberIndex(self, ctx:o9IBPLParser.LiteralMemberIndexContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralGetValue.
    def enterLiteralGetValue(self, ctx:o9IBPLParser.LiteralGetValueContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralGetValue.
    def exitLiteralGetValue(self, ctx:o9IBPLParser.LiteralGetValueContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralARGB.
    def enterLiteralARGB(self, ctx:o9IBPLParser.LiteralARGBContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralARGB.
    def exitLiteralARGB(self, ctx:o9IBPLParser.LiteralARGBContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralIsNull.
    def enterLiteralIsNull(self, ctx:o9IBPLParser.LiteralIsNullContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralIsNull.
    def exitLiteralIsNull(self, ctx:o9IBPLParser.LiteralIsNullContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralIsEmpty.
    def enterLiteralIsEmpty(self, ctx:o9IBPLParser.LiteralIsEmptyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralIsEmpty.
    def exitLiteralIsEmpty(self, ctx:o9IBPLParser.LiteralIsEmptyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralIsWhiteSpace.
    def enterLiteralIsWhiteSpace(self, ctx:o9IBPLParser.LiteralIsWhiteSpaceContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralIsWhiteSpace.
    def exitLiteralIsWhiteSpace(self, ctx:o9IBPLParser.LiteralIsWhiteSpaceContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralSafeDivide.
    def enterLiteralSafeDivide(self, ctx:o9IBPLParser.LiteralSafeDivideContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralSafeDivide.
    def exitLiteralSafeDivide(self, ctx:o9IBPLParser.LiteralSafeDivideContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#LiteralSubString.
    def enterLiteralSubString(self, ctx:o9IBPLParser.LiteralSubStringContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#LiteralSubString.
    def exitLiteralSubString(self, ctx:o9IBPLParser.LiteralSubStringContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#distinct.
    def enterDistinct(self, ctx:o9IBPLParser.DistinctContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#distinct.
    def exitDistinct(self, ctx:o9IBPLParser.DistinctContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#member_measure_crossjoin.
    def enterMember_measure_crossjoin(self, ctx:o9IBPLParser.Member_measure_crossjoinContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#member_measure_crossjoin.
    def exitMember_measure_crossjoin(self, ctx:o9IBPLParser.Member_measure_crossjoinContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#CrossJoinMembers.
    def enterCrossJoinMembers(self, ctx:o9IBPLParser.CrossJoinMembersContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#CrossJoinMembers.
    def exitCrossJoinMembers(self, ctx:o9IBPLParser.CrossJoinMembersContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#CrossJoinMember.
    def enterCrossJoinMember(self, ctx:o9IBPLParser.CrossJoinMemberContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#CrossJoinMember.
    def exitCrossJoinMember(self, ctx:o9IBPLParser.CrossJoinMemberContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#CrossJoinGraphNode.
    def enterCrossJoinGraphNode(self, ctx:o9IBPLParser.CrossJoinGraphNodeContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#CrossJoinGraphNode.
    def exitCrossJoinGraphNode(self, ctx:o9IBPLParser.CrossJoinGraphNodeContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#CrossJoinMeasure.
    def enterCrossJoinMeasure(self, ctx:o9IBPLParser.CrossJoinMeasureContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#CrossJoinMeasure.
    def exitCrossJoinMeasure(self, ctx:o9IBPLParser.CrossJoinMeasureContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#NamedNodeReference.
    def enterNamedNodeReference(self, ctx:o9IBPLParser.NamedNodeReferenceContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#NamedNodeReference.
    def exitNamedNodeReference(self, ctx:o9IBPLParser.NamedNodeReferenceContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#NamedNodeFilterSetReference.
    def enterNamedNodeFilterSetReference(self, ctx:o9IBPLParser.NamedNodeFilterSetReferenceContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#NamedNodeFilterSetReference.
    def exitNamedNodeFilterSetReference(self, ctx:o9IBPLParser.NamedNodeFilterSetReferenceContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#NamedNodeGraphReference.
    def enterNamedNodeGraphReference(self, ctx:o9IBPLParser.NamedNodeGraphReferenceContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#NamedNodeGraphReference.
    def exitNamedNodeGraphReference(self, ctx:o9IBPLParser.NamedNodeGraphReferenceContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#NamedNodeFilterSetGraphReference.
    def enterNamedNodeFilterSetGraphReference(self, ctx:o9IBPLParser.NamedNodeFilterSetGraphReferenceContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#NamedNodeFilterSetGraphReference.
    def exitNamedNodeFilterSetGraphReference(self, ctx:o9IBPLParser.NamedNodeFilterSetGraphReferenceContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#multifilter_clause.
    def enterMultifilter_clause(self, ctx:o9IBPLParser.Multifilter_clauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#multifilter_clause.
    def exitMultifilter_clause(self, ctx:o9IBPLParser.Multifilter_clauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#namedNode_Filter_clause.
    def enterNamedNode_Filter_clause(self, ctx:o9IBPLParser.NamedNode_Filter_clauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#namedNode_Filter_clause.
    def exitNamedNode_Filter_clause(self, ctx:o9IBPLParser.NamedNode_Filter_clauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#member_crossjoin.
    def enterMember_crossjoin(self, ctx:o9IBPLParser.Member_crossjoinContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#member_crossjoin.
    def exitMember_crossjoin(self, ctx:o9IBPLParser.Member_crossjoinContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberMeta.
    def enterMemberMeta(self, ctx:o9IBPLParser.MemberMetaContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberMeta.
    def exitMemberMeta(self, ctx:o9IBPLParser.MemberMetaContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberPrevMember.
    def enterMemberPrevMember(self, ctx:o9IBPLParser.MemberPrevMemberContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberPrevMember.
    def exitMemberPrevMember(self, ctx:o9IBPLParser.MemberPrevMemberContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberDescendantsAtLevel.
    def enterMemberDescendantsAtLevel(self, ctx:o9IBPLParser.MemberDescendantsAtLevelContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberDescendantsAtLevel.
    def exitMemberDescendantsAtLevel(self, ctx:o9IBPLParser.MemberDescendantsAtLevelContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberFind.
    def enterMemberFind(self, ctx:o9IBPLParser.MemberFindContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberFind.
    def exitMemberFind(self, ctx:o9IBPLParser.MemberFindContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberLeadOffset.
    def enterMemberLeadOffset(self, ctx:o9IBPLParser.MemberLeadOffsetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberLeadOffset.
    def exitMemberLeadOffset(self, ctx:o9IBPLParser.MemberLeadOffsetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberCurrentUser.
    def enterMemberCurrentUser(self, ctx:o9IBPLParser.MemberCurrentUserContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberCurrentUser.
    def exitMemberCurrentUser(self, ctx:o9IBPLParser.MemberCurrentUserContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberAncestorsAtLevel.
    def enterMemberAncestorsAtLevel(self, ctx:o9IBPLParser.MemberAncestorsAtLevelContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberAncestorsAtLevel.
    def exitMemberAncestorsAtLevel(self, ctx:o9IBPLParser.MemberAncestorsAtLevelContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberFirstOrDefault.
    def enterMemberFirstOrDefault(self, ctx:o9IBPLParser.MemberFirstOrDefaultContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberFirstOrDefault.
    def exitMemberFirstOrDefault(self, ctx:o9IBPLParser.MemberFirstOrDefaultContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberFirstElement.
    def enterMemberFirstElement(self, ctx:o9IBPLParser.MemberFirstElementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberFirstElement.
    def exitMemberFirstElement(self, ctx:o9IBPLParser.MemberFirstElementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberChildren.
    def enterMemberChildren(self, ctx:o9IBPLParser.MemberChildrenContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberChildren.
    def exitMemberChildren(self, ctx:o9IBPLParser.MemberChildrenContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberNextMember.
    def enterMemberNextMember(self, ctx:o9IBPLParser.MemberNextMemberContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberNextMember.
    def exitMemberNextMember(self, ctx:o9IBPLParser.MemberNextMemberContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberDifference.
    def enterMemberDifference(self, ctx:o9IBPLParser.MemberDifferenceContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberDifference.
    def exitMemberDifference(self, ctx:o9IBPLParser.MemberDifferenceContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberIntersect.
    def enterMemberIntersect(self, ctx:o9IBPLParser.MemberIntersectContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberIntersect.
    def exitMemberIntersect(self, ctx:o9IBPLParser.MemberIntersectContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberList.
    def enterMemberList(self, ctx:o9IBPLParser.MemberListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberList.
    def exitMemberList(self, ctx:o9IBPLParser.MemberListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#CurrentVertexCoordinateMember.
    def enterCurrentVertexCoordinateMember(self, ctx:o9IBPLParser.CurrentVertexCoordinateMemberContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#CurrentVertexCoordinateMember.
    def exitCurrentVertexCoordinateMember(self, ctx:o9IBPLParser.CurrentVertexCoordinateMemberContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberOrderBy.
    def enterMemberOrderBy(self, ctx:o9IBPLParser.MemberOrderByContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberOrderBy.
    def exitMemberOrderBy(self, ctx:o9IBPLParser.MemberOrderByContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberUnion.
    def enterMemberUnion(self, ctx:o9IBPLParser.MemberUnionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberUnion.
    def exitMemberUnion(self, ctx:o9IBPLParser.MemberUnionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberRelatedMembers.
    def enterMemberRelatedMembers(self, ctx:o9IBPLParser.MemberRelatedMembersContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberRelatedMembers.
    def exitMemberRelatedMembers(self, ctx:o9IBPLParser.MemberRelatedMembersContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberFindWithKey.
    def enterMemberFindWithKey(self, ctx:o9IBPLParser.MemberFindWithKeyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberFindWithKey.
    def exitMemberFindWithKey(self, ctx:o9IBPLParser.MemberFindWithKeyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberAncestors.
    def enterMemberAncestors(self, ctx:o9IBPLParser.MemberAncestorsContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberAncestors.
    def exitMemberAncestors(self, ctx:o9IBPLParser.MemberAncestorsContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberUnoperatedSet.
    def enterMemberUnoperatedSet(self, ctx:o9IBPLParser.MemberUnoperatedSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberUnoperatedSet.
    def exitMemberUnoperatedSet(self, ctx:o9IBPLParser.MemberUnoperatedSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberLastElement.
    def enterMemberLastElement(self, ctx:o9IBPLParser.MemberLastElementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberLastElement.
    def exitMemberLastElement(self, ctx:o9IBPLParser.MemberLastElementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberAncestor.
    def enterMemberAncestor(self, ctx:o9IBPLParser.MemberAncestorContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberAncestor.
    def exitMemberAncestor(self, ctx:o9IBPLParser.MemberAncestorContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberLevelAttribute.
    def enterMemberLevelAttribute(self, ctx:o9IBPLParser.MemberLevelAttributeContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberLevelAttribute.
    def exitMemberLevelAttribute(self, ctx:o9IBPLParser.MemberLevelAttributeContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberUnoperated.
    def enterMemberUnoperated(self, ctx:o9IBPLParser.MemberUnoperatedContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberUnoperated.
    def exitMemberUnoperated(self, ctx:o9IBPLParser.MemberUnoperatedContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberFilter.
    def enterMemberFilter(self, ctx:o9IBPLParser.MemberFilterContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberFilter.
    def exitMemberFilter(self, ctx:o9IBPLParser.MemberFilterContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberElement.
    def enterMemberElement(self, ctx:o9IBPLParser.MemberElementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberElement.
    def exitMemberElement(self, ctx:o9IBPLParser.MemberElementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberBetween.
    def enterMemberBetween(self, ctx:o9IBPLParser.MemberBetweenContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberBetween.
    def exitMemberBetween(self, ctx:o9IBPLParser.MemberBetweenContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#unoperated_member.
    def enterUnoperated_member(self, ctx:o9IBPLParser.Unoperated_memberContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#unoperated_member.
    def exitUnoperated_member(self, ctx:o9IBPLParser.Unoperated_memberContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#current_vertex_coordinate_member.
    def enterCurrent_vertex_coordinate_member(self, ctx:o9IBPLParser.Current_vertex_coordinate_memberContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#current_vertex_coordinate_member.
    def exitCurrent_vertex_coordinate_member(self, ctx:o9IBPLParser.Current_vertex_coordinate_memberContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberSetReference.
    def enterMemberSetReference(self, ctx:o9IBPLParser.MemberSetReferenceContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberSetReference.
    def exitMemberSetReference(self, ctx:o9IBPLParser.MemberSetReferenceContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#MemberArgument.
    def enterMemberArgument(self, ctx:o9IBPLParser.MemberArgumentContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#MemberArgument.
    def exitMemberArgument(self, ctx:o9IBPLParser.MemberArgumentContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#HierarchyLeafMembers.
    def enterHierarchyLeafMembers(self, ctx:o9IBPLParser.HierarchyLeafMembersContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#HierarchyLeafMembers.
    def exitHierarchyLeafMembers(self, ctx:o9IBPLParser.HierarchyLeafMembersContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#HierarchyMembers.
    def enterHierarchyMembers(self, ctx:o9IBPLParser.HierarchyMembersContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#HierarchyMembers.
    def exitHierarchyMembers(self, ctx:o9IBPLParser.HierarchyMembersContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#AttributeMemberSet.
    def enterAttributeMemberSet(self, ctx:o9IBPLParser.AttributeMemberSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#AttributeMemberSet.
    def exitAttributeMemberSet(self, ctx:o9IBPLParser.AttributeMemberSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#AttributeMemberSetFromGraphNode.
    def enterAttributeMemberSetFromGraphNode(self, ctx:o9IBPLParser.AttributeMemberSetFromGraphNodeContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#AttributeMemberSetFromGraphNode.
    def exitAttributeMemberSetFromGraphNode(self, ctx:o9IBPLParser.AttributeMemberSetFromGraphNodeContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#current_member_expression.
    def enterCurrent_member_expression(self, ctx:o9IBPLParser.Current_member_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#current_member_expression.
    def exitCurrent_member_expression(self, ctx:o9IBPLParser.Current_member_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#named_member_expression.
    def enterNamed_member_expression(self, ctx:o9IBPLParser.Named_member_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#named_member_expression.
    def exitNamed_member_expression(self, ctx:o9IBPLParser.Named_member_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#member_property.
    def enterMember_property(self, ctx:o9IBPLParser.Member_propertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#member_property.
    def exitMember_property(self, ctx:o9IBPLParser.Member_propertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#meta_element.
    def enterMeta_element(self, ctx:o9IBPLParser.Meta_elementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#meta_element.
    def exitMeta_element(self, ctx:o9IBPLParser.Meta_elementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#meta_member_property.
    def enterMeta_member_property(self, ctx:o9IBPLParser.Meta_member_propertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#meta_member_property.
    def exitMeta_member_property(self, ctx:o9IBPLParser.Meta_member_propertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#metaMemberIn.
    def enterMetaMemberIn(self, ctx:o9IBPLParser.MetaMemberInContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#metaMemberIn.
    def exitMetaMemberIn(self, ctx:o9IBPLParser.MetaMemberInContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#metaMember.
    def enterMetaMember(self, ctx:o9IBPLParser.MetaMemberContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#metaMember.
    def exitMetaMember(self, ctx:o9IBPLParser.MetaMemberContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#dimension.
    def enterDimension(self, ctx:o9IBPLParser.DimensionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#dimension.
    def exitDimension(self, ctx:o9IBPLParser.DimensionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#dimensionSet.
    def enterDimensionSet(self, ctx:o9IBPLParser.DimensionSetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#dimensionSet.
    def exitDimensionSet(self, ctx:o9IBPLParser.DimensionSetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#dimensionList.
    def enterDimensionList(self, ctx:o9IBPLParser.DimensionListContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#dimensionList.
    def exitDimensionList(self, ctx:o9IBPLParser.DimensionListContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#dimension_name.
    def enterDimension_name(self, ctx:o9IBPLParser.Dimension_nameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#dimension_name.
    def exitDimension_name(self, ctx:o9IBPLParser.Dimension_nameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#dimension_expression.
    def enterDimension_expression(self, ctx:o9IBPLParser.Dimension_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#dimension_expression.
    def exitDimension_expression(self, ctx:o9IBPLParser.Dimension_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#hierarchy.
    def enterHierarchy(self, ctx:o9IBPLParser.HierarchyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#hierarchy.
    def exitHierarchy(self, ctx:o9IBPLParser.HierarchyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#levelattribute.
    def enterLevelattribute(self, ctx:o9IBPLParser.LevelattributeContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#levelattribute.
    def exitLevelattribute(self, ctx:o9IBPLParser.LevelattributeContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#levelattribute_name.
    def enterLevelattribute_name(self, ctx:o9IBPLParser.Levelattribute_nameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#levelattribute_name.
    def exitLevelattribute_name(self, ctx:o9IBPLParser.Levelattribute_nameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#levelattribute_expression.
    def enterLevelattribute_expression(self, ctx:o9IBPLParser.Levelattribute_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#levelattribute_expression.
    def exitLevelattribute_expression(self, ctx:o9IBPLParser.Levelattribute_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#meta_levelattribute_name.
    def enterMeta_levelattribute_name(self, ctx:o9IBPLParser.Meta_levelattribute_nameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#meta_levelattribute_name.
    def exitMeta_levelattribute_name(self, ctx:o9IBPLParser.Meta_levelattribute_nameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#plan_name.
    def enterPlan_name(self, ctx:o9IBPLParser.Plan_nameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#plan_name.
    def exitPlan_name(self, ctx:o9IBPLParser.Plan_nameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measure_group_name.
    def enterMeasure_group_name(self, ctx:o9IBPLParser.Measure_group_nameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measure_group_name.
    def exitMeasure_group_name(self, ctx:o9IBPLParser.Measure_group_nameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#unqualified_measure_name.
    def enterUnqualified_measure_name(self, ctx:o9IBPLParser.Unqualified_measure_nameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#unqualified_measure_name.
    def exitUnqualified_measure_name(self, ctx:o9IBPLParser.Unqualified_measure_nameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measure_element_list.
    def enterMeasure_element_list(self, ctx:o9IBPLParser.Measure_element_listContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measure_element_list.
    def exitMeasure_element_list(self, ctx:o9IBPLParser.Measure_element_listContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measure_element.
    def enterMeasure_element(self, ctx:o9IBPLParser.Measure_elementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measure_element.
    def exitMeasure_element(self, ctx:o9IBPLParser.Measure_elementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#simple_measure_element.
    def enterSimple_measure_element(self, ctx:o9IBPLParser.Simple_measure_elementContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#simple_measure_element.
    def exitSimple_measure_element(self, ctx:o9IBPLParser.Simple_measure_elementContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measure.
    def enterMeasure(self, ctx:o9IBPLParser.MeasureContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measure.
    def exitMeasure(self, ctx:o9IBPLParser.MeasureContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measure_name.
    def enterMeasure_name(self, ctx:o9IBPLParser.Measure_nameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measure_name.
    def exitMeasure_name(self, ctx:o9IBPLParser.Measure_nameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#transient_measure_name.
    def enterTransient_measure_name(self, ctx:o9IBPLParser.Transient_measure_nameContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#transient_measure_name.
    def exitTransient_measure_name(self, ctx:o9IBPLParser.Transient_measure_nameContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#computed_plugin_measure.
    def enterComputed_plugin_measure(self, ctx:o9IBPLParser.Computed_plugin_measureContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#computed_plugin_measure.
    def exitComputed_plugin_measure(self, ctx:o9IBPLParser.Computed_plugin_measureContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#usingArgsScopeClause.
    def enterUsingArgsScopeClause(self, ctx:o9IBPLParser.UsingArgsScopeClauseContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#usingArgsScopeClause.
    def exitUsingArgsScopeClause(self, ctx:o9IBPLParser.UsingArgsScopeClauseContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#CumulativeMeasure.
    def enterCumulativeMeasure(self, ctx:o9IBPLParser.CumulativeMeasureContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#CumulativeMeasure.
    def exitCumulativeMeasure(self, ctx:o9IBPLParser.CumulativeMeasureContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#transient_computed_measure.
    def enterTransient_computed_measure(self, ctx:o9IBPLParser.Transient_computed_measureContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#transient_computed_measure.
    def exitTransient_computed_measure(self, ctx:o9IBPLParser.Transient_computed_measureContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#tuple_aggregate_measure.
    def enterTuple_aggregate_measure(self, ctx:o9IBPLParser.Tuple_aggregate_measureContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#tuple_aggregate_measure.
    def exitTuple_aggregate_measure(self, ctx:o9IBPLParser.Tuple_aggregate_measureContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#tuple_agg_measure_crossjoin.
    def enterTuple_agg_measure_crossjoin(self, ctx:o9IBPLParser.Tuple_agg_measure_crossjoinContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#tuple_agg_measure_crossjoin.
    def exitTuple_agg_measure_crossjoin(self, ctx:o9IBPLParser.Tuple_agg_measure_crossjoinContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#tuple_computed_aggregate_measure.
    def enterTuple_computed_aggregate_measure(self, ctx:o9IBPLParser.Tuple_computed_aggregate_measureContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#tuple_computed_aggregate_measure.
    def exitTuple_computed_aggregate_measure(self, ctx:o9IBPLParser.Tuple_computed_aggregate_measureContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measure_with_scope_or_graph_coordinates.
    def enterMeasure_with_scope_or_graph_coordinates(self, ctx:o9IBPLParser.Measure_with_scope_or_graph_coordinatesContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measure_with_scope_or_graph_coordinates.
    def exitMeasure_with_scope_or_graph_coordinates(self, ctx:o9IBPLParser.Measure_with_scope_or_graph_coordinatesContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#vertex_coordinate.
    def enterVertex_coordinate(self, ctx:o9IBPLParser.Vertex_coordinateContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#vertex_coordinate.
    def exitVertex_coordinate(self, ctx:o9IBPLParser.Vertex_coordinateContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#vertex_coordinate_target.
    def enterVertex_coordinate_target(self, ctx:o9IBPLParser.Vertex_coordinate_targetContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#vertex_coordinate_target.
    def exitVertex_coordinate_target(self, ctx:o9IBPLParser.Vertex_coordinate_targetContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#namenode_expression.
    def enterNamenode_expression(self, ctx:o9IBPLParser.Namenode_expressionContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#namenode_expression.
    def exitNamenode_expression(self, ctx:o9IBPLParser.Namenode_expressionContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#measure_property.
    def enterMeasure_property(self, ctx:o9IBPLParser.Measure_propertyContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#measure_property.
    def exitMeasure_property(self, ctx:o9IBPLParser.Measure_propertyContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#cell_properties.
    def enterCell_properties(self, ctx:o9IBPLParser.Cell_propertiesContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#cell_properties.
    def exitCell_properties(self, ctx:o9IBPLParser.Cell_propertiesContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#node_properties.
    def enterNode_properties(self, ctx:o9IBPLParser.Node_propertiesContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#node_properties.
    def exitNode_properties(self, ctx:o9IBPLParser.Node_propertiesContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#tuple_aggregation_meas_func.
    def enterTuple_aggregation_meas_func(self, ctx:o9IBPLParser.Tuple_aggregation_meas_funcContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#tuple_aggregation_meas_func.
    def exitTuple_aggregation_meas_func(self, ctx:o9IBPLParser.Tuple_aggregation_meas_funcContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#String.
    def enterString(self, ctx:o9IBPLParser.StringContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#String.
    def exitString(self, ctx:o9IBPLParser.StringContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#Argument.
    def enterArgument(self, ctx:o9IBPLParser.ArgumentContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#Argument.
    def exitArgument(self, ctx:o9IBPLParser.ArgumentContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#QuotedId.
    def enterQuotedId(self, ctx:o9IBPLParser.QuotedIdContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#QuotedId.
    def exitQuotedId(self, ctx:o9IBPLParser.QuotedIdContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#Id.
    def enterId(self, ctx:o9IBPLParser.IdContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#Id.
    def exitId(self, ctx:o9IBPLParser.IdContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#PositiveInt.
    def enterPositiveInt(self, ctx:o9IBPLParser.PositiveIntContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#PositiveInt.
    def exitPositiveInt(self, ctx:o9IBPLParser.PositiveIntContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#NegInteger.
    def enterNegInteger(self, ctx:o9IBPLParser.NegIntegerContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#NegInteger.
    def exitNegInteger(self, ctx:o9IBPLParser.NegIntegerContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#Integer.
    def enterInteger(self, ctx:o9IBPLParser.IntegerContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#Integer.
    def exitInteger(self, ctx:o9IBPLParser.IntegerContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#NegDecimal.
    def enterNegDecimal(self, ctx:o9IBPLParser.NegDecimalContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#NegDecimal.
    def exitNegDecimal(self, ctx:o9IBPLParser.NegDecimalContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#Decimal.
    def enterDecimal(self, ctx:o9IBPLParser.DecimalContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#Decimal.
    def exitDecimal(self, ctx:o9IBPLParser.DecimalContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#TrueBool.
    def enterTrueBool(self, ctx:o9IBPLParser.TrueBoolContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#TrueBool.
    def exitTrueBool(self, ctx:o9IBPLParser.TrueBoolContext):
        pass


    # Enter a parse tree produced by o9IBPLParser#FalseBool.
    def enterFalseBool(self, ctx:o9IBPLParser.FalseBoolContext):
        pass

    # Exit a parse tree produced by o9IBPLParser#FalseBool.
    def exitFalseBool(self, ctx:o9IBPLParser.FalseBoolContext):
        pass



del o9IBPLParser