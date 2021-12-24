import sys
from enum import Enum

from pyformlang.finite_automaton import FiniteAutomaton
from scipy.sparse import kron, dok_matrix, bsr_matrix


class Algo(Enum):
    SCIPY = 1
    PYCUBOOL = 2


class BoolFiniteAutomaton:
    def __init__(self, fa: FiniteAutomaton, algo: Algo = Algo.SCIPY):
        if algo is Algo.PYCUBOOL:
            from pycubool import Matrix
        self.start_states = fa.start_states
        self.final_states = fa.final_states
        self.number_of_states = len(fa.states)
        self.edges = dict()
        self.algo = algo
        self.__number_of_state = dict()
        self.__state_by_number = dict()
        for i, state in enumerate(fa.states):
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
                        if self.algo is Algo.SCIPY:
                            self.edges[label] = dok_matrix(
                                (self.number_of_states, self.number_of_states),
                                dtype=bool,
                            )
                        else:
                            self.edges[label] = Matrix.empty(
                                shape=(self.number_of_states, self.number_of_states)
                            )
                    self.edges[label][i, j] = True

    def get_intersection(self, other):
        if not isinstance(other, BoolFiniteAutomaton) or other.algo != self.algo:
            print("Illegal argument error: argument type mismatch", file=sys.stderr)
            exit(1)
        labels = set(self.edges.keys()).intersection(set(other.edges.keys()))
        intersection = dict()
        for label in labels:
            if self.algo is Algo.SCIPY:
                intersection[label] = kron(self.edges[label], other.edges[label])
            else:
                intersection[label] = self.edges[label].kronecker(other.edges[label])
        start_states = set()
        final_states = set()
        for u in self.start_states:
            for v in other.start_states:
                start_states.add(
                    self.get_number_of_state(u) * other.number_of_states
                    + other.get_number_of_state(v)
                )
        for u in self.final_states:
            for v in other.final_states:
                final_states.add(
                    self.get_number_of_state(u) * other.number_of_states
                    + other.get_number_of_state(v)
                )
        return self.create_bfa(intersection, start_states, final_states, self.algo)

    def transitive_closure(self) -> bsr_matrix:
        if len(self.edges) == 0:
            return bsr_matrix((1, 1), dtype=bool)
        if self.algo is Algo.SCIPY:
            res_m = sum(self.edges.values())
        else:
            from pycubool import Matrix

            n = self.edges.get(next(iter(self.edges.keys()))).shape[0]
            res_m = Matrix.empty(shape=(n, n))
            for bm in self.edges.values():
                res_m.ewiseadd(bm, out=res_m)
        while True:
            old = res_m.copy()
            if self.algo is Algo.SCIPY:
                res_m += res_m.dot(res_m)
                if res_m.nnz == old.nnz:
                    break
            else:
                res_m.mxm(res_m, out=res_m, accumulate=True)
                if res_m.nvals == old.nvals:
                    break
        return res_m

    def get_state_by_number(self, n: int):
        if n in self.__state_by_number.keys():
            return self.__state_by_number.get(n)
        return n

    def get_number_of_state(self, n):
        if n in self.__number_of_state.keys():
            return self.__number_of_state.get(n)
        return n

    @classmethod
    def create_bfa(
        cls, edges: dict, start_states: set, final_states: set, algo: Algo = Algo.SCIPY
    ):
        bfa = cls.__new__(cls)
        super(BoolFiniteAutomaton, bfa).__init__()
        bfa.edges = edges
        bfa.start_states = start_states
        bfa.final_states = final_states
        bfa.algo = algo
        bfa.__state_by_number = dict()
        bfa.__number_of_state = dict()
        return bfa
