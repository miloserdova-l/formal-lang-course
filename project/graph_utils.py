from dataclasses import dataclass
import networkx
from typing import Tuple
from networkx import MultiDiGraph
import cfpq_data
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.regular_expression import PythonRegex


@dataclass
class GraphInfo:
    def __init__(self, number_of_nodes: int, number_of_edges: int, labels: set):
        self.number_of_nodes = number_of_nodes
        self.number_of_edges = number_of_edges
        self.labels = labels

    def __repr__(self):
        return "Number of nodes: {}\nNumber of edges: {}\nLabels: {}".format(
            self.number_of_nodes, self.number_of_edges, self.labels
        )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.number_of_nodes == other.number_of_nodes
                and self.number_of_edges == other.number_of_edges
                and self.labels == other.labels
            )
        else:
            return False


def get_info(graph: MultiDiGraph) -> GraphInfo:
    return GraphInfo(
        graph.number_of_nodes(), graph.number_of_edges(), cfpq_data.get_labels(graph)
    )


def create_labeled_two_cycles_graph(
    size_of_first_cycle: int, size_of_second_cycle: int, edge_labels: Tuple[str, str]
) -> MultiDiGraph:
    return cfpq_data.labeled_two_cycles_graph(
        size_of_first_cycle,
        size_of_second_cycle,
        edge_labels=edge_labels,
        verbose=False,
    )


def regex_to_min_dfa(regex: PythonRegex or str) -> DeterministicFiniteAutomaton:
    if isinstance(regex, str):
        regex = PythonRegex(regex)
    eps_nfa = regex.to_epsilon_nfa()
    return eps_nfa.minimize()


def save_graph_to_file(graph: MultiDiGraph, file: str) -> None:
    networkx.drawing.nx_pydot.write_dot(graph, file)
