from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable

from project.cfpq.hellings import hellings
from project.cfpq.matrix import matrix
from project.cfpq.tensor import tensor
from project.finite_automaton_utils import Algo


def __cfpq(
    algo: set,
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: set = None,
    final_nodes: set = None,
) -> set:
    if not start_nodes:
        start_nodes = graph.nodes
    if not final_nodes:
        final_nodes = graph.nodes
    result = set()
    for u, h, v in algo:
        if h == cfg.start_symbol.value and u in start_nodes and v in final_nodes:
            result.add((u, v))
    return result


def cfpq_matrix(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: set = None,
    final_nodes: set = None,
    start: Variable = Variable("S"),
    algo: Algo = Algo.SCIPY,
) -> set:
    cfg._start_symbol = start
    return __cfpq(matrix(cfg, graph, algo), graph, cfg, start_nodes, final_nodes)


def cfpq_hellings(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: set = None,
    final_nodes: set = None,
    start: Variable = Variable("S"),
) -> set:
    cfg._start_symbol = start
    return __cfpq(hellings(cfg, graph), graph, cfg, start_nodes, final_nodes)


def cfpq_tensor(
    graph: MultiDiGraph,
    cfg: CFG,
    start_nodes: set = None,
    final_nodes: set = None,
    start: Variable = Variable("S"),
    algo: Algo = Algo.SCIPY,
) -> set:
    cfg._start_symbol = start
    return __cfpq(tensor(cfg, graph, algo), graph, cfg, start_nodes, final_nodes)
