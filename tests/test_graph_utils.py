import filecmp
import os

import cfpq_data
import networkx
import networkx.algorithms.isomorphism as iso
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol

from project import *

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

    exp_dfa = DeterministicFiniteAutomaton()
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    state3 = State(3)
    state4 = State(4)

    a = Symbol("a")
    b = Symbol("b")
    c = Symbol("c")
    d = Symbol("d")

    exp_dfa.add_start_state(state0)

    exp_dfa.add_final_state(state3)
    exp_dfa.add_final_state(state4)

    exp_dfa.add_transition(state0, a, state1)
    exp_dfa.add_transition(state1, b, state2)
    exp_dfa.add_transition(state2, c, state3)
    exp_dfa.add_transition(state0, d, state4)

    dfa = regex_to_min_dfa(regex)
    assert dfa.is_equivalent_to(exp_dfa)
    assert dfa.is_deterministic()
    assert dfa.is_equivalent_to(dfa.minimize())
