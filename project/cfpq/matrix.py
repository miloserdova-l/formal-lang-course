import sys
from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix

from project import cfg_to_normal_form
from project.finite_automaton_utils import Algo

if sys.platform == "linux":
    from pycubool import Matrix


def matrix(cfg: CFG, graph: MultiDiGraph, algo: Algo = Algo.SCIPY) -> set:
    n = graph.number_of_nodes()
    if n == 0:
        return set()

    result = {}
    term_prods = set()
    nonterm_prods = set()

    if cfg.generate_epsilon():
        if algo is Algo.SCIPY:
            m = dok_matrix((n, n), dtype=bool)
        else:
            m = Matrix.empty(shape=(n, n))
        for i in range(n):
            m[i, i] = True
        result[cfg.start_symbol.value] = m

    cfg = cfg_to_normal_form(cfg)

    for prod in cfg.productions:
        if len(prod.body) == 1:
            term_prods.add(prod)
        elif len(prod.body) == 2:
            nonterm_prods.add(prod)

    for u, v, edge_data in graph.edges(data=True):
        for prod in term_prods:
            if prod.body[0].value == edge_data["label"]:
                m = result.get(
                    prod.head.value,
                    dok_matrix((n, n), dtype=bool)
                    if algo is Algo.SCIPY
                    else Matrix.empty(shape=(n, n)),
                )
                m[u, v] = True
                result[prod.head.value] = m

    changing = True
    while changing:
        changing = False
        for p in nonterm_prods:
            m = result.get(p.head.value, dok_matrix((n, n), dtype=bool))
            old_nnz = m.nnz
            m += dok_matrix(
                result.get(
                    p.body[0].value,
                    dok_matrix((n, n), dtype=bool)
                    if algo is Algo.SCIPY
                    else Matrix.empty(shape=(n, n)),
                ).dot(
                    result.get(
                        p.body[1].value,
                        dok_matrix((n, n), dtype=bool)
                        if algo is Algo.SCIPY
                        else Matrix.empty(shape=(n, n)),
                    )
                )
            )
            new_nnz = m.nnz if algo is Algo.SCIPY else m.nvals
            result[p.head.value] = m
            changing = max(changing, old_nnz != new_nnz)

    if algo is Algo.SCIPY:
        triples = {
            (u, variable, v) for variable, m in result.items() for u, v in m.keys()
        }
    else:
        triples = {
            (u, variable, v) for variable, m in result.items() for u, v in m.to_list()
        }

    return triples
