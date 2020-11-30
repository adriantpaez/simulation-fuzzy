from .fuzzy_expression import *
from .linguistic_variable import *
import matplotlib.pyplot as plt


class Rule:
    def __init__(self, condition: Expression, consequence: LinguisticValue):
        super().__init__()
        self.condition = condition
        self.consequence = consequence

    def __call__(self, inp, agregation_method):
        top = self.condition(inp)
        self.consequence.memb_func.top = top
        self.consequence.memb_func.agregation_method = agregation_method
