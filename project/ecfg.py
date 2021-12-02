from typing import AbstractSet, Union

from pyformlang.cfg import Variable, Terminal


class ECFG:
    def __init__(
        self,
        variables: AbstractSet[Variable] = None,
        terminals: AbstractSet[Terminal] = None,
        start_symbol: Variable = None,
        productions: dict[Variable, list[list[Union[Variable, Terminal]]]] = None,
    ):
        self.variables = variables
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.productions = (
            productions
            if productions
            else dict[Variable, list[list[Union[Variable, Terminal]]]]()
        )
