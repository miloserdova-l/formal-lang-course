from pyformlang.cfg import CFG, Production, Variable, Terminal
from pyformlang.regular_expression import PythonRegex
from typing import AbstractSet, Iterable

from project import regex_to_min_dfa
from project.rsm import RecursiveStateMachine


def cfg_to_normal_form(cfg: CFG) -> CFG:
    is_gen_eps = cfg.generate_epsilon()
    cfg = cfg.to_normal_form()

    if is_gen_eps:
        return CFG(
            cfg.variables,
            cfg.terminals,
            cfg.start_symbol,
            cfg.productions | {Production(cfg.start_symbol, [])},
        )

    return cfg


def read_cfg_from_file(path: str, start_symbol: str = "S") -> CFG:
    with open(path) as f:
        return CFG.from_text(f.read(), start_symbol=start_symbol)


def cfg_to_ecfg(cfg: CFG):
    return ECFG(cfg.variables, cfg.terminals, cfg.start_symbol, cfg.productions)


class ECFG(CFG):
    def __init__(
        self,
        variables: AbstractSet[Variable] = None,
        terminals: AbstractSet[Terminal] = None,
        start_symbol: Variable = None,
        productions: Iterable[Production] = None,
    ):
        cfg = CFG(
            variables=variables,
            terminals=terminals,
            start_symbol=start_symbol,
            productions=productions,
        )

        cfg = cfg_to_normal_form(cfg)

        super(ECFG, self).__init__(
            variables=cfg.variables,
            terminals=cfg.terminals,
            start_symbol=cfg.start_symbol,
            productions=cfg.productions,
        )

        self.dependencies = dict()

        for p in self.productions:
            cur = self.dependencies.get(p.head, list())
            cur.append(p.body)
            self.dependencies[p.head] = cur

    def to_rsm(self) -> RecursiveStateMachine:
        rsm = RecursiveStateMachine()

        rsm.start_symbol = self.start_symbol

        for p in self.dependencies.keys():
            rsm.boxes[p] = regex_to_min_dfa(self.__get_regex(self.dependencies.get(p)))

        return rsm

    @staticmethod
    def __get_regex(body: list) -> PythonRegex:
        cur_r = None
        for conjunction in body:
            if len(conjunction) == 0:
                new_r = PythonRegex("")
            else:
                new_r = PythonRegex(conjunction[0].value)
                if len(conjunction) > 1:
                    new_r = new_r.concatenate(PythonRegex(conjunction[1].value))
            if cur_r is None:
                cur_r = new_r
            else:
                cur_r = cur_r.union(new_r)
        return cur_r
