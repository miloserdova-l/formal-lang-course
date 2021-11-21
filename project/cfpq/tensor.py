from typing import Tuple

from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix, identity

from project.finite_automaton_utils import BoolFiniteAutomaton
from project.graph_utils import graph_to_nfa


def tensor(cfg: CFG, graph: MultiDiGraph) -> set[Tuple[int, str, int]]:
    # Build boxes of RSM
    n = sum(len(p.body) + 1 for p in cfg.productions)
    rsm_heads = dict()
    nonterm = set()
    boxes = dict()
    start_states = set()
    final_states = set()
    i = 0
    for p in cfg.productions:
        nonterm.add(p.head.value)
        start_states.add(i)
        final_states.add(i + len(p.body))
        rsm_heads[(i, i + len(p.body))] = p.head.value
        for b in p.body:
            m = boxes.get(b.value, dok_matrix((n, n), dtype=bool))
            m[i, i + 1] = True
            boxes[b.value] = m
            i += 1
        i += 1

    # Build BFA for graph
    g = BoolFiniteAutomaton(graph_to_nfa(graph))

    # Add loops
    for p in cfg.productions:
        if len(p.body) == 0:
            g.edges[p.head.value] = identity(g.number_of_states, dtype=bool).todok()

    changing = True
    bfa = BoolFiniteAutomaton.create_bfa(boxes, start_states, final_states)
    bfa.number_of_states = n
    while changing:
        changing = False
        tc = bfa.get_intersection(g).transitive_closure()
        x, y = tc.nonzero()
        for (i, j) in zip(x, y):
            rfa_from = i // g.number_of_states
            rfa_to = j // g.number_of_states
            graph_from = i % g.number_of_states
            graph_to = j % g.number_of_states

            if (rfa_from, rfa_to) not in rsm_heads:
                continue

            variable = rsm_heads[(rfa_from, rfa_to)]
            m = g.edges.get(
                variable,
                dok_matrix((g.number_of_states, g.number_of_states), dtype=bool),
            )
            if not m[graph_from, graph_to]:
                changing = True
                m[graph_from, graph_to] = True
                g.edges[variable] = m

    triples = set()
    for key, m in g.edges.items():
        if key not in nonterm:
            continue
        for (u, v), _ in m.items():
            triples.add((u, key, v))

    return triples
