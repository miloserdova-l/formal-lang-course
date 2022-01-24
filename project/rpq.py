from networkx import Graph
from pyformlang.regular_expression import PythonRegex

from project import regex_to_min_dfa
from project.finite_automaton_utils import BoolFiniteAutomaton, Algo
from project.graph_utils import graph_to_nfa


def rpq(
    graph: Graph,
    request: PythonRegex,
    algo: Algo = Algo.SCIPY,
    start_nodes: set = None,
    final_nodes: set = None,
) -> set:
    new_g = BoolFiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes), algo)
    new_r = BoolFiniteAutomaton(regex_to_min_dfa(request), algo)
    intersection = new_g.get_intersection(new_r)
    tc = intersection.transitive_closure()
    if algo is Algo.SCIPY:
        x, y = tc.nonzero()
    else:
        x, y = tc.to_lists()
    ans = set()
    for (i, j) in zip(x, y):
        if i in intersection.start_states and j in intersection.final_states:
            ans.add(
                (
                    new_g.get_state_by_number(i // new_r.number_of_states),
                    new_g.get_state_by_number(j // new_r.number_of_states),
                )
            )
    return ans
