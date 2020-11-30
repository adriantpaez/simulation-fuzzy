from .functions import Membership, MembershipCombined
from typing import *
import matplotlib.pyplot as plt


class LinguisticValue:
    def __init__(self, var_name: str, name: str, memb_func: Membership):
        self.name = name
        self.memb_func = memb_func
        self.memb_func.value_name = name
        self.var_name = var_name

    def __call__(self, inp: dict) -> float:
        return self.memb_func[inp[self.var_name]]


class LinguisticVar:
    def __init__(self, name: str, values: List[LinguisticValue]):
        self.name = name
        self.values = values

    def plot(self):
        for v in self.values:
            v.memb_func.plot()
        plt.title(self.name)
        plt.legend()
        plt.show()

    def join(self) -> MembershipCombined:
        if self.values:
            resp = self.values[0].memb_func
            for i in range(1, len(self.values)):
                resp += self.values[i].memb_func
            return resp
