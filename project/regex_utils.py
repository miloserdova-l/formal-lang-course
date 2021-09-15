from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import PythonRegex


def regex_to_min_dfa(regex: PythonRegex) -> DeterministicFiniteAutomaton:
    eps_nfa = regex.to_epsilon_nfa()
    return eps_nfa.minimize()
