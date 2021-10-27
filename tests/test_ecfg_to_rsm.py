import pytest
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import PythonRegex

from project.cfg_utils import ecfg_to_rsm, cfg_to_ecfg
from project.regex_utils import regex_to_min_dfa


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
                Variable("S"): PythonRegex("B|a|"),
                Variable("B"): PythonRegex("C"),
                Variable("C"): PythonRegex("SS"),
            },
        ),
        (
            """
            S -> a S |
        """,
            {
                Variable("S"): PythonRegex("aS|"),
            },
        ),
        (
            """
            S -> A B |
            A -> a
            B -> b |
        """,
            {
                Variable("S"): PythonRegex("AB|"),
                Variable("A"): PythonRegex("a"),
                Variable("B"): PythonRegex("b|"),
            },
        ),
    ],
)
def test_ecfg_to_rsm(cfg, regex):
    cfg = CFG.from_text(cfg)
    rsm = ecfg_to_rsm(cfg_to_ecfg(cfg))
    assert set(rsm.boxes.keys()) == set(regex.keys())
    assert all(
        rsm.boxes.get(x).is_equivalent_to(regex_to_min_dfa(regex.get(x)))
        for x in rsm.boxes.keys()
    )
