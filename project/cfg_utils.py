from pyformlang.cfg import CFG


def cfg_to_normal_form(cfg: CFG) -> CFG:
    return cfg.to_normal_form()


def read_cfg_from_file(path: str, start_symbol: str = "S") -> CFG:
    with open(path) as f:
        return CFG.from_text(f.read(), start_symbol=start_symbol)
