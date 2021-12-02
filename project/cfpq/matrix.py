from typing import Tuple

from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix

from project import cfg_to_normal_form


def matrix(cfg: CFG, graph: MultiDiGraph) -> set[Tuple[int, str, int]]:
    n = graph.number_of_nodes()
    if n == 0:
        return set()

    result = {}
    term_prods = set()
    nonterm_prods = set()

    if cfg.generate_epsilon():
        m = dok_matrix((n, n), dtype=bool)
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
                m = result.get(prod.head.value, dok_matrix((n, n), dtype=bool))
                m[u, v] = True
                result[prod.head.value] = m

    changing = True
    while changing:
        changing = False
        for p in nonterm_prods:
            m = result.get(p.head.value, dok_matrix((n, n), dtype=bool))
            old_nnz = m.nnz
            m += dok_matrix(
                result.get(p.body[0].value, dok_matrix((n, n), dtype=bool)).dot(
                    result.get(p.body[1].value, dok_matrix((n, n), dtype=bool))
                )
            )
            new_nnz = m.nnz
            result[p.head.value] = m
            changing = max(changing, old_nnz != new_nnz)

    triples = set()
    for key, m in result.items():
        for (u, v), _ in m.items():
            triples.add((u, key, v))

    return triples
