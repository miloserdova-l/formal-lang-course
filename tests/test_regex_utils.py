import pytest
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol
from pyformlang.regular_expression import PythonRegex

from project import regex_to_min_dfa


@pytest.fixture()
def dfa():
    regex = PythonRegex("ab*c|d")
    return regex_to_min_dfa(regex)


def test_is_deterministic(dfa):
    assert dfa.is_deterministic()


def test_is_minimal(dfa):
    assert len(dfa.states) == 3


def test_equivalence(dfa):
    exp_dfa = DeterministicFiniteAutomaton()

    state0 = State(0)
    state1 = State(1)
    state2 = State(2)

    exp_dfa.add_start_state(state0)
    exp_dfa.add_final_state(state2)

    exp_dfa.add_transition(state0, Symbol("a"), state1)
    exp_dfa.add_transition(state1, Symbol("b"), state1)
    exp_dfa.add_transition(state1, Symbol("c"), state2)
    exp_dfa.add_transition(state0, Symbol("d"), state2)

    assert dfa.is_equivalent_to(exp_dfa)
