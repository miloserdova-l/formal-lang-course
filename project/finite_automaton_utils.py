import sys

from pyformlang.finite_automaton import (
    FiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from scipy.sparse import kron, dok_matrix, bsr_matrix


class BoolFiniteAutomaton:
    def __init__(self, fa: FiniteAutomaton):
        self.fa = fa
        self.number_of_states = len(fa.states)
        self.edges = dict()
        self.__number_of_state = dict()
        self.__state_by_number = dict()
        for i, state in enumerate(self.fa.states):
            self.__number_of_state[state] = i
            self.__state_by_number[i] = state

        edges = fa.to_dict()

        for u in edges.keys():
            i = self.__number_of_state.get(u)
            for label in edges.get(u).keys():
                if not isinstance(edges.get(u).get(label), set):
                    edges.get(u)[label] = {edges.get(u).get(label)}
                for v in edges.get(u).get(label):
                    j = self.__number_of_state.get(v)
                    if label not in self.edges.keys():
                        self.edges[label] = dok_matrix(
                            (self.number_of_states, self.number_of_states), dtype=bool
                        )
                    self.edges[label][i, j] = True

    def get_intersection(self, other):
        if not isinstance(other, BoolFiniteAutomaton):
            print("Illegal argument error: argument type mismatch", file=sys.stderr)
            exit(1)
        labels = self.fa.symbols.intersection(other.fa.symbols)
        intersection = dict()
        for label in labels:
            intersection[label] = kron(self.edges[label], other.edges[label])
        start_states = set()
        final_states = set()
        for u in self.fa.start_states:
            for v in other.fa.start_states:
                start_states.add(
                    self.__number_of_state.get(u) * other.number_of_states
                    + other.__number_of_state.get(v)
                )
        for u in self.fa.final_states:
            for v in other.fa.final_states:
                final_states.add(
                    self.__number_of_state.get(u) * other.number_of_states
                    + other.__number_of_state.get(v)
                )
        return BoolFiniteAutomaton.__create_bfa_from_matrix(
            intersection, start_states, final_states
        )

    def transitive_closure(self) -> bsr_matrix:
        res_m = sum(self.edges.values())
        while True:
            old = res_m
            res_m += res_m.dot(res_m)
            if res_m.nnz == old.nnz:
                break
        return res_m

    def get_state_by_number(self, n: int):
        return self.__state_by_number.get(n)

    @staticmethod
    def __create_bfa_from_matrix(m: dict, start_states: set, final_states: set):
        fa = NondeterministicFiniteAutomaton()
        for label in m.keys():
            edges = zip(m[label].row, m[label].col)
            for (u, v) in edges:
                fa.add_transition(u, label, v)
        for v in start_states:
            fa.add_start_state(v)
        for v in final_states:
            fa.add_final_state(v)
        return BoolFiniteAutomaton(fa)
