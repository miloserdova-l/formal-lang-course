import pytest
from cfpq_data import labeled_cycle_graph
from pyformlang.cfg import CFG

from project import create_labeled_two_cycles_graph
from project.cfpq.cfpq import cfpq_hellings, cfpq_matrix


@pytest.mark.parametrize(
    "cfg, graph, start_nodes, final_nodes, exp_ans",
    [
        (
            """
            S -> epsilon
            """,
            labeled_cycle_graph(5, "a"),
            None,
            None,
            {(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)},
        ),
        (
            """
                S -> a | epsilon
                """,
            labeled_cycle_graph(3, "a"),
            {0},
            {0, 1},
            {
                (0, 0),
                (0, 1),
            },
        ),
        (
            """
                S -> A B
                S -> A C
                C -> S B
                A -> a
                B -> b
            """,
            create_labeled_two_cycles_graph(3, 2, ("a", "b")),
            None,
            None,
            {
                (3, 4),
                (2, 5),
                (1, 0),
                (0, 4),
                (3, 5),
                (2, 0),
                (1, 4),
                (0, 5),
                (3, 0),
                (2, 4),
                (1, 5),
                (0, 0),
            },
        ),
        (
            """
                S -> A B
                S -> A C
                C -> S B
                A -> a
                B -> b
            """,
            create_labeled_two_cycles_graph(3, 2, ("a", "b")),
            {0},
            None,
            {
                (0, 4),
                (0, 5),
                (0, 0),
            },
        ),
    ],
)
def test_cfpq(cfg, graph, start_nodes, final_nodes, exp_ans):
    assert cfpq_hellings(graph, CFG.from_text(cfg), start_nodes, final_nodes) == exp_ans
    assert cfpq_matrix(graph, CFG.from_text(cfg), start_nodes, final_nodes) == exp_ans
