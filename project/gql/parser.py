from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker, ParserRuleContext
from antlr4.error.Errors import ParseCancellationException
from antlr4.tree.Tree import TerminalNodeImpl
from pydot import Dot, Node, Edge

from project.gql.GQLLexer import GQLLexer
from project.gql.GQLParser import GQLParser
from project.gql.GQLListener import GQLListener

__all__ = ["parse", "accept", "generate_dot"]



def parse(text: str) -> GQLParser:
    input_stream = InputStream(text)
    lexer = GQLLexer(input_stream)
    lexer.removeErrorListeners()
    token_stream = CommonTokenStream(lexer)
    parser = GQLParser(token_stream)

    return parser


def accept(text: str) -> bool:
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.prog()

    return parser.getNumberOfSyntaxErrors() == 0


def generate_dot(text: str, path: str):
    if not accept(text):
        raise ParseCancellationException("The word doesn't match the grammar")
    ast = parse(text).prog()
    tree = Dot("tree", graph_type="digraph")
    ParseTreeWalker().walk(DotTreeListener(tree, GQLParser.ruleNames), ast)
    tree.write(path)


class DotTreeListener(GQLListener):
    def __init__(self, tree: Dot, rules):
        super(DotTreeListener, self).__init__()
        self.tree = tree
        self.num_nodes = 0
        self.nodes = {}
        self.rules = rules

    def enterEveryRule(self, ctx: ParserRuleContext):
        if ctx not in self.nodes:
            self.num_nodes += 1
            self.nodes[ctx] = self.num_nodes
        if ctx.parentCtx:
            self.tree.add_edge(Edge(self.nodes[ctx.parentCtx], self.nodes[ctx]))
        label = self.rules[ctx.getRuleIndex()]
        self.tree.add_node(Node(self.nodes[ctx], label=label))

    def visitTerminal(self, node: TerminalNodeImpl):
        self.num_nodes += 1
        self.tree.add_edge(Edge(self.nodes[node.parentCtx], self.num_nodes))
        self.tree.add_node(Node(self.num_nodes, label=f"TERM: {node.getText()}"))
