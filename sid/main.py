from typing import List
from .rule import Rule
from .linguistic_variable import LinguisticVar
import matplotlib.pyplot as plt


class SID:
    def __init__(self, rules: List[Rule], output_vars: list, agregation_method: str, dm: set):
        consequences = set()
        for r in rules:
            if r.consequence in consequences:
                raise Exception("duplicated consequence")
            consequences.add(r.consequence)
        self.rules = rules
        self.output_vars = output_vars
        self.output_joined = []
        self.agregation_method = agregation_method
        self.dm = dm

    def __call__(self, inp):
        for r in self.rules:
            r(inp, self.agregation_method)
        for ov in self.output_vars:
            jf = ov.join()
            for _dm in self.dm:
                jf.desdifusificate(_dm)
            self.output_joined.append(jf)

    def reset(self):
        self.output_joined = []

    def plot(self):
        for i in range(0, len(self.output_joined)):
            self.output_joined[i].plot()
            plt.title(self.output_vars[i].name)
            plt.show()
