from typing import AbstractSet

from pyformlang.cfg import Variable


class ECFG:
    def __init__(
        self,
        variables: AbstractSet = None,
        terminals: AbstractSet = None,
        start_symbol: Variable = None,
        productions: dict = None,
    ):
        self.variables = variables
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.productions = productions if productions else dict()
