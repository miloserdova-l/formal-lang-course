from pyformlang.finite_automaton import FiniteAutomaton
from scipy.sparse import bsr_matrix
from project.finite_automaton_utils import Automaton


def transitive_closure(m: bsr_matrix) -> bsr_matrix:
    while True:
        old = m.todense().tolist()
        m += m.dot(m)
        new = m.todense().tolist()
        if new == old:
            break
    return m


def rpq(g: FiniteAutomaton, r: FiniteAutomaton) -> set:
    new_g = Automaton(g)
    new_r = Automaton(r)
    intersection = new_g.get_intersection(new_r)
    tc = transitive_closure(intersection)
    x, y = tc.nonzero()
    ans = set()
    for (i, j) in zip(x, y):
        a = i // new_r.number_of_states
        b = j // new_r.number_of_states
        if (
            new_g.get_state_by_node(a) in g.start_states
            and new_g.get_state_by_node(b) in g.final_states
            and new_r.get_state_by_node(i % new_r.number_of_states) in r.start_states
            and new_r.get_state_by_node(j % new_r.number_of_states) in r.final_states
        ):
            ans.add((new_g.get_state_by_node(a), new_g.get_state_by_node(b)))
    return ans
