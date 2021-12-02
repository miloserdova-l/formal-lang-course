from scipy.sparse import dok_matrix

from project.ecfg import ECFG
from project.regex_utils import get_regex

Box = dict


class RSM:
    def __init__(self, ecfg: ECFG):
        self.boxes = dict()
        for k, v in ecfg.productions.items():
            self.boxes[k] = get_regex(v).to_epsilon_nfa().to_deterministic()


class MatrixRSM(RSM):
    def __init__(self, ecfg: ECFG):
        super().__init__(ecfg)
        self.n = sum(len(body) + 1 for p in ecfg.productions.values() for body in p)
        self.m_boxes = dict()
        self.heads = dict()
        self.start_states = set()
        self.final_states = set()
        i = 0
        for head, body in ecfg.productions.items():
            for simple_production in body:
                self.start_states.add(i)
                self.final_states.add(i + len(simple_production))
                self.heads[(i, i + len(simple_production))] = head.value
                for b in simple_production:
                    m = self.m_boxes.get(
                        b.value, dok_matrix((self.n, self.n), dtype=bool)
                    )
                    m[i, i + 1] = True
                    self.m_boxes[b.value] = m
                    i += 1
                i += 1
