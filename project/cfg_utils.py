from functools import reduce

from pyformlang.cfg import CFG, Production
from pyformlang.regular_expression import PythonRegex

from project.ecfg import ECFG
from project.rsm import RSM


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
    dependencies = dict()
    for p in cfg.productions:
        cur = dependencies.get(p.head, list())
        cur.append(p.body)
        dependencies[p.head] = cur
    productions = dict(
        map(lambda kv: (kv[0], __get_regex(kv[1])), dependencies.items())
    )
    return ECFG(cfg.variables, cfg.terminals, cfg.start_symbol, productions)


def ecfg_to_rsm(ecfg: ECFG) -> RSM:
    boxes = dict()
    for k, v in ecfg.productions.items():
        boxes[k] = v.to_epsilon_nfa().to_deterministic()
    return RSM(ecfg.start_symbol, boxes)


def __get_regex(body: list) -> PythonRegex:
    return reduce(
        lambda f, s: f.union(s),
        [__get_concat(elem) for elem in body],
    )


def __get_concat(elem: list) -> PythonRegex:
    if len(elem) == 0:
        return PythonRegex("")
    return reduce(
        lambda x, y: x.concatenate(y), [PythonRegex(symbol.value) for symbol in elem]
    )
