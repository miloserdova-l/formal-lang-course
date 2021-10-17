import os

import pytest

from pyformlang.cfg import CFG
from pyformlang.cfg import Production, Variable, Terminal
from project import cfg_to_normal_form, read_cfg_from_file

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(
    params=[
        """
    """,
        # цепные
        """
        A -> B
        B -> C
        C -> A A
        A -> epsilon
    """,
        # непорождающие
        """
        S -> a S
        S -> epsilon
        A -> a
    """,
        # длинные
        """
        S -> A S B
        S -> epsilon
        A -> a
        B -> b
    """,
        # epsilon
        """
        S -> A S B
        S -> epsilon
        A -> a
        B -> epsilon
    """,
    ]
)
def cfg(request):
    return CFG.from_text(request.param)


def test_cfg_to_normal_form(cfg):
    cnf = cfg_to_normal_form(cfg)
    assert cnf.is_normal_form()


@pytest.mark.parametrize(
    "path, expected",
    [
        ("cfg-1.txt", set()),
        ("cfg-2.txt", {Production(Variable("S"), [Terminal("a")])}),
        (
            "cfg-3.txt",
            {
                Production(Variable("A"), [Variable("B")]),
                Production(Variable("B"), [Variable("C")]),
                Production(Variable("C"), [Variable("A"), Variable("A")]),
                Production(Variable("A"), []),
                Production(Variable("A"), [Terminal("a")]),
            },
        ),
    ],
)
def test_read_cfg_from_file(path, expected):
    cfg = read_cfg_from_file(os.sep.join([root_path, "tests", "resources", path]))
    actual = cfg.productions

    assert actual == expected
