from antlr4 import InputStream, CommonTokenStream

from project.gql.GQLLexer import GQLLexer
from project.gql.GQLParser import GQLParser

__all__ = ["parse", "accept"]


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
