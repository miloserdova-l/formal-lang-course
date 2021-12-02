from functools import reduce

from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import PythonRegex


def regex_to_min_dfa(regex: PythonRegex) -> DeterministicFiniteAutomaton:
    eps_nfa = regex.to_epsilon_nfa()
    return eps_nfa.minimize()


def get_regex(body: list) -> PythonRegex:
    return reduce(
        lambda f, s: f.union(s),
        [__get_concat(elem) for elem in body],
    )


def __get_concat(elem: list) -> PythonRegex:
    if len(elem) == 0:
        return PythonRegex("")
    return reduce(
        lambda x, y: x.concatenate(y), [PythonRegex(symbol.value) for symbol in elem]
    )
