grammar o9IBPL;

@lexer::members {
    // Helper to determine if the current double-brace block is a simple template
    private bool IsSimpleTemplate()
	{
		const int maxLookahead = 10000;
		int i = 1;
		while (i < maxLookahead)
		{
			int lookahead = InputStream.LA(i);

			if (lookahead == Antlr4.Runtime.IntStreamConstants.EOF) return false;

			if (lookahead == '}' && InputStream.LA(i + 1) == '}') return true;

			char c = (char)lookahead;
			// If any structural/functional character is found, it's NOT a template
			if (c == '[' || c == '"' || c == '.' || c == ',')
			{
				return false;
			}
			i++;
		}
		return false;
	}
}


options {
	language=CSharp;
}

@lexer::header {
}

@parser::header{
}

block
	: statement+
	;


statement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: spreadSelectCrossJoinStatement SEMICOLON
	| selectMemberExprStatement SEMICOLON
	| selectGraphEdgeProjectStatement SEMICOLON
	| selectGraphEdgesStatement SEMICOLON
	| selectGraphPathsStatement SEMICOLON
	| selectDimensionGraphEdgesStatement SEMICOLON
	| blockStatement SEMICOLON
	| execParallelStatement SEMICOLON
	| createSetStatement SEMICOLON
	| createProcStatement SEMICOLON
	| createFunctionStatement SEMICOLON
	| createRelStatement SEMICOLON
	| deleteRelStatement SEMICOLON
	| updateRelAttrStatement SEMICOLON
	| getRelAttrStatement SEMICOLON
	| scopeStatement SEMICOLON
	| recurrenceScopeStatement SEMICOLON
	| blockScopeGraphStatement SEMICOLON
	| blockScopeStatement SEMICOLON
	| insertScopeStatement SEMICOLON
	| scopeStatementWithImpact SEMICOLON
	| scopedGraphEdgePropertyAssignments SEMICOLON
	| updateStatement SEMICOLON
	| updateStatementWithImpact SEMICOLON
	| foreachStatement SEMICOLON
	| massUpdateStatement SEMICOLON
	| deleteFactStatement SEMICOLON
	| truncateFactStatement SEMICOLON
	| flushDataStatement SEMICOLON
	| nullifyFactStatement SEMICOLON
	| ifStatement SEMICOLON
	| computePlanStatement SEMICOLON
	| enableDisablePlanStatement SEMICOLON
	| beginTransactionStatement SEMICOLON
	| commitTransactionStatement SEMICOLON
	| abortTransactionStatement SEMICOLON
	| createVersionStatement SEMICOLON
	| createScenarioStatement SEMICOLON
	| deleteVersionStatement SEMICOLON
	| updateScenarioStatement SEMICOLON
	| shareScenarioStatement SEMICOLON
	| unshareScenarioStatement SEMICOLON
	| updateVersionPropertyStatement SEMICOLON
	| execScriptStatement SEMICOLON
	| execProcedureStatement SEMICOLON
	| bulkMemberCreateStatement SEMICOLON
	| createMemberStatement SEMICOLON
	| updateMemberStatement SEMICOLON
	| deleteMemberStatement SEMICOLON
	| copyMemberStatement SEMICOLON
	| copyMeasureStatement SEMICOLON
	| crudMemberStatementSet SEMICOLON
	| purgeMemberStatement SEMICOLON
	| uploadDatafileStatement SEMICOLON
	| downloadDatafileStatement SEMICOLON
	| exportAllStatement SEMICOLON
	| importAllStatement SEMICOLON
	| saveStatement SEMICOLON
	| serviceCommandStatement SEMICOLON
	| restoreExternalDataStatement SEMICOLON
	| syncExternalModelsStatement SEMICOLON
	| syncLocalModelsStatement SEMICOLON
	| refreshMaterializedViewsStatement SEMICOLON
	| mergeDeltaModelsStatement SEMICOLON
	| assignment SEMICOLON
	| grantAccessStatement SEMICOLON
	| denyAccessStatement SEMICOLON
	| resetAccessControlStatement SEMICOLON
	| netChangeAclStatement SEMICOLON
	| updateGraphStatement SEMICOLON
	| vertexSetStatement SEMICOLON
	| subGraphStatement SEMICOLON
	| traverseGraphStatement SEMICOLON
	| graphNodeMembersStatement SEMICOLON
	| activePluginStatement SEMICOLON
	| onDemandPluginStatement SEMICOLON
	| executePowershellPluginStatement SEMICOLON
	| registerAlertStatement SEMICOLON
	| deregisterAlertStatement SEMICOLON
	| garbageCollectStatement SEMICOLON
	| releaseTableMemoryStatement SEMICOLON
	| respreadStatement SEMICOLON
	| respreadStatementWithImpact SEMICOLON
	| simulateWriteStatement SEMICOLON
	| currentUserStatement SEMICOLON
	| sanityCheckStatement SEMICOLON
	| gatherColumnStatsStatement SEMICOLON
	| amplifyRedologStatement SEMICOLON
	| generateGraphStatement SEMICOLON
	| ddlStatement SEMICOLON
	| dmlStatement SEMICOLON
	| batchStartStatement SEMICOLON
	| batchEndStatement SEMICOLON
	| replayStatement SEMICOLON
	| countSelectMemberExprStatement SEMICOLON
	| getAccessControlRulesInfo SEMICOLON
	| haRedisPassThroughStatement SEMICOLON
	| sequentialStatement SEMICOLON
	| explainStatement SEMICOLON
	| execExternalStatement SEMICOLON
	;

execExternalStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: EXECUTE EXTERNAL json
	;

haRedisPassThroughStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
   : HAREDIS .+
   ;

replayStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
   : REPLAY FROM INTEGERS
   ;

batchStartStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
   : START_BATCH
   ;

batchEndStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
   : END_BATCH STRING
   ;

ddlStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
   : DDL json
   ;

dmlStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
   : DML json
   ;

json returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
   : jsonValue
   | JSON_BLOCK
   ;

jsonObject
   : LBRACE jsonPair (',' jsonPair)* RBRACE
   | LBRACE RBRACE
   ;

jsonPair
   : jsonstring ':' jsonValue
   ;

jsonArray
   : LBRACKET jsonValue (',' jsonValue)* RBRACKET
   | LBRACKET RBRACKET
   | QUOTEDID
   ;

jsonValue
   : jsonstring
   | jsonnumber
   | jsonObject
   | jsonArray
   | TEMPLATE_BLOCK
   | 'true'
   | 'false'
   | 'null'
   ;


jsonstring
   : STRING
   ;

jsonnumber
   : numbers
   ;

garbageCollectStatement returns [str serializedInfo]
	: GARBAGE COLLECT
	;

registerAlertStatement	returns [str serializedInfo]
	: REGISTER ALERT (identifierList)?
	;

deregisterAlertStatement	returns [str serializedInfo]
	: DEREGISTER ALERT (identifierList)?
	;

//alert statements - End

// Graph rules (General) - Begin

from_tail
	: FROM | TAIL
	;

to_head
	: TO | HEAD
	;

edgeDirection
	: (IN | from_tail) | (OUT | to_head) | (BOTH | ALL)
	;

traverseDirection
	: UPSTREAM | DOWNSTREAM | (BOTH | ALL)
	;

traverseDistance
	: numbers | ALL
	;

graphNameOrIdentfier returns [str serializedInfo, object RelationshipType]
@after {$ctx.serializedInfo = $ctx.getText();}
	: graph_identifier | graphName
	;

graph_identifier  returns [str serializedInfo, object RelationshipType]
@after {$ctx.serializedInfo = $ctx.getText();}
	: GRAPH DOT graphName
	;

graphName returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	:  (identifier DOT) ? identifier
	;

edge_property returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: EDGE DOT edgePropertyName
	;

edgePropertyName returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	:  (identifier DOT) ? identifier
	;

nameSpace returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: identifier
	;

fully_qualified_edge_property returns [str serializedInfo, str RelationshipTypeName, str EdgePropertyName]
@after {$ctx.serializedInfo = $ctx.getText();}
	: EDGE DOT graphName {$ctx.RelationshipTypeName = $graphName.text;} DOT edgePropertyName {$ctx.EdgePropertyName = $edgePropertyName.text;}
	;

fully_qualified_edge_property_with_vertex_coordinates returns [str serializedInfo, str RelationshipTypeName, str EdgePropertyName]
@after {$ctx.serializedInfo = $ctx.getText();}
	: fully_qualified_edge_property AT LPAREN vertex_coordinate (COMMA vertex_coordinate)* RPAREN
	;

edge_node_member_property returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: (EDGE DOT)? (from_tail | to_head) DOT (member_property | meta_member_property)
	;

node_member_property returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: member_property
	| NODE DOT meta_member_property
	;

nameValue returns [KeyValuePair<str, object> NameValue]
	: LPAREN identifier COMMA (literals | null_or_scalar_exp | identifier) RPAREN
	;

genericNameValue returns [KeyValuePair<str, object> NameValue]
	: LPAREN identifier COMMA scalar_expression RPAREN
	;

edgePredicate_expression returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: scalar_expression
	;

vertexPredicate_expression returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: scalar_expression
	;

graphLevelAttributeName
	: levelattribute_name
	| meta_levelattribute_name
	;

graphVersion_expression returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: member_expression
	;

// Graph rules (General) - End

// Graph crud rules - Begin

updateGraphStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: UPDATE GRAPH graphName (edgeCrudClause)+
	;

edgeCrudClause returns [str serializedInfo, str Action]
@after {$ctx.serializedInfo = $ctx.getText();}
	: ADD EDGE graphNodePairClause edgePropertiesClause?		#EdgeCreate
	| MODIFY EDGE graphNodePairClause edgePropertiesClause		#EdgeModify
	| DELETE EDGE graphNodePairClause							#EdgeDelete
	;

graphNodePairClause returns [str serializedInfo, object VersionExpression, System.Tuple<object, object> GraphNodePair]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LPAREN graphVersion_expression COMMA graphNodeClause COMMA graphNodeClause RPAREN
	;

graphNodeClause returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: graphMemberNode
	| LPAREN graphMemberNode (COMMA graphMemberNode)* RPAREN
	;

graphMemberNode returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: member_expression
	| measure_name
	;

edgePropertiesClause returns [str serializedInfo, List<KeyValuePair<str, object>> EdgePropertyNameValueList]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SET PROPERTIES LBRACE nameValue (COMMA nameValue)* RBRACE
	;

// Graph crud rules - End

// Graph traversal rules - Begin

vertexSetStatement returns [str serializedInfo]
	: VERTEXSET LPAREN graphName COMMA graphVersion_expression (COMMA edgeDirection)? (COMMA vertexPredicate_expression)? RPAREN		#VertexSetName
	| VERTEXSET LPAREN edgeSet_expression (COMMA edgeDirection)? (COMMA vertexPredicate_expression)? RPAREN								#VertexSetExpr
	| LPAREN graphMemberNode (STAR graphMemberNode)* RPAREN																				#VertexSetFromMemberSets
	| graphMemberNode																													#VertexSetFromMemberSet
	;

subGraphStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SUBGRAPH LPAREN graphName COMMA graphVersion_expression (COMMA subGraphVertexSet_expression)* (COMMA edgePredicate_expression)? RPAREN	#SubGraphName
	| SUBGRAPH LPAREN edgeSet_expression (COMMA edgePredicate_expression)? RPAREN																#SubGraphExpr
	;

subGraphVertexSet_expression returns [str serializedInfo, System.Tuple<object, object> DirectionVertexSetPair]
@after {$ctx.serializedInfo = $ctx.getText();}
	: edgeDirection vertexSetStatement
	;

traverseGraphStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: (vertexSetStatement DOT)? TRAVERSE LPAREN graphName COMMA graphVersion_expression (COMMA traverseDirection)? (COMMA traverseDistance)? (COMMA edgePredicate_expression)? RPAREN		#TraverseGraphName
	| (vertexSetStatement DOT)? TRAVERSE LPAREN edgeSet_expression (COMMA traverseDirection)? (COMMA traverseDistance)? (COMMA edgePredicate_expression)? RPAREN							#TraverseGraphExp
	;

edgeSet_expression returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: subGraphStatement
	| traverseGraphStatement
	;

graphNodeMembersStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: DISTINCT? edgeSet_expression DOT MEMBERS LPAREN (graphLevelAttributeName (STAR graphLevelAttributeName)*)? COMMA? edgeDirection? RPAREN
	;

// Graph traversal rules - End

// Graph edge query rules - Begin

selectGraphEdgeProjectStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SELECT member_measure_crossjoin (ON AXISTYPE)? (COMMA member_measure_crossjoin ON AXISTYPE )?
		FROM LPAREN selectGraphEdgesStatement RPAREN
		(adornmentInfo)?
		(WHERE LBRACE edgeProjectPredicate_expression RBRACE)?
		(orderByClause)?
		(limitClause)?
	;

edgeProjectPredicate_expression returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: scalar_expression
	;

selectGraphEdgesStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SELECT edge_crossjoin graph_traversal_options (adornmentInfo)? (WHERE graph_filter_set)? (limitClause)?
	;

edge_crossjoin returns [str serializedInfo, object IBPLExpressions, object RelationshipTypes]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LPAREN RPAREN
	| LPAREN edge_crossjoin_element (STAR edge_crossjoin_element)* RPAREN
	;

edge_crossjoin_element
	: graphVersions_expression
	| graph_identifier
	| measure_element_list
	;

graph_traversal_options returns [str serializedInfo, object TraverseDirection, object TraverseDistance, object StartMemberExpressions]
@after {$ctx.serializedInfo = $ctx.getText();}
	: TRAVERSE? traverseDirection (traverseDistance STEPS?)? graph_traversal_start_set
	;

graph_traversal_start_set returns [str serializedInfo, object StartMemberExpressions]
@after {$ctx.serializedInfo = $ctx.getText();}
	: START? FROM? LBRACE member_expression (COMMA member_expression)* RBRACE
	;

graph_filter_set returns [str serializedInfo, object MemberFilterExpSet, object MeasureFilterExpSet]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LBRACE graph_filter_element (COMMA graph_filter_element)* RBRACE
	;

graph_filter_element
	: graphVersions_expression | rel_edgePredicate_expression
	;

rel_edgePredicate_expression returns [str serializedInfo, object Relationshiptype, object PredicateExpression]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LPAREN graph_identifier COMMA edgePredicate_expression RPAREN
	;

selectGraphPathsStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SELECT member_measure_crossjoin (ON AXISTYPE)? (COMMA member_measure_crossjoin ON AXISTYPE )?
		graph_traversal_options
		(adornmentInfo)?
		(WHERE graph_path_filter_set)?
		(orderByClause)?
		(limitClause)?
	;

graph_path_filter_set returns [str serializedInfo, object MemberFilterExpSet, object MeasureFilterExpSet, object RelationshipTypes]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LBRACE graph_path_filter_element (COMMA graph_path_filter_element)* RBRACE
	;

// TODO: change from graphVersions_expression to member_expression for other member filters later
graph_path_filter_element
	: graph_identifier | graphVersions_expression | rel_edgePredicate_expression
	;


// Graph edge query rules - End

// Dimension graph traversal rules - Begin

selectDimensionGraphEdgesStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SELECT PARENTCHILD dimension_name graph_traversal_options (adornmentInfo)? (dimgraph_where_clause)? (limitClause)?
	;

dimgraph_where_clause returns [str serializedInfo]
	: WHERE LBRACE edgePredicate_expression RBRACE
	;

// Dimension graph traversal rules - End

blockStatement
	: BLOCK BEGIN statement+ END
	;

execParallelStatement
	: EXECUTE PARALLEL BEGIN blockStatement+ END
	;

// Access control rules - Begin

denyAccessStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: denyMemberReadAccessStatement
	| denyCellWriteAccessStatement
	;

denyMemberReadAccessStatement  returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: denyReadPrefixStatement MEMBERS member_expression				#DenyDimensionReadAccessAtMemberSet
	| denyReadPrefixStatement DIMENSION dimension_name				#DenyDimensionReadAccessAtDimension
	| denyReadPrefixStatement LEVELATTRIBUTE levelattribute_name	#DenyDimensionReadAccessAtAttribute
	;

denyReadPrefixStatement  returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: DENY READ accessDeclarationStatement
	;

grantAccessStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: grantCellReadAccessStatement
	| grantMemberReadAccessStatement
	| grantWriteAccessStatement
	| grantMemberExclusiveReadAccessStatement
	;

accessDeclarationStatement returns [str serializedInfo, object IntermediateRule]
@after {$ctx.serializedInfo = $ctx.getText();}
	:	ACCESS aclRuleName=identifier TO ROLES identifier (COMMA identifier)* FOR
	;

grantWriteAccessPrefixStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: GRANT WRITE accessDeclarationStatement
	;

grantReadAccessPrefixStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: GRANT READ accessDeclarationStatement
	;

grantExclusiveReadAccessPrefixStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: GRANT EXCLUSIVE READ accessDeclarationStatement
	;

grantWriteAccessStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: grantMemberWriteAccessStatement #GrantDimensionWriteAccess
	| grantCellWriteAccessStatement   #GrantCellWriteAccess
	;

grantMemberWriteAccessStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: grantWriteAccessPrefixStatement MEMBERS  member_expression		#GrantDimensionWriteAccessAtMemberSet
	| grantWriteAccessPrefixStatement DIMENSION dimension_name		#GrantDimensionWriteAccessAtDimension
	| grantWriteAccessPrefixStatement LEVELATTRIBUTE levelattribute_name	#GrantDimensionWriteAccessAtAttribute
	;

grantMemberExclusiveReadAccessStatement  returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: grantExclusiveReadAccessPrefixStatement MEMBERS  member_expression		#GrantDimensionExclusiveReadAccessAtMemberSet
	| grantExclusiveReadAccessPrefixStatement DIMENSION dimension_name		#GrantDimensionExclusiveReadAccessAtDimension
	| grantExclusiveReadAccessPrefixStatement LEVELATTRIBUTE levelattribute_name	#GrantDimensionExclusiveReadAccessAtAttribute
	;

grantCellWriteAccessStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: grantWriteAccessPrefixStatement cellAccessStatement
	;

grantCellReadAccessStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: grantReadAccessPrefixStatement cellAccessStatement
	;

grantMemberReadAccessStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: grantReadAccessPrefixStatement MEMBERS  member_expression				#GrantDimensionReadAccessAtMemberSet
	| grantReadAccessPrefixStatement DIMENSION dimension_name				#GrantDimensionReadAccessAtDimension
	| grantReadAccessPrefixStatement LEVELATTRIBUTE levelattribute_name		#GrantDimensionReadAccessAtAttribute
	| grantReadAccessPrefixStatement attributeAccessStatement				#GrantDimensionReadAccessAtAttributeBasedOnMeasure
	;

attributeAccessStatement returns [str serializedInfo, object IntermediateRule]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LEVELATTRIBUTE levelattribute_name usingScopeStatement FILTERBY LBRACE measure_name RBRACE
	;

denyCellWriteAccessStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: denyWritePrefixStatement cellAccessStatement
	;

denyWritePrefixStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: DENY WRITE accessDeclarationStatement
	;

cellAccessStatement returns [str serializedInfo, object IntermediateRule]
@after {$ctx.serializedInfo = $ctx.getText();}
	: 	PLAN plan_name usingScopeStatement?	measureFilterStatement?   #PlanAccess
	|	MODEL measure_group_name usingScopeStatement? measureFilterStatement?   #MeasureGroupAccess
	|   MEASURE unqualified_measure_name usingScopeStatement? measureFilterStatement?	#MeasureAccess
	;

getAccessControlRulesInfo returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	:	ACCESSCONTROLRULESINFO
	;

measureFilterStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: FILTERBY LBRACE scalar_expression RBRACE
	;

// Access Control Statements - End

// Plug-in Statements - Begin

activePluginStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: DECLARE PLUGIN INSTANCE instanceName=identifier operatingScopeStatement* usingArgumentsClause?
	;

onDemandPluginStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: EXECUTE PLUGIN INSTANCE instanceName=identifier operatingScopeStatement* usingArgumentsClause? postActionClause?
	;

executePowershellPluginStatement
	: EXECUTE POWERSHELL PLUGIN moduleName=identifier usingArgumentsClause?
	;

operatingScopeStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: FOR MEASURES LBRACE (unqualified_measure_name | measure_name) (COMMA (unqualified_measure_name | measure_name))* RBRACE usingScopeStatement
	;

usingArgumentsClause returns [str serializedInfo, List<KeyValuePair<str, object>> NameValueList]
@after {$ctx.serializedInfo = $ctx.getText();}
	: USING? argumentsClause
	;

argumentsClause returns [str serializedInfo, List<KeyValuePair<str, object>> NameValueList]
@after {$ctx.serializedInfo = $ctx.getText();}
	: ARGUMENTS LBRACE genericNameValue (COMMA genericNameValue)* RBRACE
	;

postActionClause returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
    : POST_ACTION LBRACE statement+ RBRACE
	;

// Plug-in Statements - End

scenarioScopeStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	:	FOR MODEL measure_group_name (usingScopeStatement)?
	|	FOR GRAPH graphNameOrIdentfier (usingVertexScopeStatement)?
	|	FOR MODELS measureGroupList (usingScopeStatement)?
	|	FOR GRAPHS graphList (usingVertexScopeStatement)?
	|	FOR PLAN plan_name (usingScopeStatement|usingVertexScopeStatement)?
	|	FOR PLANS planList (usingScopeStatement|usingVertexScopeStatement)?
	;

usingScopeStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: USING scopeClause
	;

scopeClause returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SCOPE member_crossjoin
	;

globalScenarioScopeStatement
	: usingScopeStatement
	;

measureList
	: unqualified_measure_name (COMMA unqualified_measure_name)*
	;

identifierList
	: identifier (COMMA identifier)*
	;

referMeasuresInParent
	: REFER_PARENT FOR (MEASURES|MEASURE) LBRACE measureList RBRACE
	| INCLUDE (MEASURES|MEASURE) LBRACE measureList RBRACE (REFER_PARENT_FOR_OTHERS)?
	;

mgOverriddenLocalScopeList
	: measure_group_name (usingScopeStatement)? (REFER_PARENT)? (referMeasuresInParent)?
	;

mgOverriddenScopeList
	: mgOverriddenLocalScopeList (COMMA mgOverriddenLocalScopeList)*
	;

includeModelsStatement
	: INCLUDE (MODELS|MODEL) (mgOverriddenScopeList|ALL) (COMMA REFER_PARENT_FOR_OTHERS)? (REFER_PARENT)?
	;

mgNewOverriddenLocalScopeList
	: (measure_group_name)? (usingScopeStatement)? (includeMeasuresStatement)?
	;

planLocalScopeList
	: (plan_name) (usingScopeStatement|usingVertexScopeStatement)?
	;

planOveriddenScopeList
	: planLocalScopeList (COMMA planLocalScopeList)*
	;

mgNewOverriddenScopeList
	: mgNewOverriddenLocalScopeList (COMMA mgNewOverriddenLocalScopeList)*
	;

includeMeasuresStatement
	: (MEASURES|MEASURE) LBRACE measureList RBRACE (REFER_PARENT_FOR_OTHERS|REFER_SELF_FOR_OTHERS)?
	;

includePointerMeasuresStatement
	: (REFER_PARENT|REFER_SELF|EXCLUDE) (MODELS|MODEL)? (mgNewOverriddenScopeList|ALL)? (ALL_OTHERS)?
	;

includePointerMeasuresList
	: includePointerMeasuresStatement (AND includePointerMeasuresStatement)*
	;

mgScopeList
	: mgScopeStatement (COMMA mgScopeStatement)*
	;

mgScopeStatement
	: (measure_group_name) (usingScopeStatement)?
	;

graphScopeList
	: graphScopeStatement (COMMA graphScopeStatement)*
	;

graphScopeStatement
	: (graphNameOrIdentfier) (usingVertexScopeStatement)?
	;

includePlanStatement
	: (REFER_PARENT|REFER_SELF|EXCLUDE) (PLANS|PLAN) (planOveriddenScopeList|ALL)? ((MODELS|MODEL) mgScopeList)? ((MEASURES|MEASURE) LBRACE measureList RBRACE)? ((GRAPHS|GRAPH) graphScopeList)? ((EDGES|EDGE) LBRACE edgeList RBRACE)? (ALL_OTHERS)?
	;

includePlanStatementList
	:	includePlanStatement (AND includePlanStatement)*
	;

fromVertexStatement
	: from_tail vertexScopeStatement
	;

toVertexStatement
	: to_head vertexScopeStatement
	;

usingVertexScopeStatement
	: USING SCOPE LPAREN (fromVertexStatement? | toVertexStatement? | fromVertexStatement (COMMA toVertexStatement)?) RPAREN
	;

edgeList
	: edgePropertyName (COMMA edgePropertyName)*
	;

fullyQualifiedEdgeList
	: fully_qualified_edge_property (COMMA fully_qualified_edge_property)*
	;

referEdgePropInParent
	: REFER_PARENT FOR (EDGE|EDGES) LBRACE edgeList RBRACE
	| INCLUDE (EDGES|EDGE) LBRACE edgeList RBRACE (REFER_PARENT_FOR_OTHERS)?
	;

graphOverriddenLocalScopeList
	: graphNameOrIdentfier (usingVertexScopeStatement)? (REFER_PARENT)? (referEdgePropInParent)?
	;

graphOverriddenScopeList
	: graphOverriddenLocalScopeList (COMMA graphOverriddenLocalScopeList)*
	;

includeGraphsStatement
	: INCLUDE (GRAPHS|GRAPH) (graphOverriddenScopeList|ALL) (COMMA REFER_PARENT_FOR_OTHERS)? (REFER_PARENT)?
	;

edgeOverriddenLocalScopeList
	: (graphNameOrIdentfier)? (usingVertexScopeStatement)? (includeEdgesStatement)?
	;

edgeOverriddenScopeList
	: edgeOverriddenLocalScopeList (COMMA edgeOverriddenLocalScopeList)*
	;

includeEdgesStatement
	: (EDGE|EDGES) LBRACE edgeList RBRACE (REFER_PARENT_FOR_OTHERS|REFER_SELF_FOR_OTHERS)?
	;

pointerEdgeStatement
	: (REFER_PARENT|REFER_SELF|EXCLUDE) (GRAPHS|GRAPH)? (edgeOverriddenScopeList|ALL)? (ALL_OTHERS)?
	;

pointerEdgeStatementList
	:	pointerEdgeStatement (AND pointerEdgeStatement)*
	;

includeDependentEntities
	: INCLUDE DEPENDENT ENTITIES
	;

// LW scenario statements
initializeScenarioStatement	 returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	:	(initializeMeasureGroupStatement) (usingScopeStatement)? (initializeMeasuresStatement)?
	|	(initializeGraphStatement) (usingVertexScopeStatement)? (initializeEdgeStatement)?
	;

initializeMeasureGroupStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	:	INITIALIZE (MODEL|MODELS) LBRACE measureGroupList RBRACE TO (PARENT|NULL)
	;

initializeMeasuresStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	:	INITIALIZE (MEASURE|MEASURES) LBRACE measureList RBRACE
	;

initializeGraphStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	:	INITIALIZE (GRAPH|GRAPHS) LBRACE graphList RBRACE TO (PARENT|NULL)
	;

initializeEdgeStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	:	INITIALIZE (EDGE|EDGES) LBRACE (edgeList|fullyQualifiedEdgeList) RBRACE
	;

// LW scenario statements - END

// Note: AUTHOR tag was a mistake - retained for backward compatibility; should have used arbitrary identifer pairs to begin with
versionArgs
	: FOR identifier
	| AUTHOR identifier
	| EXTERNAL? REPLACE
	| genericVersionArgs
	;

genericVersionArgs returns [object ArgValuePairs]
	: LBRACE argValuePair (COMMA argValuePair)*  RBRACE
	;

argValuePair returns [object ArgValuePair]
	: LBRACE identifier COMMA identifier RBRACE
	;

versionNameOrExp returns [str VersionName, object VersionMemberExp]
	: identifier | member_expression
	;

createVersionStatement
	: CREATEVERSION LPAREN (numbers | member_expression) (COMMA numbers)* COMMA identifier COMMA bools COMMA bools (COMMA identifier)* (COMMA scenarioScopeStatement)* RPAREN (MATERIALIZE|NONMATERIALIZE)? (versionArgs)*
	;

createScenarioStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: createScopedScenarioStatement
	| createLWScenarioStatement
	| createEphemeralScenarioStatement
	;

createScopedScenarioStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: CREATESCENARIO scenarioSourceExpression (MATERIALIZE? globalScenarioScopeStatement? (includePlanStatementList|includeModelsStatement|includePointerMeasuresList)? (includeGraphsStatement|pointerEdgeStatementList)? )? (versionArgs)*
	;

createLWScenarioStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: CREATELWSCENARIO scenarioSourceExpression MATERIALIZE? globalScenarioScopeStatement? initializeScenarioStatement (COMMA initializeScenarioStatement)* (versionArgs)*
	;

createEphemeralScenarioStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: CREATEEPHEMERALSCENARIO scenarioSourceExpression
	;

scenarioSourceExpression returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
    : LPAREN (numbers | member_expression) (COMMA numbers)* COMMA (identifier | TEMPLATE_BLOCK)
      (COMMA (identifier | TEMPLATE_BLOCK))* RPAREN
    ;

deleteVersionStatement
	: DELETEVERSION LPAREN versionNameOrExp RPAREN
	;

updateScenarioStatement
	: UPDATESCENARIO LPAREN versionNameOrExp COMMA versionNameOrExp COMMA bools (COMMA bools)* (COMMA scenarioScopeStatement)* (COMMA EXEC_INCREMENTAL_PLAN)? RPAREN
	;

 updateVersionPropertyStatement
	: UPDATEVERSIONPROPERTY LPAREN versionNameOrExp COMMA levelattribute_name COMMA valueExpr RPAREN
	;

shareScenarioStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SHARESCENARIO versionExpressionStatement WITH identifier (COMMA identifier)*
	;

unshareScenarioStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: UNSHARESCENARIO LPAREN versionNameOrExp RPAREN  WITH identifier (COMMA identifier)*
	;

versionExpressionStatement
	: LPAREN versionNameOrExp (COMMA identifier)? RPAREN
	;

 createMemberStatement
	: CREATEMEMBER LPAREN memberAttributeAssignment (COMMA memberAttributeAssignment)* RPAREN
	;

 updateMemberStatement
	: UPDATEMEMBER LPAREN memberAttributeAssignment (COMMA memberAttributeAssignment)* RPAREN
	;

 deleteMemberStatement
	: DELETEMEMBER LPAREN memberAttributeAssignment RPAREN (CASCADE)?
	;

copyMemberStatement
	: COPYMEMBER LPAREN copyMemberSourceMembers (COMMA copyMemberParentMembers)? RPAREN
	;

copyMemberSourceMembers
	: member_expression
	| memberAssignmentPairs
	;

copyMemberParentMembers returns [object ParentMemberExpList]
	: LBRACE member_expression (COMMA member_expression)* RBRACE
	;

copyMeasureStatement
	: COPYMEASURE LPAREN memberNameAssignmentPairs COMMA LBRACE simple_measure_element (COMMA simple_measure_element)* RBRACE copyMeasureOptions RPAREN (WHERE member_expression)
	;

copyMeasureOptions
	: COMMA bools
	| (COMMA commandOption)*
	;

crudMemberStatement
	: createMemberStatement
	| updateMemberStatement
	| deleteMemberStatement
	| copyMemberStatement
	;

 crudMemberStatementSet
	: EDIT MEMBERS BEGIN (crudMemberStatement SEMICOLON)+ END
	;

purgeMemberStatement
	: PURGE MEMBERS LPAREN RPAREN
	| PURGE MEMBERS LPAREN member_expression (COMMA member_expression)* RPAREN
	;

bulkMemberCreateStatement
	: CREATEMEMBER LPAREN memberAttributeAssignment (COMMA memberAttributeAssignment)* RPAREN usingScopeStatement (WHERE member_measure_filter_set)? (orderByClause)? (limitClause)?
	;

filePaths
	: identifier (COMMA identifier)*
	;

 uploadDatafileStatement
	: UPLOADDATAFILE LPAREN filePaths COMMA bools COMMA identifier (COMMA bools)? RPAREN
	| UPLOADDATAFILE LPAREN filePaths COMMA bools COMMA identifier (COMMA bools)? COMMA identifier RPAREN
	| UPLOADDATAFILE LPAREN filePaths COMMA bools COMMA identifier (COMMA bools)? COMMA identifier COMMA identifier RPAREN
	| UPLOADDATAFILE LPAREN filePaths (COMMA commandOption)* RPAREN
	;

 downloadDatafileStatement
	: DOWNLOADDATAFILE LPAREN (selectCrossJoinStatement | selectCrossJoinStatementWithPostFilter) (COMMA (selectCrossJoinStatement | selectCrossJoinStatementWithPostFilter))* COMMA identifier COMMA bools COMMA identifier RPAREN
	| DOWNLOADDATAFILE LPAREN (selectCrossJoinStatement | selectCrossJoinStatementWithPostFilter) (COMMA (selectCrossJoinStatement | selectCrossJoinStatementWithPostFilter))* COMMA identifier COMMA bools COMMA identifier COMMA identifier RPAREN
	| DOWNLOADDATAFILE LPAREN (selectCrossJoinStatement | selectCrossJoinStatementWithPostFilter) (COMMA (selectCrossJoinStatement | selectCrossJoinStatementWithPostFilter))* COMMA identifier COMMA bools COMMA identifier COMMA identifier COMMA identifier RPAREN
	| DOWNLOADDATAFILE LPAREN (selectCrossJoinStatement | selectCrossJoinStatementWithPostFilter) (COMMA (selectCrossJoinStatement | selectCrossJoinStatementWithPostFilter))* (COMMA commandOption)* RPAREN
	;

commandOption
	: identifier COLON identifier
	| identifier COLON bools
	| identifier COLON INTEGERS
	| identifier COLON MINUS INTEGERS
	| identifier COLON convert_using_clause
	;

 exportAllStatement
    : EXPORTALL LPAREN bools? RPAREN (INCLUDE (DIMENSION|DIMENSIONS) dimensionSet)? (INCLUDE (MODEL|MODELS) measureGroupSet)? (INCLUDE (GRAPH|GRAPHS) graphSet)?
	| EXPORTALL LPAREN identifier (COMMA bools)? RPAREN (INCLUDE (DIMENSION|DIMENSIONS) dimensionSet)? (INCLUDE (MODEL|MODELS) measureGroupSet)? (INCLUDE (GRAPH|GRAPHS) graphSet)?
	| EXPORTALL LPAREN identifier COMMA identifier (COMMA bools)? RPAREN (INCLUDE (DIMENSION|DIMENSIONS) dimensionSet)? (INCLUDE (MODEL|MODELS) measureGroupSet)? (INCLUDE (GRAPH|GRAPHS) graphSet)?
	| EXPORTALL LPAREN identifier COMMA identifier COMMA identifier (COMMA bools)? RPAREN (INCLUDE (DIMENSION|DIMENSIONS) dimensionSet)? (INCLUDE (MODEL|MODELS) measureGroupSet)? (INCLUDE (GRAPH|GRAPHS) graphSet)?
	;

 importAllStatement
	: IMPORTALL LPAREN RPAREN
	| IMPORTALL LPAREN identifier RPAREN
	| IMPORTALL LPAREN identifier COMMA identifier RPAREN
	| IMPORTALL LPAREN identifier COMMA identifier COMMA identifier RPAREN
	;

 saveStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SAVE LPAREN identifier? RPAREN (BACKGROUND bools)? (PARALLEL bools)? (OBFUSCATE bools)? (FOR_UPGRADE bools)? (ARGUMENTS json)?
	;

serviceCommandStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: EXECSERVICECOMMAND identifier (ARGUMENTS json)?
	;

restoreExternalDataStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: RESTORE EXTERNAL DATA json
	;

syncExternalModelsStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SYNC EXTERNAL (SNAPSHOT)? (INCLUDE (MODEL|MODELS) measureGroupSet)? (INCLUDE (GRAPH|GRAPHS) graphSet)? (INCLUDE (DIMENSION|DIMENSIONS) dimensionSet)? FROM_STAGE? (WHERE LBRACE member_expression RBRACE)?
	| SYNC EXTERNAL (INCLUDE (MODEL|MODELS) measureGroupList)? (INCLUDE (DIMENSION|DIMENSIONS) dimensionList)? (WHERE LBRACE member_expression RBRACE)? FOR (PARTITION|PARTITIONS) (identifier (COMMA identifier)*)
	;

syncLocalModelsStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SYNC LOCAL INCREMENTAL? STRICT? (INCLUDE (MODEL|MODELS) measureGroupSet)? (INCLUDE (GRAPH|GRAPHS) graphSet)? (INCLUDE (DIMENSION|DIMENSIONS) dimensionSet)? (WHERE LBRACE graphEdgePropertyUpdate_member (COMMA graphEdgePropertyUpdate_member)* RBRACE)? (EXCLUDEPROPERTIES syncLocalExcludePropertyList)?
	| SYNC LOCAL (INCLUDE (MODEL|MODELS) measureGroupList)? (INCLUDE (DIMENSION|DIMENSIONS) dimensionList)? (WHERE LBRACE member_expression RBRACE)? FOR (PARTITION|PARTITIONS) (identifier (COMMA identifier)*) (EXCLUDEPROPERTIES syncLocalExcludePropertyList)?
	;

syncLocalExcludePropertyList returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LBRACE (identifier (COMMA identifier)*) RBRACE
	;

refreshMaterializedViewsStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: REFRESH MATERIALIZED VIEW (INCLUDE (MODEL|MODELS) measureGroupSet)? (INCLUDE (GRAPH|GRAPHS) graphSet)? (WHERE LBRACE member_expression RBRACE)?
	;

releaseTableMemoryStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: RELEASE MEMORY (INCLUDE (MODEL|MODELS) measureGroupSet)? (INCLUDE (GRAPH|GRAPHS) graphSet)? (WHERE LBRACE member_expression RBRACE)?
	;

mergeDeltaModelsStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: MERGE DELTA (INCLUDE (MODEL|MODELS) measureGroupSet)? (INCLUDE (GRAPH|GRAPHS) graphSet)?
	;

 resetAccessControlStatement
	: RESETACCESSCONTROL
	;

generateGraphStatement
	: GENERATEGRAPH LPAREN commandOption COMMA commandOption (COMMA commandOption)* RPAREN
	;

netChangeAclStatement
	: BEGIN NETCHANGE_ACCESSCONTROL SEMICOLON (netChangeAclRoleStatement | netChangeAclRuleStatement)+ END NETCHANGE_ACCESSCONTROL
	;

netChangeAclRoleStatement
	: (ADD | DELETE) ROLE identifier ( rolePropertyValuePair (COMMA rolePropertyValuePair)* )? SEMICOLON
	;

rolePropertyValuePair
	: LBRACE identifier COMMA identifier RBRACE
	;

netChangeAclRuleStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: (DELETE)? (grantAccessStatement | denyAccessStatement) SEMICOLON
	| DELETE ACL_RULE identifier SEMICOLON
	;

 simulateWriteStatement
	: SIMULATEWRITE positiveInteger
	;

 memberAttributeAssignment returns [object Attr, System.Tuple<object, object> Value]
	: levelattribute_name ASSIGN LBRACE valueExpr? COMMA (identifier | scalar_expression)? RBRACE
	;

memberNameAssignmentPairs returns [object Attr, object MemberNamePairs]
	: levelattribute_name ASSIGN LBRACE LBRACE memberNamePair RBRACE (COMMA LBRACE memberNamePair RBRACE)*  RBRACE
	;

memberAssignmentPairs returns [object Attr, object MemberNamePairs]
	: LBRACE levelattribute_name ASSIGN LPAREN memberNamePair RPAREN (COMMA LPAREN memberNamePair RPAREN)* RBRACE
	;

memberNamePair returns [object MemberNamePair]
	: identifier COMMA identifier
	;

currentUserStatement
	: CURRENTUSER LPAREN RPAREN
	;

selectMemberExprStatement
	: selectCrossJoinStatement
	| selectCrossJoinStatementWithPostFilter
	| selectMemberStatement
	| selectScenarioScopedMemberStatement
	| SELECT graphNodeMembersStatement
	| SELECT scalar_expression
	;

selectCrossJoinStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: withCalcMembersClause? withTransientMeasureClause? SELECT member_measure_crossjoin (ON AXISTYPE)? (COMMA member_measure_crossjoin ON AXISTYPE )?
		(join_on_clause)?
		(convert_using_clause)?
		(adornmentInfo)?
		query_option_list?
		include_subtotals_sub_query?
		(WHERE member_measure_filter_set)?
		(orderByClause)?
		(limitClause)?
	;

selectCrossJoinStatementWithPostFilter returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LPAREN selectCrossJoinStatement RPAREN DOT FILTER LPAREN scalar_expression RPAREN (orderByClause)? (limitClause)?
	| selectCrossJoinStatement DOT FILTER LPAREN scalar_expression RPAREN (orderByClause)? (limitClause)?
	;

selectMemberStatement
	: SELECT member_expression (INCLUDE include_member_properties (COMMA include_member_properties)*) ? (orderByClause)? (limitClause)?
	;

selectScenarioScopedMemberStatement
	: SELECT member_expression (INCLUDE include_member_properties (COMMA include_member_properties)*) ? (limitClause)? WHERE LBRACE member_expression RBRACE
	;

countSelectMemberExprStatement returns [str serializedInfo]
	: LPAREN selectMemberExprStatement RPAREN DOT COUNT
	;

spreadSelectCrossJoinStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SPREAD SELECT member_measure_crossjoin
			(WHERE member_filter_set)?
	;

member_filter_set returns [object MemberFilterExpSet, object RelationshipTypes]
	: LBRACE member_filter (COMMA member_filter)* RBRACE
	;

member_filter
	: member_expression
	| graph_identifier
	| graphNodeMembersStatement
	;


// Begin Calculated Member clause

withCalcMembersClause returns [str serializedInfo, object CalcMemberSpecs, object SelectedMeasures]
@after {$ctx.serializedInfo = $ctx.getText();}
	: WITH CALCULATED MEMBERS calcMemberClause (COMMA calcMemberClause)*
	;

calcMemberClause returns [str serializedInfo, object CalcMemberSpec, object SelectedMeasures]
@after {$ctx.serializedInfo = $ctx.getText();}
	: scalar_expression AS identifier calcMemberCellPropertiesClause? calcMemberOverridesClause?
	;

calcMemberCellPropertiesClause returns [str serializedInfo, object CellProperties]
@after {$ctx.serializedInfo = $ctx.getText();}
	: CELLPROPERTIES LPAREN measure_cell_properties_pair (COMMA measure_cell_properties_pair)* RPAREN
	;

measure_cell_properties_pair returns [str serializedInfo, str MeasureName, object CellProperties]
@after {$ctx.serializedInfo = $ctx.getText();}
	: (measure_name	| transient_measure_name) COMMA LBRACE cell_property_override (COMMA cell_property_override)* RBRACE
	;

cell_property_override returns [str serializedInfo, str PropertyName, object PropertyFormula]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LPAREN cell_properties COMMA scalar_expression RPAREN
	;

calcMemberOverridesClause returns [str serializedInfo, object MeasuresWithCalcMemberOverrides, object CalcMemberOverrides]
@after {$ctx.serializedInfo = $ctx.getText();}
	: CALCULATEDMEMBEROVERRIDES LPAREN measure_calcmemberexpression_pair (COMMA measure_calcmemberexpression_pair)* RPAREN
	;

measure_calcmemberexpression_pair returns [str serializedInfo, str MeasureName, object CalcMemberOverride]
@after {$ctx.serializedInfo = $ctx.getText();}
	: (measure_name	| transient_measure_name) LBRACE scalar_expression RBRACE
	;

// End Calculated Member clause


// Begin TRANSIENT Measure clause

withTransientMeasureClause returns [str serializedInfo, object TransientMeasureSpecs, object SelectedMeasures]
@after {$ctx.serializedInfo = $ctx.getText();}
	: WITH TRANSIENT MEASURES transientMeasureClause (COMMA transientMeasureClause)*
	;

transientMeasureClause returns [str serializedInfo, object TransientMeasureSpec, object SelectedMeasures]
@after {$ctx.serializedInfo = $ctx.getText();}
	:  (transient_measure_name CELLPROPERTIES LBRACE transientMeasurePropertyClause RBRACE)
	;

transientMeasurePropertyClause returns [str serializedInfo, str MeasureName, object CellProperties]
@after {$ctx.serializedInfo = $ctx.getText();}
	:  cellPropertyClause (COMMA cellPropertyClause)*
	;

cellPropertyClause returns [str serializedInfo, str PropertyName, object PropertyFormula]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LPAREN cell_properties COMMA scalar_expression RPAREN
	;

// End TRANSIENT Measure clause


orderByClause returns [str serializedInfo, object OrderByClause]
@after {$ctx.serializedInfo = $ctx.getText();}
	:  ORDERBY memberOrMeasureNameOrderByClause (COMMA memberOrMeasureNameOrderByClause)*
	;

limitClause returns [str serializedInfo, object LimitSpec]
@after {$ctx.serializedInfo = $ctx.getText();}
       : LIMIT INTEGERS (offsetClause)?
	   | offsetClause
	   | (topClause | bottomClause)+
       ;

topClause returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
       : (TOP | FIRST) INTEGERS
       ;

bottomClause returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
       : (BOTTOM | LAST) INTEGERS
       ;

offsetClause returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: OFFSET INTEGERS
	;

memberOrMeasureNameOrderByClause
	: memberPropertyOrderByClause | measureNameOrderByClause
	;

memberPropertyOrderByClause
	: levelattribute_name DOT identifier (ASC|DESC)?
	| (graph_identifier DOT)? (from_tail | to_head) DOT levelattribute_name DOT identifier (ASC|DESC)?
	;

measureNameOrderByClause
	: measure_name (ASC|DESC)?
	| transient_measure_name (ASC|DESC)?
	| fully_qualified_edge_property (ASC|DESC)?
	| edge_property (ASC|DESC)?
	;

join_on_clause returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: JOIN ON LPAREN join_expression (COMMA join_expression)* RPAREN
	;

join_expression returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LBRACE member_expression (COMMA member_expression)+ RBRACE
	;

convert_using_clause returns [object MeasureMemberMap]
	: CONVERT USING LPAREN named_member_expression (COMMA named_member_expression)* RPAREN
	| CONVERT (USING|FROM) LPAREN LBRACE measure_element COMMA named_member_expression RBRACE (COMMA LBRACE measure_element COMMA named_member_expression RBRACE)* RPAREN
	;

adornmentInfo returns [object Info]
	: INCLUDE include_properties (COMMA include_properties)*  use_aliases?
	| use_aliases
	;

use_aliases
	: USE ALIASES LBRACE alias (COMMA alias)* RBRACE
	;

alias
	: dimension_attribute_alias
	| node_alias
	;

dimension_attribute_alias
	: (dimension|levelattribute) COLON identifier
	;

node_alias
	: vertex_coordinate COLON identifier
	;

include_properties
	: include_member_properties
	| include_anchor_members
	| CELLPROPERTIES LBRACE cell_properties (COMMA cell_properties)* RBRACE
	| NODEPROPERTIES LBRACE node_properties (COMMA node_properties)* RBRACE
	| LCID numbers
	| NODETYPEMEASURES LBRACE measure_name (COMMA measure_name)* RBRACE
	| GROUPBYMEMBERPROPERTIES LBRACE levelattribute_name COMMA levelattribute_name RBRACE
	;

include_member_properties returns [object Info]
	: MEMBERPROPERTIES attribute_properties*
	;

include_anchor_members returns [object Info]
	: ANCHORMEMBERS LBRACE anchor_members (COMMA anchor_members)* RBRACE
	;

anchor_members
	: levelattribute_name COLON LBRACE (identifier (COMMA identifier)*)? RBRACE
	;

query_option_list returns [object QueryOptions]
	: query_option+
	;

query_option
	: include_nulls
	| NULLS_FOR_UNRELATED_ATTR_SELECT
	| NULLS_FOR_FINER_GRAIN_SELECT
	| include_subtotals
	| FILTER_BY_UPDATES
	| FILTER_BY_UPDATES_IN_ALERTS
	| APPLY_CARTESIAN
	| include_nullmember
	| INCLUDEALLVALUESWITHFILTER
	;

include_nullmember
	: INCLUDE_NULLMEMBERS
	;

include_subtotals
	: INCLUDE_SUBTOTALS
	| INCLUDE_VISUAL_SUBTOTALS
	;

include_subtotals_sub_query returns [object SubQueryElements, object SubQueryElementsGraphs]
	: LBRACE sub_query (COMMA sub_query)* RBRACE
	;

sub_query
	: LBRACE sub_query_element (STAR sub_query_element)* RBRACE convert_using_clause?
	;

sub_query_element
	: levelattribute (DOT identifier)?
	| vertex_coordinate ((DOT identifier)?)
	;

include_nulls
	: INCLUDE NULLS (FOR SERIES dimension?)?
	;

member_measure_filter_set returns [object MemberFilterExpSet, object MeasureFilterExpSet, object RelationshipTypes, object AssociationMeasureExpSet, object MeasureZero]
	: LBRACE member_measure_filter (COMMA member_measure_filter)* RBRACE
	;

member_measure_filter
	: member_expression
	| graph_identifier
	| graphNodeMembersStatement
	| ASSOCIATION? scalar_expression
	| measureZeroClause
	;

measureZeroClause
	: MEASURE_ZERO
	| MEASURE_NULL
	| MEASURE_NULLORZERO
	;

attribute_properties
	: LBRACE levelattribute COMMA identifier (COMMA identifier)* RBRACE
	| LBRACE (graph_identifier DOT)? (from_tail | to_head) DOT levelattribute COMMA identifier (COMMA identifier)* RBRACE
	;

computePlanStatement
	: COMPUTE PLAN
	;

enableDisablePlanStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: (ENABLE | DISABLE) PLAN
	;

beginTransactionStatement
	: BEGIN TRANSACTION
	;

commitTransactionStatement
	: COMMIT TRANSACTION
	;

abortTransactionStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: abortTransaction																			#DiscardTransaction
	| abortTransaction (selectCrossJoinStatement | selectCrossJoinStatementWithPostFilter)		#DiscardTransactionWithImpact
	;

abortTransaction
	: ABORT TRANSACTION
	;

updateStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: UPDATE measure_or_edge_property_update (COMMA measure_or_edge_property_update)*
		(WHERE member_measure_filter_set)?
		(convert_using_clause)?
		(include_subtotals)? (include_subtotals_sub_query)?												#UpdateAssignment
	| UPDATE CELL tuple_cell_assignment																	#UpdateSingleTupleSet
	| UPDATE CELL LPAREN tuple_cell_assignment RPAREN (COMMA LPAREN tuple_cell_assignment RPAREN)*
		(WHERE member_measure_filter_set)?
		(convert_using_clause)?
		(include_subtotals)? (include_subtotals_sub_query)?												#UpdateMultiTupleSet
	;

updateStatementWithImpact
	: updateStatement (selectCrossJoinStatement | selectCrossJoinStatementWithPostFilter)
	;

respreadStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: RESPREAD measure_element USING measure_element FOR SCOPE COLON member_measure_crossjoin (WHERE member_measure_filter_set)?
	;

respreadStatementWithImpact
	: respreadStatement (selectCrossJoinStatement | selectCrossJoinStatementWithPostFilter)
	;

measure_or_edge_property_update returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: assignment | graphEdgePropertyUpdate
	;

tuple_cell_assignment
	: measure cell_property_assignment (COMMA cell_property_assignment)*
	;

cell_property_assignment
	: cell_properties ASSIGN valueExpr
	;

massUpdateStatement
	: BEGIN UPDATE (scopeStatement SEMICOLON)+ END
	;

sanityCheckStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: SANITY CHECK (USING identifier (COMMA identifier)*)? (FOR (MODEL|MODELS) mgAndGraphGroupSet)? (FOR (DIMENSION|DIMENSIONS) dimensionSet)? (HIGHLIGHT_CORRUPT_PARTITIONS)? (includeDependentEntities)?
	;

gatherColumnStatsStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: GATHER COLUMNSTATS (USING identifier (COMMA identifier)*)? FOR MODEL measure_group_name (COMMA measure_group_name)*     #GatherColumnStatsForMeasureGroup
	| GATHER COLUMNSTATS FOR DIMENSION dimension_name (COMMA dimension_name)*	#GatherColumnStatsForDimension
;

explainStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: EXPLAIN selectMemberExprStatement
;

amplifyRedologStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: AMPLIFYREDO numbers identifier #AmplifyRedo
;


deleteFactStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: DELETE DATA FOR MODEL measureGroupList (COPYTO measureGroupList)? WHERE member_measure_filter_set	#DeleteFactMeasureGroup
	| DELETE ALL MODEL DATA FOR MEMBERS member_measure_filter_set										#DeleteFactMembers
	| DELETE (DATA | EDGES) FOR GRAPH graphList (COPYTO graphList)? deleteEdgesFilterClause		#DeleteGraphEdges
	;

measureGroupSet
	: measureGroupList
	| ALL
	| ALL EXCEPT measureGroupList
	;

measureGroupList
	: measure_group_name (COMMA measure_group_name)*
	;

graphSet
	: measureGroupList
	| ALL
	| ALL EXCEPT measureGroupList
	;

graphList
	: graphNameOrIdentfier (COMMA graphNameOrIdentfier)*
	;

planList
	: plan_name (COMMA plan_name)*
	;

mgAndGraphGroupSet
	: measureGroupList
	| ALL
	| ALL EXCEPT measureGroupList
	;

deleteEdgesFilterClause  returns [str serializedInfo, object VersionFilterExp, object RelationshipFilterExpSet]
@after {$ctx.serializedInfo = $ctx.getText();}
	: WHERE LBRACE graphVersions_expression (COMMA rel_deleteEdgesFilter_expression)* RBRACE
	;

rel_deleteEdgesFilter_expression  returns [str serializedInfo, object Relationshiptype, object MemberFilterExpSet, object PredicateExpression]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LPAREN graphNameOrIdentfier (COMMA member_expression)* (COMMA edgePredicate_expression)* (COMMA measureZeroClause)? RPAREN
	;

truncateFactStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: TRUNCATE DATA FOR MODEL measureGroupList WITH VERSIONNAME (identifier (COMMA identifier)*)		#TruncateMeasureGroup
	| TRUNCATE DATA FOR GRAPH graphList WITH VERSIONNAME (identifier (COMMA identifier)*)				#TruncateGraph
	;

flushDataStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: FLUSH DATA FOR (MODEL|MODELS) measureGroupList DELETEFROMDISK? (WHERE LBRACE member_expression RBRACE)? FOR (PARTITION|PARTITIONS) (identifier (COMMA identifier)*)
	| FLUSH DATA FOR (DIMENSION|DIMENSIONS) dimensionList DELETEFROMDISK? FOR (PARTITION|PARTITIONS) (identifier (COMMA identifier)*)
	;

nullifyFactStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: NULLIFY measure_element_list FOR member_expression (INCLUDE DEPENDENT MEASURES)?
	;

recurrenceScopeStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: (ORDERED)? RECURRENCE SCOPE COLON member_measure_crossjoin SEMICOLON statement+ ENDSCOPE
	;

insertScopeStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: INSERT SCOPE COLON member_measure_crossjoin SEMICOLON statement+ ENDSCOPE
	;

blockScopeStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: BLOCK SCOPE COLON member_measure_crossjoin SEMICOLON statement+ ENDSCOPE
	;

blockScopeGraphStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: BLOCK SCOPE COLON vertexScopeForGraphAssignmentStatement SEMICOLON graphEdgePropertyAssignment+ ENDSCOPE
	;

scopeStatement returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	:  scopePrefix SCOPE COLON member_measure_crossjoin (WHERE member_measure_filter_set)? SEMICOLON statement+ ENDSCOPE (convert_using_clause)?
	;

scopePrefix
	: SPREAD? CARTESIAN? EVALUATEMEMBER?
	;

scopeStatementWithImpact
	: scopeStatement (selectCrossJoinStatement | selectCrossJoinStatementWithPostFilter)
	;

scopedGraphEdgePropertyAssignments returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: scopePrefix SCOPE COLON  vertexScopeForGraphAssignmentStatement SEMICOLON graphEdgePropertyAssignment+ ENDSCOPE
	;

vertexScopeForGraphAssignmentStatement	returns [str serializedInfo, object RelationshipType, object VersionExpression, object FromNodeFilters, object ToNodeFilters]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LPAREN graphName COMMA graphVersions_expression (COMMA from_tail vertexScopeStatement)? ( COMMA to_head vertexScopeStatement)? RPAREN
	;

graphVersions_expression returns [str serializedInfo,  object VersionExpression]
@after {$ctx.serializedInfo = $ctx.getText();}
       : member_expression
       ;

vertexScopeStatement returns [str serializedInfo, object NodeFilters]
@after {$ctx.serializedInfo = $ctx.getText();}
       : member_expressions_or_expression (STAR member_expressions_or_expression)*
       ;

member_expressions_or_expression returns [str serializedInfo, object NodeFilters]
@after {$ctx.serializedInfo = $ctx.getText();}
	   : member_expressions
	   | member_expression
	   ;

graphEdgePropertyAssignment returns [str serializedInfo, object RelationshipType]
@after {$ctx.serializedInfo = $ctx.getText();}
	: edge_property	ASSIGN null_or_scalar_exp SEMICOLON
	;

graphEdgePropertyUpdate returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: EDGE (DOT graphName)? DOT edgePropertyName AT LPAREN graphEdgePropertyUpdate_coordinates RPAREN ASSIGN null_or_scalar_exp
	;

graphEdgePropertyUpdate_coordinates returns [str serializedInfo, object VersionExpression, object FromMemberExpressions, object ToMemberExpressions]
@after {$ctx.serializedInfo = $ctx.getText();}
	: graphEdgePropertyUpdate_member (COMMA graphEdgePropertyUpdate_member)*
	;

graphEdgePropertyUpdate_member returns [str serializedInfo, object IsFromNode]
@after {$ctx.serializedInfo = $ctx.getText();}
	: (from_tail | to_head) DOT member_expression
	| graphVersions_expression
	;

foreachStatement
	: member_expression DOT FOREACH LPAREN block RPAREN
	;


ifStatement
	: IF expression THEN block (ELSE  IF expression THEN block)* (ELSE THEN block)?
	;


ifStat
	: IF expression THEN block
	;


elseIfStat
	: ELSE IF expression THEN block
	;


elseStat
	: ELSE THEN block
	;


assignment returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
  	: scalar_expression ASSIGN null_or_scalar_exp
  	;

edgePropertyAssignment [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: fully_qualified_edge_property ASSIGN null_or_scalar_exp
	;

createSetStatement
	: CREATE set_modifier? SET identifier ASSIGN member_expression		#CreateSetMemberSet
	| CREATE set_modifier? SET identifier ASSIGN member_crossjoin		#CreateSetMemberSetCrossJoin
	;

createProcStatement
	: (CREATE | REPLACE) PARALLEL? PROCEDURE procname=identifier BEGIN PROCEDURE? statement+ END PROCEDURE?	#CreateProcedure
	| (CREATE | REPLACE) PARAMETERIZED PARALLEL? PROCEDURE procname=identifier json? procbody=PROC_BODY		#CreateParameterizedProcedure
	;

sequentialStatement
    : BEGIN SEQUENTIAL statement+ END SEQUENTIAL
	;

createFunctionStatement
	: (CREATE | REPLACE) FUNCTION funcname=identifier LPAREN (argument+=ARGUMENT argumentType+=DATATYPE COMMA?)* RPAREN RETURNS DATATYPE BEGIN block? RETURN ASSIGN expression SEMICOLON END
	;

execScriptStatement
	: EXECUTE SCRIPT scriptName=identifier
	;


execProcedureStatement
	: (EXECUTE | EXPAND) PROCEDURE procname=identifier json?
	;


createRelStatement
	: CREATERELATIONSHIP LPAREN member_expression COMMA member_expression COMMA identifier RPAREN
	;


deleteRelStatement
	: DELETERELATIONSHIP LPAREN member_expression COMMA member_expression COMMA identifier RPAREN
	;


updateRelAttrStatement
	: UPDATERELATIONSHIPATTR LPAREN member_expression COMMA member_expression COMMA identifier COMMA identifier COMMA literals RPAREN
	;


getRelAttrStatement
	: GETRELATIONSHIPATTR LPAREN member_expression COMMA member_expression COMMA identifier COMMA identifier RPAREN
	;

set_modifier
	: DYNAMIC|STATIC
	;


member_exprList
	: LPAREN member_expression (COMMA member_expression)* RPAREN
	;


scalar_exprList returns [object ScalarExpressions]
    : TEMPLATE_BLOCK
    | LBRACE (scalar_expression | TEMPLATE_BLOCK)
      (COMMA (scalar_expression | TEMPLATE_BLOCK))* RBRACE
    ;


literal_exprSet
    : LBRACE (literals | TEMPLATE_BLOCK) (COMMA (literals | TEMPLATE_BLOCK))* RBRACE
    | LBRACE (identifier | TEMPLATE_BLOCK) (COMMA (identifier | TEMPLATE_BLOCK))* RBRACE
    ;

expression
	: member_expression
	| scalar_expression
	;

null_or_scalar_exp returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: NULL
	| scalar_expression
	;


scalar_expression returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: condExpr
	;

condExpr
	: orExpr ( QUESTION scalar_expression COLON scalar_expression )?
	;

orExpr
	: andExpr (OR andExpr)*
	;

andExpr
	: equExpr (AND equExpr)*
	;

equExpr
	: notEquExpr (EQUALS notEquExpr)*
	;

notEquExpr
	: inScalarSetExpr (NOTEQUAL inScalarSetExpr)*
	;

inScalarSetExpr
	: relExpr (IN scalar_exprList)?
	;

relExpr
	: relStrExpr (op=(LESSTHANOREQUALTO | LESSTHAN | GREATERTHANOREQUALTO | GREATERTHAN) relStrExpr )*		#RelExprNumeric
	;

relStrExpr
	: addExpr (op=(LIKE | CONTAINS | STARTSWITH | ENDSWITH | CONTAINSREGEXP) addExpr)*				#RelExprString
	;

addExpr
	: subExpr (PLUS subExpr)*
	;

subExpr
	: mulExpr (MINUS mulExpr)*
	;

mulExpr
	: divExpr (STAR divExpr)*
	;

divExpr
	: modExpr (DIVIDE modExpr)*
	;

modExpr
	: powExpr (MOD powExpr)*
	;

powExpr
	: unaryExpr (POWER unaryExpr)*
	;

unaryExpr
	: TILDE valueExpr
	| valueExpr
	;

valueExpr
	: LPAREN scalar_expression RPAREN			#ValueScalar
	| literals									#ValueLiteral
	| named_member_expression					#ValueNamedMember
	| member_property							#ValueMemberProperty
	| measure_property							#ValueMeasureProperty
	| measure									#ValueMeasure
	| tuple_computed_aggregate_measure          #ValueTupleComputedAggregateMeasure
	| fully_qualified_edge_property             #ValueFullyQualifiedEdgeProperty
	| edge_property								#ValueEdgeProperty
	| fully_qualified_edge_property_with_vertex_coordinates         #ValueFullyQualifiedEdgePropertyWithVertexCoordinates
	| edge_node_member_property					#ValueEdgeNodeMemberProperty
	| node_member_property						#ValueNodeMemberProperty
	| identifier								#ValueId
	| literal_exprSet							#ValueLiteralSet
	| TEMPLATE_BLOCK							#ValueTemplate
	;

literals
	: numbers																	#LiteralNumber
	| bools																		#LiteralBool
	| NULL																		#LiteralNull
	| NOW (LPAREN RPAREN)?														#LiteralDateNow
	| LASTCOMMITTIME (LPAREN identifier? RPAREN)?								#LiteralLastCommitTime
	| LASTUPDATETIME (LPAREN identifier? RPAREN)?								#LiteralLastUpdateTime
	| TODATETIME LPAREN scalar_expression RPAREN								#LiteralToDateTime
	| DATEADD LPAREN scalar_expression COMMA scalar_expression COMMA identifier RPAREN #LiteralDateAdd
	| DATEDIFF LPAREN scalar_expression COMMA scalar_expression COMMA identifier RPAREN #LiteralDateDiff
	| NEXTCOUNT LPAREN identifier RPAREN										#LiteralNextCount
	| NEXTLABEL LPAREN identifier RPAREN										#LiteralNextLabel
	| ABS LPAREN scalar_expression RPAREN										#LiteralAbs
	| CEILING LPAREN scalar_expression RPAREN									#LiteralCeiling
	| DIV LPAREN scalar_expression RPAREN										#LiteralDiv
	| FLOOR LPAREN scalar_expression RPAREN										#LiteralFloor
	| FLOAT LPAREN scalar_expression RPAREN										#LiteralFloat
	| INTEGER LPAREN scalar_expression RPAREN									#LiteralInteger
	| TOSTRING LPAREN scalar_expression RPAREN									#LiteralToString
	| UPPER LPAREN scalar_expression RPAREN										#LiteralUpper
	| LOWER LPAREN scalar_expression RPAREN										#LiteralLower
	| LOG LPAREN scalar_expression (COMMA scalar_expression)? RPAREN			#LiteralLog
	| EXP LPAREN scalar_expression RPAREN										#LiteralExponential
	| POWER LPAREN scalar_expression COMMA scalar_expression RPAREN				#LiteralPow
	| RANDOM LPAREN (numbers (COMMA numbers)*)? RPAREN							#LiteralRandom
	| ROUND LPAREN scalar_expression (COMMA valueExpr)? (COMMA identifier)? RPAREN	#LiteralRound
	| SUM LPAREN scalar_expression (COMMA scalar_expression)* RPAREN			#LiteralSum
	| SUMPRODUCT LPAREN scalar_exprList COMMA scalar_exprList RPAREN			#LiteralSumProduct
	| AVG LPAREN scalar_expression (COMMA scalar_expression)* RPAREN			#LiteralAvg
	| AVGWITHNULLS LPAREN scalar_expression (COMMA scalar_expression)* RPAREN	#LiteralAvgWithNulls
	| CORREL LPAREN scalar_exprList COMMA scalar_exprList RPAREN				#LiteralCorrel
	| COUNT LPAREN scalar_expression (COMMA scalar_expression)* RPAREN			#LiteralCount
	| MIN LPAREN scalar_expression (COMMA scalar_expression)* RPAREN			#LiteralMin
	| MAX LPAREN scalar_expression (COMMA scalar_expression)* RPAREN			#LiteralMax
	| CONCATENATE LPAREN scalar_expression (COMMA scalar_expression)* RPAREN	#LiteralConcat
	| LENGTH LPAREN scalar_expression RPAREN                                     #LiteralLength
	| LEN LPAREN scalar_expression RPAREN										#LiteralLen
	| LEFT LPAREN scalar_expression (COMMA numbers)? RPAREN						#LiteralLeft
	| RIGHT LPAREN scalar_expression (COMMA numbers)? RPAREN					#LiteralRight
	| MID LPAREN scalar_expression COMMA numbers COMMA numbers RPAREN			#LiteralMid
	| COALESCE LPAREN scalar_expression (COMMA scalar_expression)* RPAREN					#LiteralCoalesce
	| IF LPAREN scalar_expression RPAREN THEN null_or_scalar_exp (ELSE null_or_scalar_exp)?	#LiteralIfThen
	| member_expression DOT COUNT															#LiteralMemberCount
	| member_expression DOT INDEX LPAREN member_expression RPAREN							#LiteralMemberIndex
	| identifier DOT GETVALUE LPAREN scalar_expression COMMA identifier RPAREN				#LiteralGetValue
	| ARGB LPAREN INTEGERS (COMMA INTEGERS)* RPAREN											#LiteralARGB
	| ISNULL LPAREN scalar_expression RPAREN												#LiteralIsNull
	| ISEMPTY LPAREN scalar_expression RPAREN												#LiteralIsEmpty
	| ISWHITESPACE LPAREN scalar_expression RPAREN											#LiteralIsWhiteSpace
	| SAFEDIVIDE LPAREN scalar_expression COMMA scalar_expression (COMMA scalar_expression)? RPAREN		#LiteralSafeDivide
	| SUBSTRING LPAREN scalar_expression COMMA scalar_expression (COMMA scalar_expression)? RPAREN #LiteralSubString
	;

distinct
	: DISTINCT LPAREN member_expression RPAREN
	;

member_measure_crossjoin returns [str serializedInfo, object IBPLExpressions]
@after {$ctx.serializedInfo = $ctx.getText();}
	: LPAREN RPAREN
	| LPAREN crossjoin_element (STAR crossjoin_element)* RPAREN
	;

crossjoin_element returns [str serializedInfo, object IBPLExpressions]
@after {$ctx.serializedInfo = $ctx.getText();}
	: member_expressions			#CrossJoinMembers
	| member_expression				#CrossJoinMember
	| TEMPLATE_BLOCK				#CrossJoinTemplate
	| graphNodeMembersStatement		#CrossJoinGraphNode
	| measure_element_list			#CrossJoinMeasure
	;

member_expressions returns [str serializedInfo, object IBPLExpressions]
@after {$ctx.serializedInfo = $ctx.getText();}
    : NAMEDNODE	multifilter_clause?																#NamedNodeReference
	| NAMEDNODEFILTERSET multifilter_clause?													#NamedNodeFilterSetReference
    | (graph_identifier DOT)? (from_tail | to_head) DOT NAMEDNODE multifilter_clause?			#NamedNodeGraphReference
    | (graph_identifier DOT)? (from_tail | to_head) DOT NAMEDNODEFILTERSET multifilter_clause?	#NamedNodeFilterSetGraphReference
	;

multifilter_clause returns [str serializedInfo, object IBPLExpressions]
@after {$ctx.serializedInfo = $ctx.getText();}
	: DOT FILTER LPAREN namedNode_Filter_clause (COMMA namedNode_Filter_clause)* RPAREN
	;

namedNode_Filter_clause returns [KeyValuePair<str, object> NamedNodeFilter]
	: identifier COLON scalar_expression
	;

//Member Rules
member_crossjoin returns [str serializedInfo , object IBPLExpressions]
@after {$ctx.serializedInfo = $ctx.getText();}
	: member_crossjoin DOT FILTER LPAREN exprBool=scalar_expression RPAREN
	| member_crossjoin DOT ORDERBY LPAREN exprScalar=valueExpr (COMMA opt=(DESC|ASC))? RPAREN
	| LPAREN member_expressions_or_expression (STAR member_expressions_or_expression)* RPAREN
	;

member_expression returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: BETWEEN LPAREN member_expression COMMA member_expression RPAREN						#MemberBetween
	| LBRACE member_expression (COMMA member_expression)* RBRACE							#MemberList
	| member_expression DOT (FILTER LPAREN scalar_expression RPAREN)						#MemberFilter
	| member_expression DOT (ORDERBY LPAREN valueExpr (COMMA opt=(DESC|ASC))?  RPAREN)		#MemberOrderBy
	| member_expression DOT (ANCESTORSATLEVEL LPAREN identifier RPAREN)						#MemberAncestorsAtLevel
	| member_expression DOT (DESCENDANTSATLEVEL LPAREN identifier RPAREN)					#MemberDescendantsAtLevel
	| member_expression DOT (RELATEDMEMBERS LPAREN identifier RPAREN)						#MemberRelatedMembers
	| member_expression DOT (FIND LPAREN identifier RPAREN)									#MemberFind
	| member_expression DOT (FIRSTORDEFAULT LPAREN scalar_expression RPAREN)				#MemberFirstOrDefault
	| member_expression DOT (UNIONWITH LPAREN member_expression RPAREN)						#MemberUnion
	| member_expression DOT (INTERSECTWITH LPAREN member_expression RPAREN)                 #MemberIntersect
	| member_expression DOT (EXCEPT LPAREN member_expression RPAREN)						#MemberDifference
	| member_expression DOT (FINDWITHKEY LPAREN numbers RPAREN)								#MemberFindWithKey
	| member_expression DOT (ANCESTORS LPAREN hierarchy? RPAREN)							#MemberAncestors
	| member_expression DOT (ANCESTOR LPAREN hierarchy COMMA numbers RPAREN)				#MemberAncestor
	| member_expression DOT (CHILDREN LPAREN hierarchy RPAREN)								#MemberChildren
	| member_expression DOT (ELEMENT LPAREN numbers RPAREN)									#MemberElement
	| member_expression DOT ((FIRST | FIRSTELEMENT) (LPAREN RPAREN)?)						#MemberFirstElement
	| member_expression DOT ((LAST | LASTELEMENT) (LPAREN RPAREN)?)							#MemberLastElement
	| member_expression DOT (PREVMEMBER)													#MemberPrevMember
	| member_expression DOT (NEXTMEMBER)													#MemberNextMember
	| member_expression DOT (LEADOFFSET LPAREN scalar_expression RPAREN)					#MemberLeadOffset
	| unoperated_member_set																	#MemberUnoperatedSet
	| unoperated_member																		#MemberUnoperated
	| current_vertex_coordinate_member														#CurrentVertexCoordinateMember
	| member_expression DOT (identifier) 													#MemberLevelAttribute
	| member_expression TEMPLATE_BLOCK														#MemberTemplate
	| meta_member_expression																#MemberMeta
	| currentUserStatement																	#MemberCurrentUser
	;

unoperated_member returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: named_member_expression
	| current_member_expression
	;

current_vertex_coordinate_member returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	   : (from_tail | to_head) DOT levelattribute_name DOT HASH
       ;

unoperated_member_set returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: (graph_identifier DOT (from_tail | to_head) DOT)? RESOLVABLES		#MemberSetReference
	| ARGUMENT						#MemberArgument
	| hierarchy DOT LEAFMEMBERS		#HierarchyLeafMembers
	| hierarchy DOT MEMBERS			#HierarchyMembers
	| levelattribute DOT MEMBERS	#AttributeMemberSet
	| levelattribute				#AttributeMemberSet
	| (graph_identifier DOT)? (from_tail | to_head) DOT levelattribute  (DOT identifier)?  #AttributeMemberSetFromGraphNode
	;

current_member_expression
	: HASH
	| levelattribute_name DOT HASH
	| dimension DOT HASH
	;

named_member_expression
	: levelattribute_name DOT identifier
	;

member_property
	: member_expression DOT identifier
	;

// Add more as needed. Example: MEASUREGROUP
meta_element
	: MEASURE
	;

meta_member_property
	: meta_element DOT identifier
	;

meta_member_expression returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: meta_element IN LBRACE identifier (COMMA identifier)* RBRACE						#metaMemberIn
	| META DOT meta_element																#metaMember
	;

//Olap models
dimension
	: dimension_name
	;

dimensionSet
	: dimensionList
	| ALL
	| ALL EXCEPT dimensionList
	;

dimensionList
	: dimension_name (COMMA dimension_name)*
	;

dimension_name
	: identifier
	;

dimension_expression
	: member_expression DOT DIMENSION
	;

hierarchy
	: dimension_name DOT identifier
	;

levelattribute
	: levelattribute_name
	| levelattribute_expression
	;

levelattribute_name
	: dimension_name DOT identifier
	| NAMEDNODE
	;

levelattribute_expression
	: hierarchy DOT GETLEVELATTRIBUTE LPAREN numbers RPAREN
	;

meta_levelattribute_name
	: MEASURE
	;

plan_name
	:	identifier
	;

measure_group_name
	: identifier
	;

unqualified_measure_name
	: (identifier DOT)? identifier
	;

//Measure Rules
measure_element_list
	: LBRACE measure_element (COMMA measure_element)* RBRACE
	;

measure_element
	: simple_measure_element
	| cum_measure_name
	| transient_computed_measure
	| tuple_aggregate_measure
	| fully_qualified_edge_property
	| edge_property
	| fully_qualified_edge_property_with_vertex_coordinates
	;

simple_measure_element
	: measure
	;

measure
	: measure_with_scope_or_graph_coordinates
	| measure_name
	| transient_measure_name
	| computed_plugin_measure
	| cum_measure_name
	;

measure_name returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: MEASURE DOT identifier
	| MEASURE DOT identifier DOT identifier
	;

transient_measure_name returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: TRANSIENT DOT identifier
	;

computed_plugin_measure returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: PLUGIN LPAREN instanceName=identifier (COMMA measureName=identifier)? usingArgsScopeClause? RPAREN
	;

usingArgsScopeClause returns [str serializedInfo, List<KeyValuePair<str, object>> NameValueList]
@after {$ctx.serializedInfo = $ctx.getText();}
	: USING? (argumentsClause | scopeClause)+
	;

cum_measure_name
	: CUM LPAREN measure_name RPAREN				#CumulativeMeasure
	;

transient_computed_measure
	: scalar_expression AS TRANSIENT DOT identifier
	;

tuple_aggregate_measure
	: tuple_aggregation_meas_func tuple_agg_measure_crossjoin AS TRANSIENT DOT identifier (USING scalar_expression)?
	;

tuple_agg_measure_crossjoin returns [object MemberSetExpSet, object MeasureValueExpSet]
	: LPAREN (levelattribute_name | measure_name) (STAR (levelattribute_name | measure_name))* RPAREN
	;

tuple_computed_aggregate_measure
	: tuple_aggregation_meas_func tuple_agg_measure_crossjoin (USING scalar_expression)?
	;

measure_with_scope_or_graph_coordinates returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: (MEASURE DOT)? identifier AT LPAREN vertex_coordinate (COMMA vertex_coordinate)* RPAREN
	| (MEASURE DOT)? identifier AT LPAREN member_expression (COMMA member_expression)* RPAREN
	| (MEASURE DOT)? identifier AT member_expression
	| (MEASURE DOT)? identifier DOT identifier AT LPAREN vertex_coordinate (COMMA vertex_coordinate)* RPAREN
	| (MEASURE DOT)? identifier DOT identifier AT LPAREN member_expression (COMMA member_expression)* RPAREN
	| (MEASURE DOT)? identifier DOT identifier AT member_expression
	;

vertex_coordinate
	: (graph_identifier DOT)? (from_tail | to_head) DOT vertex_coordinate_target
	;

vertex_coordinate_target returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: levelattribute_name
	| member_expression
	;

namenode_expression returns [str serializedInfo]
@after {$ctx.serializedInfo = $ctx.getText();}
	: levelattribute_name (STAR levelattribute_name)*
	;

measure_property
	: measure DOT cell_properties
	;

cell_properties
	: identifier
	;

node_properties
	: identifier
	;

tuple_aggregation_meas_func
	: COUNT
	| DISTINCTCOUNT
	;

identifier returns [str Val]
	: STRING		#String
	| ARGUMENT		#Argument
	| QUOTEDID		#QuotedId
	| ID			#Id
	;

positiveInteger returns [object Val]
        : INTEGERS #PositiveInt
	;

numbers returns [object Val]
	: MINUS INTEGERS	#NegInteger
	| INTEGERS			#Integer
	| MINUS DECIMALS	#NegDecimal
	| DECIMALS			#Decimal
	;

bools returns [bool Val]
	: TRUE				#TrueBool
	| FALSE				#FalseBool
	;



// no leading zeros

// \- since - means "range" inside [...]

//moustache template for parameters in parameterised procedures
TEMPLATE_BLOCK
    : '{{' { IsSimpleTemplate() }? .*? '}}'
    ;

//Operators

IF	: 'if';
BEGIN : 'begin';
ELSE	: 'else';
CASE	: 'case';
WHEN	: 'when';
WHERE	: 'where';
THEN	: 'then';
CARTESIAN : 'cartesian';
EVALUATEMEMBER : 'evaluatemember';
SPREAD : 'spread';
RESPREAD : 'respread';
SCOPE 	: 'scope';
FOREACH : 'for_each';
END	: 'end';
ENDIF	: 'end if';
ENDSCOPE	: 'end scope';
CREATE	: 'create';
REPLACE : 'replace';
UPDATE : 'update';
SELECT : 'select';
SET : 'set';
CELL : 'cell';
BLOCK : 'block';
INSERT: 'insert';
PARAMETERIZED : 'parameterized';
PROCEDURE : 'procedure';
PLUGIN    : 'plugin';
SCRIPT : 'script';
FUNCTION : 'function';
EXECUTE : 'exec';
EXPAND : 'expand';
CREATERELATIONSHIP : 'createrelationship';
DELETERELATIONSHIP : 'deleterelationship';
UPDATERELATIONSHIPATTR : 'updaterelationshipattrvalue';
GETRELATIONSHIPATTR : 'getrelationshipattrvalue';
CREATEVERSION : 'createversion';
CREATESCENARIO : 'createscenario';
DELETEVERSION : 'deleteversion';
MEASURE_ZERO: 'measure_zero';
MEASURE_NULLORZERO: 'measure_nullorzero';
MEASURE_NULL: 'measure_null';
UPDATESCENARIO : 'updatescenario';
UPDATEVERSIONPROPERTY : 'updateversionproperty';
SHARESCENARIO : 'sharescenario' ;
UNSHARESCENARIO : 'unsharescenario';
CREATEMEMBER : 'createmember';
UPDATEMEMBER : 'updatemember';
DELETEMEMBER : 'deletemember';
COPYMEMBER : 'copymember';
COPYMEASURE : 'copymeasure';
CRUDMEMBERS : 'crudMembers';
UPLOADDATAFILE : 'uploaddatafile';
DOWNLOADDATAFILE : 'downloaddatafile';
RESETACCESSCONTROL: 'resetaccesscontrol';
NETCHANGE_ACCESSCONTROL: 'netchange_accesscontrol';
SIMULATEWRITE: 'simulatewrite';
EXPORTALL : 'exportall';
IMPORTALL : 'importall';
GENERATEGRAPH : 'generategraph';
SAVE : 'save';
EXECSERVICECOMMAND : 'execservicecommand';
SYNC : 'sync';
REFRESH : 'refresh';
MATERIALIZED : 'materialized';
NONMATERIALIZE : 'nonmaterialize';
VIEW : 'view';
MERGE : 'merge';
DELTA : 'delta';
EXTERNAL : 'external';
LOCAL : 'local';
FROM_STAGE : 'from_stage';
INCREMENTAL : 'incremental';
GRANT: 'grant';
DENY : 'deny';
EXCLUSIVE : 'exclusive';
ADD : 'add';
MODIFY : 'modify';
DELETE : 'delete';
TRUNCATE : 'truncate';
FLUSH : 'flush';
PURGE : 'purge';
NULLIFY : 'nullify';
DECLARE: 'declare';
VERTEXSET : 'vertexset';
SUBGRAPH : 'subgraph';
INSTANCE : 'instance';
CURRENTUSER : 'currentuser';
SANITY : 'sanity';
CHECK : 'check';
COLUMNSTATS : 'columnstats';
DATEADD : 'dateadd';
DATEDIFF : 'datediff';
NEXTCOUNT : 'nextcount';
NEXTLABEL : 'nextlabel';
AMPLIFYREDO : 'amplifyredo';
RESTORE : 'restore';
STRICT : 'strict';
JOIN : 'join';


//Keywords
DDL : 'ddl';
DML	: 'dml';
ARGUMENTS : 'arguments';
AS : 'as';
READ : 'read';
WRITE : 'write';
ACCESS : 'access';
ACL_RULE : 'acl_rule';
ROLE : 'role';
ROLES : 'roles';
USING : 'using';
IN : 'in';
UPSTREAM : 'upstream';
TAIL : 'tail';
OUT : 'out';
DOWNSTREAM : 'downstream';
HEAD : 'head';
BOTH : 'both';
ALL : 'all';
TO : 'to';
FOR : 'for';
FROM : 'from';
DIMENSION	: 'dimension';
DIMENSIONS	: 'dimensions';
VERSIONNAME	: 'versionname';
HIERARCHY	: 'hierarchy';
LEVELATTRIBUTE	: 'levelattribute';
DESC	: 'desc';
ASC	: 'asc';
DYNAMIC	: 'dynamic';
STATIC	: 'static';
DATATYPE: 'int' | 'string' | 'datetime' | 'number' | 'memberset' | 'member' | 'bool';
TRUE : 'true';
FALSE : 'false';
NULL : 'null';
RETURNS : 'returns';
RETURN : 'return';
MEASURE : 'measure';
MEASURES: 'measures';
PLAN : 'plan';
PLANS : 'plans';
MODEL : 'model';
MODELS : 'models';
PARTITION : 'partition';
EXCLUDEPROPERTIES: 'exclude properties';
PARTITIONS : 'partitions';
TRANSACTION : 'transaction';
COMMIT: 'commit';
ABORT: 'abort';
INCLUDE: 'include';
ON: 'on';
AXISTYPE: 'row' | 'column';
MEMBERPROPERTIES: 'memberproperties';
ANCHORMEMBERS: 'anchormembers';
CELLPROPERTIES: 'cellproperties';
NODEPROPERTIES: 'nodeproperties';
NODETYPEMEASURES: 'nodetypemeasures';
GROUPBYMEMBERPROPERTIES: 'groupbymemberproperties';
LCID: 'lcid';
LIMIT: 'limit';
OFFSET: 'offset';
FIRST: 'first';
LAST: 'last';
TOP: 'top';
BOTTOM: 'bottom';
NULLS: 'nulls';
CUM : 'cum';
EDIT : 'edit';
COMPUTE : 'compute';
ENABLE : 'enable';
DISABLE : 'disable';
CONVERT : 'convert';
USE : 'use';
ALIASES : 'aliases';
NULLS_FOR_UNRELATED_ATTR_SELECT : 'nulls_for_unrelated_attr_select';
NULLS_FOR_FINER_GRAIN_SELECT : 'nulls_for_finer_grain_select';
INCLUDEALLVALUESWITHFILTER : 'includeallvalueswithfilter';
APPLY_CARTESIAN : 'apply_cartesian';
INCLUDE_SUBTOTALS : 'include_subtotals';
INCLUDE_VISUAL_SUBTOTALS : 'include_visual_subtotals';
INCLUDE_NULLMEMBERS : 'include_nullmembers';
FILTER_BY_UPDATES : 'filter_by_updates';
FILTER_BY_UPDATES_IN_ALERTS : 'filter_by_updates_in_alerts';
TRANSIENT : 'transient';
GRAPH : 'graph' | 'relationshiptype';
GRAPHS : 'graphs' | 'relationshiptypes';
EDGE : 'edge' | 'relationship';
EDGES : 'edges' | 'relationships';
PROPERTIES : 'properties';
NODE : 'node';
META : 'meta';
ALERT : 'alert';
REGISTER : 'register';
DEREGISTER : 'deregister';
GARBAGE : 'garbage';
COLLECT : 'collect';
RELEASE : 'release';
MEMORY : 'memory';
POWERSHELL : 'powershell';
DATA : 'data';
RECURRENCE : 'recurrence';
ORDERED : 'ordered';
DEPENDENT : 'dependent';
GATHER : 'gather';
STATS : 'stats';
PARALLEL: 'parallel';
COPYTO: 'copyto';
CASCADE : 'cascade';
SERIES : 'series';
REFER_PARENT : 'refer_parent';
REFER_PARENT_FOR_OTHERS : 'refer_parent_for_others';
REFER_SELF_FOR_OTHERS : 'refer_self_for_others';
REFER_SELF : 'refer_self';
EXCLUDE : 'exclude';
ALL_OTHERS : 'all_others';
OBFUSCATE : 'obfuscate';
FOR_UPGRADE : 'for_upgrade';
MATERIALIZE : 'materialize';
ASSOCIATION : 'association';
WITH : 'with';
CALCULATED : 'calculated';
AUTHOR : 'author';
SNAPSHOT : 'snapshot';
DELETEFROMDISK : 'deletefromdisk';
BACKGROUND : 'background';
CALCULATEDMEMBEROVERRIDES : 'calculatedmemberoverrides';
ACCESSCONTROLRULESINFO : 'accesscontrolrulesinfo';
POST_ACTION : 'post_action';
SEQUENTIAL : 'sequential';
INITIALIZE : 'initialize';
CREATELWSCENARIO : 'createlwscenario';
CREATEEPHEMERALSCENARIO : 'createephemeralscenario';
HIGHLIGHT_CORRUPT_PARTITIONS : 'highlight_corrupt_partitions';
EXEC_INCREMENTAL_PLAN : 'exec_incremental_plan';
ENTITIES : 'entities';

//Functions
MEMBERS	: 'members';
CURRENTMEMBER	: 'currentmember';
LEAFMEMBERS	: 'leafmembers';
ELEMENT	: 'element';
FIRSTELEMENT	: 'firstelement';
LASTELEMENT	: 'lastelement';
INDEX : 'index';
PARENT	: 'parent';
CHILDREN	: 'children';
LASTCHILD	: 'lastchild';
FIRSTCHILD	: 'firstchild';
ANCESTOR	: 'ancestor';
ANCESTORS	: 'ancestors';
ANCESTORSATLEVEL: 'ancestorsatlevel';
DESCENDANTS	: 'descendants';
DESCENDANTSATLEVEL	: 'descendantsatlevel';
RELATEDMEMBERS	: 'relatedmembers';
UNIONWITH	: 'unionwith';
INTERSECTWITH : 'intersectwith';
DISTINCT	: 'distinct';
FILTER	: 'filter';
FILTERBY	: 'filterby';
ORDERBY	: 'orderby';
EXCEPT	: 'except';
UNION	: 'union';
BETWEEN	: 'between';
PREVMEMBER: 'prevmember';
NEXTMEMBER: 'nextmember';
LEADOFFSET:	'leadoffset';
TRAVERSE : 'traverse';
START : 'start';
STEPS : 'steps';
PARENTCHILD : 'parentchild';
NOW : 'now';
LASTCOMMITTIME : 'lastcommittime';
LASTUPDATETIME : 'lastupdatetime';
DATEVALUE : 'datevalue';
TODATETIME : 'todatetime';
ABS : 'abs';
CEILING : 'ceiling';
DIV : 'div';
FLOOR : 'floor';
INTEGER : 'integer';
FLOAT : 'float';
TOSTRING : 'tostring';
LOG : 'ln' | 'log';
EXP : 'exp';
RANDOM : 'random';
ROUND : 'round';
SUM : 'sum';
SUMPRODUCT : 'sumproduct';
AVG : 'avg';
AVGWITHNULLS : 'avgwithnulls';
CORREL : 'correl';
COUNT : 'count';
DISTINCTCOUNT : 'distinctcount';
MIN : 'min';
MAX : 'max';
CONCATENATE : 'concatenate';
LEN : 'len';
LEFT : 'left';
RIGHT : 'right';
UPPER : 'upper';
LOWER : 'lower';
MID : 'mid';
GETVALUE : 'getvalue';
COALESCE : 'coalesce';
LENGTH : 'length';
SUBSTRING : 'substring';
LIKE : 'like';
CONTAINS : 'contains';
STARTSWITH : 'startswith';
ENDSWITH : 'endswith';
CONTAINSREGEXP : 'containsregexp';
ARGB : 'argb';
ISNULL : 'isnull';
ISEMPTY : 'isempty';
ISWHITESPACE : 'iswhitespace';
SAFEDIVIDE : 'safedivide';
START_BATCH: 'start_batch';
END_BATCH: 'end_batch';
REPLAY: 'replay';
HAREDIS: 'haredis';
EXPLAIN: 'explain';

//o9IBPL Functions
GETLEVELATTRIBUTE: 'getlevelattribute';
FIND	: 'find';
FINDWITHKEY	: 'findwithkey';
FIRSTORDEFAULT : 'firstordefault';

/* !! Warning !! Nested usage does not work !!  */
// This captures (possibly non-IBPL) text of procedure body
PROC_BODY : (options {greedy=false;} : 'begin' WS+? 'procedure' .+? 'end' WS+? 'procedure');
// This captures (possibly non-IBPL) text of json
JSON_BLOCK : (options {greedy=false;} : 'begin' WS+? 'jsonblock' .+? 'end' WS+? 'jsonblock');

DOT	: '.';
COLON	: ':' ;
COMMA	: ',' ;
SEMICOLON	: ';' ;

LPAREN	: '(' ;
RPAREN	: ')' ;
LBRACKET 	: '[' ;
RBRACKET 	: ']' ;
LBRACE	: '{';
RBRACE	: '}';
//SPECIALTOK	: 'A+A+';
ASSIGN	: '=' ;
OR      	: '||';
AND     	: '&&';
EQUALS  	: '==';
NOTEQUAL	: '<>' | '!=' ;
LESSTHAN	: '<' ;
LESSTHANOREQUALTO	: '<=' | '!>' ;
GREATERTHANOREQUALTO	: '>=' | '!<' ;
GREATERTHAN 	: '>' ;

DIVIDE	: '/' ;
PLUS	: '+' ;
MINUS	: '-' ;
STAR	: '*' ;
MOD		: '%' ;
POWER	: '^' | 'power' ;

QUESTION	: '?';
AMPERSAND 	: '&' ;
TILDE	: '~' ;
BITWISEOR 	: '|' ;
DOTSTAR 	: '.*' ;
HASH	: '#';
AT	: '@';

ID  	: ('a'..'z'|'_') ('a'..'z'|'0'..'9'|'_')*;
//ID  	: ('a'..'z'|'_') ('a'..'z'|'0'..'9'|'_')* ('a'..'r'|'t'..'z'|'0'..'9'|'_');
//PLURALID: ('a'..'z'|'_') ('a'..'z'|'0'..'9'|'_')* 's';
QUOTEDID	: '[' ( ESC_SEQ | ~('"'|'['|']') )* ']';
//AMPQUOTEDID	: '[&' (ID ((' ' | '\t')+ ID)* | INTEGERS) ']';

INTEGERS 	: '0'..'9'+;
DECIMALS	: ('0'..'9')+ '.' ('0'..'9')* EXPONENT?
    	| '.' ('0'..'9')+ EXPONENT?
    	| ('0'..'9')+ EXPONENT
   	;

COMMENT : ('//' .*? '\r'? '\n'
		| '/*' .*? '*/') -> channel(HIDDEN)
		;

WS  	: ( ' '
			| ' '
        	| '\t'
        	| '\r'
        	| '\n'
       	 ) -> channel(HIDDEN)
    	;

ARGUMENT : '$' ('a'..'z'|'0'..'9'|'_')*;
RESOLVABLES : '&' ('a'..'z'|'0'..'9'|'_')*;
NAMEDNODE : '$$' ('a'..'z'|'0'..'9'|'_')+;
NAMEDNODEFILTERSET : '%%' ('a'..'z'|'0'..'9'|'_')+;
STRING	: '"' ( ESC_SEQ | ~('"') )* '"';

CHAR	: '\'' ( ESC_SEQ | ~('\''|'\\') ) '\'';

fragment
EXPONENT 	: ('e'|'E') ('+'|'-')? ('0'..'9')+ ;

fragment
HEX_DIGIT 	: ('0'..'9'|'a'..'f'|'A'..'F') ;

fragment
ESC_SEQ	: '\\' ('b'|'t'|'n'|'f'|'r'|'"'|'\''|'\\')
    	| UNICODE_ESC
    	| OCTAL_ESC
    	;

fragment
OCTAL_ESC	: '\\' ('0'..'3') ('0'..'7') ('0'..'7')
    	| '\\' ('0'..'7') ('0'..'7')
    	| '\\' ('0'..'7')
    	;

fragment
UNICODE_ESC	: '\\' 'u' HEX_DIGIT HEX_DIGIT HEX_DIGIT HEX_DIGIT;
