import filecmp
import os
import cfpq_data
import networkx
import networkx.algorithms.isomorphism as iso
import pytest
from project import *
from project.graph_utils import graph_to_nfa
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton


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
    save_graph_to_file(g, os.sep.join([root_path, "tests", "resources", "my-graph"]))
    assert filecmp.cmp(
        os.sep.join([root_path, "tests", "resources", "my-graph"]),
        os.sep.join([root_path, "tests", "resources", "exp-graph"]),
    )


@pytest.fixture()
def two_cycles_graph():
    return create_labeled_two_cycles_graph(1, 3, ("q", "w"))


def test_graph_to_nfa_is_nondeterministic(two_cycles_graph):
    nfa = graph_to_nfa(two_cycles_graph)
    assert not nfa.is_deterministic()


def exp_nfa_base():
    exp_nfa = NondeterministicFiniteAutomaton()

    states = [State(i) for i in range(5)]
    q = Symbol("q")
    w = Symbol("w")

    exp_nfa.add_transition(states[0], q, states[1])
    exp_nfa.add_transition(states[1], q, states[0])
    exp_nfa.add_transition(states[0], w, states[2])
    exp_nfa.add_transition(states[2], w, states[3])
    exp_nfa.add_transition(states[3], w, states[4])
    exp_nfa.add_transition(states[4], w, states[0])

    return exp_nfa


def exp_nfa_with_fixed_states():
    exp_nfa = exp_nfa_base()
    exp_nfa.add_start_state(State(0))
    exp_nfa.add_final_state(State(3))
    exp_nfa.add_final_state(State(4))
    return exp_nfa


def exp_nfa_without_fixed_states():
    exp_nfa = exp_nfa_base()
    for i in range(5):
        exp_nfa.add_start_state(State(i))
        exp_nfa.add_final_state(State(i))
    return exp_nfa


def test_graph_to_nfa_equivalence(two_cycles_graph):
    exp_nfa = exp_nfa_without_fixed_states()
    nfa = graph_to_nfa(two_cycles_graph)
    assert nfa.is_equivalent_to(exp_nfa)

    exp_nfa = exp_nfa_with_fixed_states()
    nfa = graph_to_nfa(two_cycles_graph, start_nodes={0}, final_nodes={3, 4})
    assert nfa.is_equivalent_to(exp_nfa)
