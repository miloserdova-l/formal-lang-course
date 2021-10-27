import os

import pytest

from pyformlang.cfg import CFG
from pyformlang.cfg import Production, Variable, Terminal
from project import cfg_to_normal_form, read_cfg_from_file

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.parametrize(
    "cfg, gen_eps",
    [
        (
            """
    """,
            False,
        ),
        # цепные
        (
            """
        A -> B
        B -> C
        C -> A A
        A -> epsilon
    """,
            False,
        ),
        # непорождающие
        (
            """
        S -> a S
        S -> epsilon
        A -> a
    """,
            True,
        ),
        # длинные
        (
            """
        S -> A S B
        S -> epsilon
        A -> a
        B -> b
    """,
            True,
        ),
        # epsilon
        (
            """
        S -> A S B
        S -> epsilon
        A -> a
        B -> epsilon
    """,
            True,
        ),
    ],
)
def test_cfg_to_normal_form(cfg, gen_eps):
    cnf = cfg_to_normal_form(CFG.from_text(cfg))
    assert all(
        production.is_normal_form() if production.body else True
        for production in cnf.productions
    )
    assert cnf.generate_epsilon() == gen_eps


@pytest.mark.parametrize(
    "path, expected",
    [
        ("cfg-1.txt", set()),
        ("cfg-2.txt", {Production(Variable("S"), [Terminal("a")])}),
        (
            "cfg-3.txt",
            {
                Production(Variable("S"), [Variable("B")]),
                Production(Variable("B"), [Variable("C")]),
                Production(Variable("C"), [Variable("S"), Variable("S")]),
                Production(Variable("S"), []),
                Production(Variable("S"), [Terminal("a")]),
            },
        ),
    ],
)
def test_read_cfg_from_file(path, expected):
    cfg = read_cfg_from_file(os.sep.join([root_path, "tests", "resources", path]))
    actual = cfg.productions

    assert actual == expected


@pytest.mark.parametrize(
    "cfg, accepted, rejected",
    [
        (
            """
        """,
            [],
            ["", "a"],
        ),
        (
            """
                S -> a S
                S -> epsilon
                A -> a
            """,
            ["", "a", "aa", "aaaaaaaaa"],
            ["aS", "ab"],
        ),
        (
            """
                S -> A S B
                S -> epsilon
                A -> a
                B -> b
            """,
            ["", "ab", "aabb", "aaaaabbbbb"],
            ["abab", "aabbb", "aaabb", "ba"],
        ),
        (
            """
                S -> A S B
                S -> epsilon
                A -> a
                B -> epsilon
                B -> b
            """,
            ["", "ab", "aabb", "aaaaabbbbb", "aaaab", "aaabb", "aaa"],
            ["ba", "abab", "aabbb"],
        ),
    ],
)
def test_equivalence(cfg, accepted, rejected):
    cfg = CFG.from_text(cfg)
    cnf = cfg_to_normal_form(cfg)
    assert all(cnf.contains(w) and cfg.contains(w) for w in accepted) and all(
        not cnf.contains(w) and not cfg.contains(w) for w in rejected
    )
