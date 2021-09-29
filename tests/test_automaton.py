from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    State,
)

from project.finite_automaton_utils import BoolFiniteAutomaton


def test_intersection():
    first = NondeterministicFiniteAutomaton()
    first.add_transitions([(0, "b", 1), (1, "c", 1), (1, "b", 2), (0, "a", 2)])
    first.add_start_state(State(0))
    first.add_final_state(State(1))
    first.add_final_state(State(2))
    """
    { } {b} {a}
    { } {c} {b}
    { } { } { }
    """
    second = DeterministicFiniteAutomaton()
    second.add_transitions([(0, "b", 1), (1, "c", 2), (2, "b", 3)])
    second.add_start_state(State(0))
    second.add_final_state(State(3))
    """
    { } {b} { } { }
    { } { } {c} { }
    { } { } { } {b}
    { } { } { } { }
    """
    exp = NondeterministicFiniteAutomaton()
    exp.add_transitions(
        [(0, "b", 5), (2, "b", 7), (4, "b", 9), (5, "c", 6), (6, "b", 11)]
    )
    exp.add_start_state(State(0))
    exp.add_final_state(State(7))
    exp.add_final_state(State(11))
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
    assert (
        BoolFiniteAutomaton(first)
        .get_intersection(BoolFiniteAutomaton(second))
        .fa.is_equivalent_to(exp)
    )
