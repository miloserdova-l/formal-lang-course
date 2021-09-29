import pytest
from pyformlang.regular_expression import PythonRegex

from project import create_labeled_two_cycles_graph
from project.rpq import rpq


@pytest.fixture()
def graph():
    return create_labeled_two_cycles_graph(2, 3, ("a", "c"))


def test_rpq(graph):
    request = PythonRegex("a*c")
    ans = rpq(graph, request, start_nodes={1}, final_nodes={3})
    assert ans == {(1, 3)}

    request = PythonRegex("a*|c")
    ans = rpq(graph, request, start_nodes={4}, final_nodes={4, 5})
    assert ans == {(4, 5)}

    request = PythonRegex("ac*")
    ans = rpq(graph, request, start_nodes={2}, final_nodes={0, 3, 4, 5})
    assert ans == {(2, 0), (2, 3), (2, 4), (2, 5)}

    request = PythonRegex("a*b*c*")
    ans = rpq(graph, request, start_nodes={0, 1}, final_nodes={0, 3, 5})
    assert ans == {(0, 0), (0, 3), (0, 5), (1, 3), (1, 5), (1, 0)}
