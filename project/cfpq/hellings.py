from collections import deque

from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix

from project.cfg_utils import cfg_to_normal_form


def hellings(cfg: CFG, graph: MultiDiGraph) -> set:
    n = graph.number_of_nodes()
    if n == 0:
        return set()

    result = {}
    deq = deque()
    term_prods = set()
    nonterm_prods = set()

    if cfg.generate_epsilon():
        matrix = dok_matrix((n, n), dtype=bool)
        for i in range(n):
            matrix[i, i] = True
            deq.append((i, cfg.start_symbol.value, i))
        result[cfg.start_symbol.value] = matrix

    cfg = cfg_to_normal_form(cfg)

    for prod in cfg.productions:
        if len(prod.body) == 1:
            term_prods.add(prod)
        elif len(prod.body) == 2:
            nonterm_prods.add(prod)

    for u, v, edge_data in graph.edges(data=True):
        for prod in term_prods:
            if prod.body[0].value == edge_data["label"]:
                deq.append((u, prod.head.value, v))
                matrix = result.get(prod.head.value, dok_matrix((n, n), dtype=bool))
                matrix[u, v] = True
                result[prod.head.value] = matrix

    while deq:
        tmp = list()
        out, var, to = deq.popleft()

        for key, matrix in result.items():
            for (i, _), _ in matrix.getcol(out).todok().items():
                for prod in nonterm_prods:
                    if (
                        prod.body[0].value == key
                        and prod.body[1].value == var
                        and (
                            prod.head.value not in result
                            or result[prod.head.value][i, to] == False
                        )
                    ):
                        deq.append((i, prod.head.value, to))
                        tmp.append((i, prod.head.value, to))

        for out, var, to in tmp:
            matrix = result.get(var, dok_matrix((n, n), bool))
            matrix[out, to] = True
            result[var] = matrix
        tmp.clear()

        for key, matrix in result.items():
            for (_, new_to), _ in matrix.getrow(to).todok().items():
                for prod in nonterm_prods:
                    if (
                        prod.body[0].value == var
                        and prod.body[1].value == key
                        and (
                            prod.head.value not in result
                            or result[prod.head.value][out, new_to] == False
                        )
                    ):
                        deq.append((out, prod.head.value, new_to))
                        tmp.append((out, prod.head.value, new_to))

        for out, var, to in tmp:
            matrix = result.get(var, dok_matrix((n, n), bool))
            matrix[out, to] = True
            result[var] = matrix

    triples = set()
    for key, matrix in result.items():
        for (u, v), _ in matrix.items():
            triples.add((u, key, v))

    return triples
