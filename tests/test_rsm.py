import pytest
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import PythonRegex

from project import regex_to_min_dfa
from project.cfg_utils import ECFG


@pytest.mark.parametrize(
    "cfg, variables, regex",
    [
        (
            """
            S -> B
            B -> C
            C -> S S
            S -> epsilon
            S -> a
        """,
            {Variable("S")},
            {Variable("S"): PythonRegex("SS|a|")},
        ),
        (
            """
            S -> a S
            S -> epsilon
        """,
            {Variable("S"), Variable("a#CNF#")},
            {
                Variable("a#CNF#"): PythonRegex("a"),
                Variable("S"): PythonRegex("a#CNF#S|a|"),
            },
        ),
        (
            """
            S -> A B
            S -> epsilon
            A -> a
            B -> epsilon
        """,
            {Variable("S")},
            {Variable("S"): PythonRegex("a|")},
        ),
    ],
)
def test_ecfg_to_rsm(cfg, variables, regex):
    cfg = CFG.from_text(cfg)
    rsm = ECFG(cfg.variables, cfg.terminals, cfg.start_symbol, cfg.productions).to_rsm()
    assert set(rsm.boxes.keys()) == variables
    assert all(
        rsm.boxes[x].is_equivalent_to(regex_to_min_dfa(regex[x]))
        for x in rsm.boxes.keys()
    )
