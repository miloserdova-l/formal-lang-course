import sys

from pyformlang.finite_automaton import FiniteAutomaton, State, Symbol
from scipy.sparse import kron, dok_matrix, bsr_matrix


class Automaton:
    def __init__(self, fa: FiniteAutomaton):
        self.fa = fa
        self.number_of_states = len(fa.states)
        self.edges = dict()
        self.state_by_number = dict()

        edges = fa.to_dict()
        self.__node_number = dict()

        for u in edges.keys():
            i = self.__get_node_number(u)
            for label in edges.get(u).keys():
                if not isinstance(edges.get(u).get(label), set):
                    edges.get(u)[label] = {edges.get(u).get(label)}
                for v in edges.get(u).get(label):
                    j = self.__get_node_number(v)
                    if label not in self.edges.keys():
                        self.edges[label] = dok_matrix(
                            (self.number_of_states, self.number_of_states), dtype=bool
                        )
                    self.edges[label][i, j] = True

    def __get_node_number(self, x: State) -> int:
        if x not in self.__node_number.keys():
            self.state_by_number[len(self.__node_number)] = x
            self.__node_number[x] = len(self.__node_number)
        return self.__node_number.get(x)

    def get_edges_by_label(self, label: Symbol):
        return self.edges[label]

    def get_state_by_node(self, node: int) -> State:
        return self.state_by_number.get(node)

    def get_intersection(self, other) -> bsr_matrix:
        if not isinstance(other, Automaton):
            print("Illegal argument error: argument type mismatch", file=sys.stderr)
            exit(1)
        labels = self.fa.symbols.intersection(other.fa.symbols)
        size = self.number_of_states * other.number_of_states
        intersection = bsr_matrix((size, size), dtype=bool)
        for label in labels:
            intersection += kron(
                self.get_edges_by_label(label), other.get_edges_by_label(label)
            )
        return intersection
