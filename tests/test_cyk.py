import pytest
from pyformlang.cfg import CFG, Terminal

from project.CYK import cyk


@pytest.mark.parametrize(
    "cnf, accepted, rejected",
    [
        (
            """
                S -> B B
                S -> C D
                S -> epsilon
                B -> B B
                B -> C D
                C -> (
                D -> B E
                D -> )
                E -> )
            """,
            [
                [Terminal("("), Terminal(")")],
                [
                    Terminal("("),
                    Terminal("("),
                    Terminal("("),
                    Terminal(")"),
                    Terminal(")"),
                    Terminal(")"),
                ],
                [],
                [
                    Terminal("("),
                    Terminal("("),
                    Terminal("("),
                    Terminal(")"),
                    Terminal(")"),
                    Terminal(")"),
                    Terminal("("),
                    Terminal(")"),
                ],
                [
                    Terminal("("),
                    Terminal(")"),
                    Terminal("("),
                    Terminal(")"),
                    Terminal("("),
                    Terminal("("),
                    Terminal(")"),
                    Terminal(")"),
                ],
            ],
            [
                [Terminal("(")],
                [Terminal(")")],
                [Terminal("("), Terminal("("), Terminal(")")],
                [Terminal("("), Terminal(")"), Terminal(")")],
                [Terminal("("), Terminal(")"), Terminal(")"), Terminal(")")],
            ],
        ),
        (
            """
                S -> A B
                A -> C D
                B -> E F
                C -> l
                D -> o
                E -> v
                F -> e
            """,
            [[Terminal("l"), Terminal("o"), Terminal("v"), Terminal("e")]],
            [[], [Terminal("l"), Terminal("o")], [Terminal("A"), Terminal("B")]],
        ),
    ],
)
def test_cyk(cnf, accepted, rejected):
    cnf = CFG.from_text(cnf)
    assert all(cyk(s, cnf) for s in accepted)
    assert all(not cyk(s, cnf) for s in rejected)
