import os
import filecmp
import cfpq_data
import networkx
import networkx.algorithms.isomorphism as iso
from project import *
from pyformlang.regular_expression import PythonRegex

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_graph_info():
    g = cfpq_data.labeled_two_cycles_graph(
        42, 29, edge_labels=("c", "d"), verbose=False
    )
    assert get_info(g) == GraphInfo(72, 73, {"c", "d"})

    g = cfpq_data.labeled_cycle_graph(5, edge_label="a")
    assert get_info(g) == GraphInfo(5, 5, {"a"})


def test_create_labeled_two_cycles_graph():
    expected_graph = cfpq_data.labeled_two_cycles_graph(
        42, 29, edge_labels=("c", "d"), verbose=False
    )
    my_graph = create_labeled_two_cycles_graph(42, 29, edge_labels=("c", "d"))
    em = iso.categorical_multiedge_match("label", None)
    assert networkx.is_isomorphic(my_graph, expected_graph, edge_match=em)

    not_expected_graph = cfpq_data.labeled_two_cycles_graph(
        42, 29, edge_labels=("d", "c"), verbose=False
    )
    assert not networkx.is_isomorphic(my_graph, not_expected_graph, edge_match=em)


def test_save_graph_to_file():
    g = create_labeled_two_cycles_graph(42, 29, edge_labels=("c", "d"))
    save_graph_to_file(g, os.sep.join([root_path, "output", "my-graph"]))
    assert filecmp.cmp(
        os.sep.join([root_path, "output", "my-graph"]),
        os.sep.join([root_path, "output", "exp-graph"]),
    )


def test_regex_to_min_dfa():
    regex = "abc|d"
    dfa = regex_to_min_dfa(regex)
    assert dfa.is_equivalent_to(PythonRegex(regex).to_epsilon_nfa())
    assert dfa.is_deterministic()
    assert dfa.is_equivalent_to(dfa.minimize())
