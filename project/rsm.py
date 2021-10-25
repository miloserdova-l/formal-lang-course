from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

Box = dict[Variable, DeterministicFiniteAutomaton]


class RecursiveStateMachine:
    def __init__(self):
        self.start_symbol = None
        self.boxes = Box()

    def minimize(self) -> None:
        for var in self.boxes.keys():
            self.boxes.get(var).minimize()
