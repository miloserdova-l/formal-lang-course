import pytest
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import PythonRegex

from project.cfg_utils import cfg_to_ecfg
from project.regex_utils import regex_to_min_dfa


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
                Variable("S"): PythonRegex("B|a|"),
                Variable("B"): PythonRegex("C"),
                Variable("C"): PythonRegex("SS"),
            },
        ),
        (
            """
            S -> a S
            S -> epsilon
        """,
            {
                Variable("S"): PythonRegex("aS|"),
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
                Variable("S"): PythonRegex("AB|"),
                Variable("A"): PythonRegex("a"),
                Variable("B"): PythonRegex("b|"),
            },
        ),
    ],
)
def test_cfg_to_ecfg(cfg, regex):
    cfg = CFG.from_text(cfg)
    ecfg = cfg_to_ecfg(cfg)
    assert set(ecfg.productions.keys()) == set(regex.keys())
    assert all(
        regex_to_min_dfa(ecfg.productions.get(x)).is_equivalent_to(
            regex_to_min_dfa(regex.get(x))
        )
        for x in ecfg.productions.keys()
    )
