from typing import Tuple

from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix, identity

from project.cfg_utils import cfg_to_ecfg
from project.finite_automaton_utils import BoolFiniteAutomaton
from project.graph_utils import graph_to_nfa
from project.rsm import MatrixRSM


def tensor(cfg: CFG, graph: MultiDiGraph) -> set[Tuple[int, str, int]]:
    ecfg = cfg_to_ecfg(cfg)
    nonterm = set()
    for p in ecfg.productions:
        nonterm.add(p.value)
    ecfg = cfg_to_ecfg(cfg)
    m_rsm = MatrixRSM(ecfg)
    g = BoolFiniteAutomaton(graph_to_nfa(graph))

    # Add loops
    for p in cfg.productions:
        if len(p.body) == 0:
            g.edges[p.head.value] = identity(g.number_of_states, dtype=bool).todok()

    changing = True
    bfa = BoolFiniteAutomaton.create_bfa(
        m_rsm.m_boxes, m_rsm.start_states, m_rsm.final_states
    )
    bfa.number_of_states = m_rsm.n
    prev_nnz = -2
    new_nnz = -1
    while prev_nnz != new_nnz:
        tc = bfa.get_intersection(g).transitive_closure()
        prev_nnz, new_nnz = new_nnz, tc.nnz
        x, y = tc.nonzero()
        for (i, j) in zip(x, y):
            rfa_from = i // g.number_of_states
            rfa_to = j // g.number_of_states
            graph_from = i % g.number_of_states
            graph_to = j % g.number_of_states

            if (rfa_from, rfa_to) not in m_rsm.heads:
                continue

            variable = m_rsm.heads[(rfa_from, rfa_to)]
            m = g.edges.get(
                variable,
                dok_matrix((g.number_of_states, g.number_of_states), dtype=bool),
            )
            m[graph_from, graph_to] = True
            g.edges[variable] = m

    triples = {
        (u, key, v)
        for key, m in g.edges.items()
        if key in nonterm
        for (u, v) in m.keys()
    }
    return triples
