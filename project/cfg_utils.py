from pyformlang.cfg import CFG, Production
from project.ecfg import ECFG


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
    productions = dict(map(lambda kv: (kv[0], kv[1]), dependencies.items()))
    return ECFG(cfg.variables, cfg.terminals, cfg.start_symbol, productions)
