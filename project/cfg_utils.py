from pyformlang.cfg import CFG, Production


def cfg_to_normal_form(cfg: CFG) -> CFG:
    is_gen_eps = cfg.generate_epsilon()
    cfg = cfg.to_normal_form()

    if is_gen_eps is True:
        cfg.productions |= {Production(cfg.start_symbol, [])}

    return cfg


def read_cfg_from_file(path: str, start_symbol: str = "S") -> CFG:
    with open(path) as f:
        return CFG.from_text(f.read(), start_symbol=start_symbol)
