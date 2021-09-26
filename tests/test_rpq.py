from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from pyformlang.regular_expression import PythonRegex
from project import regex_to_min_dfa
from project.rpq import rpq, get_intersection


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
    assert get_intersection(first, second)[0].todense().tolist() == exp


def test_rpq():
    graph = DeterministicFiniteAutomaton()
    graph.add_transitions([(0, "a", 1), (1, "a", 2), (2, "c", 3)])
    graph.add_start_state(0)
    graph.add_final_state(3)
    request = regex_to_min_dfa(PythonRegex("a*c"))
    ans = rpq(graph, request)
    assert ans == {(0, 3)}
