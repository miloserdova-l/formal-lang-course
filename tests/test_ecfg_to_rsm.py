import pytest
from pyformlang.cfg import CFG, Variable, Terminal

from project.cfg_utils import cfg_to_ecfg
from project.regex_utils import regex_to_min_dfa
from project.rsm import RSM, get_regex


@pytest.mark.parametrize(
    "cfg, regex",
    [
        (
            """
            S -> B | a |
            B -> C
            C -> S S
        """,
            {
                Variable("S"): [[Variable("B")], [Terminal("a")], [Terminal("")]],
                Variable("B"): [[Variable("C")]],
                Variable("C"): [[Variable("S"), Variable("S")]],
            },
        ),
        (
            """
            S -> a S |
        """,
            {
                Variable("S"): [[Terminal("a"), Variable("S")], [Terminal("")]],
            },
        ),
        (
            """
            S -> A B |
            A -> a
            B -> b |
        """,
            {
                Variable("S"): [[Variable("A"), Variable("B")], [Terminal("")]],
                Variable("A"): [[Terminal("a")]],
                Variable("B"): [[Terminal("b")], [Terminal("")]],
            },
        ),
    ],
)
def test_ecfg_to_rsm(cfg, regex):
    cfg = CFG.from_text(cfg)
    rsm = RSM(cfg_to_ecfg(cfg))
    assert set(rsm.boxes.keys()) == set(regex.keys())
    assert all(
        rsm.boxes.get(x).is_equivalent_to(regex_to_min_dfa(get_regex(regex.get(x))))
        for x in rsm.boxes.keys()
    )
