from typing import AbstractSet

from pyformlang.cfg import Variable, Terminal
from pyformlang.regular_expression import PythonRegex


class ECFG:
    def __init__(
        self,
        variables: AbstractSet[Variable] = None,
        terminals: AbstractSet[Terminal] = None,
        start_symbol: Variable = None,
        productions: dict[Variable, PythonRegex] = None,
    ):
        self.variables = variables
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.productions = productions if productions else dict[Variable, PythonRegex]()
