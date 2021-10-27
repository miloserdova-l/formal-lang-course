from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

Box = dict[Variable, DeterministicFiniteAutomaton]


class RSM:
    def __init__(self, start_symbol: Variable = None, boxes: Box = None):
        self.start_symbol = start_symbol
        self.boxes = boxes if boxes else Box()
