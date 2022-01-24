import pytest, sys
from pyformlang.regular_expression import PythonRegex

from project import create_labeled_two_cycles_graph
from project.finite_automaton_utils import Algo
from project.rpq import rpq


@pytest.fixture()
def graph():
    return create_labeled_two_cycles_graph(2, 3, ("a", "c"))


@pytest.mark.parametrize(
    "pattern,start_states,final_states,expected",
    [
        ("a*c", {1}, {3}, {(1, 3)}),
        ("a*|c", {4}, {4, 5}, {(4, 5)}),
        ("ac*", {2}, {0, 3, 4, 5}, {(2, 0), (2, 3), (2, 4), (2, 5)}),
        ("a*b*c*", {0, 1}, {0, 3, 5}, {(0, 0), (0, 3), (0, 5), (1, 3), (1, 5), (1, 0)}),
    ],
)
def test_rpq(graph, pattern, start_states, final_states, expected):
    request = PythonRegex(pattern)
    ans = rpq(graph, request, start_nodes=start_states, final_nodes=final_states)
    assert ans == expected
    if sys.platform == "linux":
        ans = rpq(
            graph,
            request,
            algo=Algo.PYCUBOOL,
            start_nodes=start_states,
            final_nodes=final_states,
        )
        assert ans == expected
