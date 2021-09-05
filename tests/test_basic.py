import os
import filecmp
import cfpq_data
import networkx
import networkx.algorithms.isomorphism as iso
from project import *


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
    save_graph_to_file(g, os.sep.join(["..", "output", "my-graph"]))
    assert filecmp.cmp(
        os.sep.join(["..", "output", "my-graph"]),
        os.sep.join(["..", "output", "exp-graph"]),
    )
