from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from pyformlang.regular_expression import PythonRegex
from project import regex_to_min_dfa
from project.rpq import rpq
from project.finite_automaton_utils import Automaton


def test_intersection():
    first = NondeterministicFiniteAutomaton()
    first.add_transitions([(0, "b", 1), (1, "c", 1), (1, "b", 2), (0, "a", 2)])
    """
    { } {b} {a}
    { } {c} {b}
    { } { } { }
    """
    second = DeterministicFiniteAutomaton()
    second.add_transitions([(0, "b", 1), (1, "c", 2), (2, "b", 3)])
    """
    { } {b} { } { }
    { } { } {c} { }
    { } { } { } {b}
    { } { } { } { }
    """
    exp = [[False for _ in range(12)] for _ in range(12)]
    """
    { } { } { } { }|{ } {b} { } { }|{ } { } { } { }
    { } { } { } { }|{ } { } { } { }|{ } { } { } { }
    { } { } { } { }|{ } { } { } {b}|{ } { } { } { }
    { } { } { } { }|{ } { } { } { }|{ } { } { } { }
    { } { } { } { } { } { } { } { } { } {b} { } { }
    { } { } { } { } { } { } {c} { } { } { } { } { }
    { } { } { } { } { } { } { } { } { } { } { } {b}
    { } { } { } { } { } { } { } { } { } { } { } { }
    { } { } { } { }|{ } { } { } { }|{ } { } { } { }
    { } { } { } { }|{ } { } { } { }|{ } { } { } { }
    { } { } { } { }|{ } { } { } { }|{ } { } { } { }
    { } { } { } { }|{ } { } { } { }|{ } { } { } { }
    """
    exp[0][5] = True
    exp[2][7] = True
    exp[4][9] = True
    exp[5][6] = True
    exp[6][11] = True
    assert (
        Automaton(first).get_intersection(Automaton(second)).todense().tolist() == exp
    )


def test_rpq():
    graph = DeterministicFiniteAutomaton()
    graph.add_transitions([(1, "a", 2), (2, "a", 3), (3, "c", 4)])
    graph.add_start_state(State(1))
    graph.add_final_state(State(4))
    request = regex_to_min_dfa(PythonRegex("a*c"))
    ans = rpq(graph, request)
    assert ans == {(1, 4)}
