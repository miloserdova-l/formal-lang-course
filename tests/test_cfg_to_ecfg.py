import pytest
from pyformlang.cfg import CFG, Variable, Terminal

from project.cfg_utils import cfg_to_ecfg
from project.regex_utils import regex_to_min_dfa
from project.rsm import get_regex


@pytest.mark.parametrize(
    "cfg, regex",
    [
        (
            """
            S -> B
            B -> C
            C -> S S
            S -> epsilon
            S -> a
        """,
            {
                Variable("S"): [[Variable("B")], [Terminal("a")], [Terminal("")]],
                Variable("B"): [[Variable("C")]],
                Variable("C"): [[Variable("S"), Variable("S")]],
            },
        ),
        (
            """
            S -> a S
            S -> epsilon
        """,
            {
                Variable("S"): [[Terminal("a"), Variable("S")], [Terminal("")]],
            },
        ),
        (
            """
            S -> A B
            S -> epsilon
            A -> a
            B -> epsilon
            B -> b
        """,
            {
                Variable("S"): [[Variable("A"), Variable("B")], [Terminal("")]],
                Variable("A"): [[Terminal("a")]],
                Variable("B"): [[Terminal("b")], [Terminal("")]],
            },
        ),
    ],
)
def test_cfg_to_ecfg(cfg, regex):
    cfg = CFG.from_text(cfg)
    ecfg = cfg_to_ecfg(cfg)
    assert set(ecfg.productions.keys()) == set(regex.keys())
    assert all(
        regex_to_min_dfa(get_regex(ecfg.productions.get(x))).is_equivalent_to(
            regex_to_min_dfa(get_regex(regex.get(x)))
        )
        for x in ecfg.productions.keys()
    )
