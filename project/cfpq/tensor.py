import sys
from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix, identity

from project.cfg_utils import cfg_to_ecfg
from project.finite_automaton_utils import BoolFiniteAutomaton, Algo
from project.graph_utils import graph_to_nfa
from project.rsm import MatrixRSM

if sys.platform == "linux":
    from pycubool import Matrix


def tensor(cfg: CFG, graph: MultiDiGraph, algo: Algo = Algo.SCIPY) -> set:
    ecfg = cfg_to_ecfg(cfg)
    nonterm = {p.value for p in ecfg.productions}
    m_rsm = MatrixRSM(ecfg, algo)
    g = BoolFiniteAutomaton(graph_to_nfa(graph), algo)

    for p in cfg.productions:
        if len(p.body) == 0:
            if algo is Algo.SCIPY:
                g.edges[p.head.value] = identity(g.number_of_states, dtype=bool).todok()
            else:
                id = Matrix.empty(shape=(g.number_of_states, g.number_of_states))
                for i in range(g.number_of_states):
                    id[i, i] = True
                g.edges[p.head.value] = id

    bfa = BoolFiniteAutomaton.create_bfa(
        m_rsm.m_boxes, m_rsm.start_states, m_rsm.final_states, algo
    )
    bfa.number_of_states = m_rsm.n
    prev_nnz = -2
    new_nnz = -1
    while prev_nnz != new_nnz:
        tc = bfa.get_intersection(g).transitive_closure()
        prev_nnz, new_nnz = new_nnz, tc.nnz if algo is Algo.SCIPY else tc.nvals
        x, y = tc.nonzero() if algo is Algo.SCIPY else tc.to_lists()
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
                dok_matrix((g.number_of_states, g.number_of_states), dtype=bool)
                if algo is Algo.SCIPY
                else Matrix.empty(shape=(g.number_of_states, g.number_of_states)),
            )
            m[graph_from, graph_to] = True
            g.edges[variable] = m

    if algo is Algo.SCIPY:
        triples = {
            (u, key, v)
            for key, m in g.edges.items()
            if key in nonterm
            for (u, v) in m.keys()
        }
    else:
        triples = {
            (u, key, v)
            for key, m in g.edges.items()
            if key in nonterm
            for (u, v) in zip(*m.to_lists())
        }
    return triples
