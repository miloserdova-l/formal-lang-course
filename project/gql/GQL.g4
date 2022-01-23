grammar GQL;

prog : (EOL? WS? stmt SEMI EOL?)+ EOF;

stmt : PRINT expr
     | VAR WS? ASSIGN WS? expr
     ;

val : string
    | integer
    | boolean
    | path
    ;

boolean : BOOL;
integer : INT;
string : STRING;
path : PATH;

var : VAR;

expr : var
     | val
     | graph_
     | vertices
     | edges
     | labels
     | mapping
     | filtering
     | anfunc
     | NOT expr
     | expr IN expr
     | expr AND expr
     | expr DOT expr
     | expr OR expr
     | expr KLEENE
     | LP expr RP
     ;

graph_ : string
      | set_start
      | set_final
      | add_start
      | add_final
      | load_graph
      | cfg
      | intersect
      | LP graph_ RP
      ;

intersect : INTERSECT (graph_ | var) WITH (graph_ | var) ;
load_graph : LOAD GRAPH (path | string);
set_start : SET START OF (graph_ | var) TO (vertices | var);
set_final : SET FINAL OF (graph_ | var) TO (vertices | var);
add_start : ADD START OF (graph_ | var) TO (vertices | var);
add_final : ADD FINAL OF (graph_ | var) TO (vertices | var);
cfg : CFG;

vertices : vertex
       | vertices_set
       | vertices_range
       | get_final
       | get_start
       | get_reachable
       | get_vertices
       | LP vertices RP
       ;


vertex : INT;
vertices_set : LCB (INT COMMA)* (INT)? RCB
             | vertices_range;
vertices_range : LCB INT DOT DOT INT RCB;
get_final : GET FINAL VERTICES FROM (graph_ | var);
get_start : GET START VERTICES FROM (graph_ | var);
get_vertices : GET VERTICES FROM (graph_ | var);
get_reachable : GET REACHABLE VERTICES FROM (graph_ | var);

edges : edge
      | edges_set
      | get_edges;

edge : LP vertex COMMA label COMMA vertex RP
     | LP vertex COMMA vertex RP;

get_edges : GET EDGES FROM (graph_ | var);
edges_set : LCB (edge COMMA)* (edge)? RCB;

labels : label
       | labels_set
       | get_labels;

label : string;
labels_set : LCB (STRING COMMA)* (STRING)? RCB;
get_labels : GET LABELS FROM (graph_ | var);

mapping : MAP anfunc expr;
filtering : FILTER anfunc expr;

anfunc : FUN variables COLON expr
       | LP anfunc RP;

variables : (var COMMA)* var?
     | var_edge;

var_edge : LP var COMMA var RP
         | LP var COMMA var COMMA var RP
         | LP LP var COMMA var RP COMMA var COMMA LP var COMMA var RP RP
         ;

FUN : WS? 'fun' WS?;
LOAD : WS? 'load' WS? ;
SET : WS? 'set' WS? ;
ADD : WS? 'add' WS? ;
OF : WS? 'of' WS? ;
TO : WS? 'to' WS? ;
GRAPH : WS? 'graph' WS?;
VERTICES : WS? 'vertices' WS? ;
LABELS : WS? 'labels' WS? ;
GET : WS? 'get' WS? ;
EDGES : WS? 'edges' WS? ;
REACHABLE : WS? 'reachable' WS? ;
START : WS? 'start' WS? ;
FINAL : WS? 'final' WS? ;
FROM : WS? 'from' WS? ;
FILTER : WS? 'filter' WS? ;
MAP : WS? 'map' WS? ;
PRINT : WS? 'print' WS?;
BOOL : TRUE | FALSE;
TRUE : 'true' ;
FALSE : 'false' ;
INTERSECT : 'intersect';
WITH : 'with';

ASSIGN : WS? '=' WS? ;
AND : WS? '&' WS?;
OR : WS? '|' WS? ;
NOT : WS? 'not' WS? ;
IN : WS? 'in' WS?;
KLEENE : WS? '*' WS?;
DOT : WS? '.' WS? ;
COMMA : WS? ',' WS?;
SEMI : ';' WS?;
LCB : '{' WS?;
RCB : WS? '}' WS?;
LP : '(' WS?;
RP : WS? ')' ;
QUOT : '"' ;
TRIPLE_QUOT : '"""' ;
COLON : ':' ;
ARROW : '->' ;

VAR : ('_' | CHAR) ID_CHAR* ;

INT : NONZERO_DIGIT DIGIT* | '0' ;
CFG : TRIPLE_QUOT (CHAR | DIGIT | ' ' | '|' | '\n' | ARROW)* TRIPLE_QUOT ;
STRING : QUOT (CHAR | DIGIT | '_' | ' ')* QUOT ;
PATH : QUOT (CHAR | DIGIT | '_' | ' ' | '/' | DOT)* QUOT ;
ID_CHAR : (CHAR | DIGIT | '_');
CHAR : [a-z] | [A-Z];
NONZERO_DIGIT : [1-9];
DIGIT : [0-9];
WS : [ \t\r]+ -> skip;
EOL : [\n]+;
