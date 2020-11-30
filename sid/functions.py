import matplotlib.pyplot as plt
import math
from typing import *
from .methods import *

colors = ['m', 'b', 'g', 'y', 'r', 'k']


class Membership:

    def __init__(self, dom: tuple):
        if len(dom) != 2 or dom[0] > dom[1]:
            raise Exception("invalid dom")
        self.dom = dom
        self.value_name = ""
        self.top = 1.0
        self.agregation_method = "mamdani"
        self.points = []

    def __evaluate__(self, x) -> float:
        raise NotImplementedError()

    def __getitem__(self, key) -> float:
        if self.agregation_method == "mamdani":
            return min(self.top, self.__evaluate__(key))
        if self.agregation_method == "larsen":
            return self.__evaluate__(key) * self.top

    def __add__(self, other):
        if isinstance(self, MembershipCombined):
            if isinstance(other, MembershipCombined):
                return MembershipCombined(self.dom, self.funcs + other.funcs)
            self.funcs.append(other)
            return self
        return MembershipCombined(self.dom, [self, other])

    def desdifusificate(self, method):
        x = None
        if method == DM_CENTROID:
            x = self.__centroid__()
            self.points.append(
                (x, self[x], "centroide: " + str(round(x, 2)), colors[0]))
        elif method == DM_BISECCION:
            x = self.__biseccion__()
            self.points.append(
                (x, self[x], "biseccion: " + str(round(x, 2)), colors[1]))
        elif method == DM_FIRSTMAX:
            x = self.__first_max__()
            self.points.append(
                (x, self[x], "first max: " + str(round(x, 2)), colors[2]))
        elif method == DM_LASTMAX:
            x = self.__last_max__()
            self.points.append(
                (x, self[x], "last max: " + str(round(x, 2)), colors[3]))
        elif method == DM_AVEMAX:
            x = self.__ave_max__()
            self.points.append(
                (x, self[x], "ave max: " + str(round(x, 2)), colors[4]))
        else:
            raise Exception("invalid desdifusification mthod")
        return x

    def __centroid__(self):
        interval = (self.dom[1] - self.dom[0]) / 5000
        xfx = 0
        fx = 0
        i = self.dom[0]
        while i < self.dom[1]:
            y = self[i]
            xfx += i * y
            fx += y
            i += interval
        xfx += self.dom[1] * self[self.dom[1]]
        fx += self.dom[1]
        self._centroid = xfx / fx
        return self._centroid

    def __biseccion__(self):
        interval = (self.dom[1] - self.dom[0]) / 5000
        a = self.dom[0] + interval
        a_acum = 0
        b = self.dom[1] - interval
        b_acum = 0
        while a < b:
            if a_acum <= b_acum:
                a_acum += interval * self[a]
                a += interval
            else:
                b_acum += interval * self[b]
                b -= interval
        return (b + a) / 2

    def __first_max__(self):
        interval = (self.dom[1] - self.dom[0]) / 5000
        fm = 0
        x = self.dom[0]
        while x < self.dom[1]:
            y = self[x]
            if y <= fm and y != 0:
                return x
            fm = y
            x += interval
        if self[self.dom[1]] > fm:
            return self.dom[1]
        return x

    def __last_max__(self):
        interval = (self.dom[1] - self.dom[0]) / 5000
        fm = 0
        x = self.dom[1]
        while x > self.dom[0]:
            y = self[x]
            if y <= fm and y != 0:
                return x
            fm = y
            x -= interval
        if self[self.dom[0]] > fm:
            return self.dom[0]
        return x

    def __ave_max__(self):
        interval = (self.dom[1] - self.dom[0]) / 5000
        acum = 0
        count = 0
        lv = 0
        x = self.dom[0]
        while x < self.dom[1]:
            y = self[x]
            if y <= lv and y != 0:
                count += 1
                acum += x
            lv = y
            x += interval
        if self[self.dom[1]] <= lv:
            acum += self.dom[1]
            count += 1
        return acum / count

    def plot(self):
        interval = (self.dom[1] - self.dom[0]) / 2000
        x = []
        y = []
        a = self.dom[0]
        while a < self.dom[1]:
            x.append(a)
            y.append(self[a])
            a += interval
        x.append(self.dom[1])
        y.append(self[self.dom[1]])
        plt.ylim(0, 1.1)
        plt.plot(x, y, label=self.value_name)
        for p in self.points:
            plt.plot(p[0], p[1], p[3] + 'o', label=p[2])
        plt.legend()


class MembershipTriangular(Membership):

    def __init__(self, dom: tuple, a: float, b: float, c: float):
        super().__init__(dom)
        if dom[0] <= a <= b <= c <= dom[1]:
            self.a = float(a)
            self.b = float(b)
            self.c = float(c)
        else:
            raise Exception("invalid Triangular membership definition")

    def __evaluate__(self, x) -> float:
        if x <= self.a or x >= self.c:
            return 0.0
        if self.a < x < self.b:
            return (x - self.a) / (self.b - self.a)
        if self.b <= x < self.c:
            return (self.c - x) / (self.c - self.b)
        raise Exception("value outside dom")


class MembershipTrapezoidal(Membership):
    def __init__(self, dom: tuple, a: float, b: float, c: float, d: float):
        super().__init__(dom)
        if dom[0] <= a <= b <= c <= d <= dom[1]:
            self.a = float(a)
            self.b = float(b)
            self.c = float(c)
            self.d = float(d)
        else:
            raise Exception("invalid Trapezoidal definition")

    def __evaluate__(self, x) -> float:
        if self.b <= x <= self.c:
            return 1.0
        if self.dom[0] <= x <= self.a or self.d <= x <= self.dom[1]:
            return 0.0
        if self.a < x < self.b:
            return (x - self.a) / (self.b - self.a)
        if self.c < x < self.d:
            return (self.d - x) / (self.d - self.c)
        raise Exception("value outside dom")


class MembershipGausian(Membership):
    def __init__(self, dom: tuple, m: float, k: float):
        super().__init__(dom)
        if dom[0] <= m <= dom[1] and k > 0:
            self.m = m
            self.k = k
        else:
            raise Exception("invalid Gausian definition")

    def __evaluate__(self, x) -> float:
        if self.dom[0] <= x <= self.dom[1]:
            return math.e ** (-1 * self.k * (x - self.m) ** 2)
        raise Exception("value outside dom")


class MembershipSigmoidal(Membership):
    def __init__(self, dom: tuple, a: float, m: float, b: float):
        super().__init__(dom)
        if dom[0] <= a < m < b <= dom[1]:
            self.a = float(a)
            self.b = float(b)
            self.m = float(m)
        else:
            raise Exception("invalid Sigmoidal definition")

    def __evaluate__(self, x) -> float:
        if self.dom[0] <= x <= self.a:
            return 0.0
        if self.a < x <= self.m:
            return 2 * (((x - self.a)/(self.b - self.a)) ** 2)
        if self.m < x < self.b:
            return 1 - 2 * (((x - self.b)/(self.b - self.a)) ** 2)
        if self.b <= x <= self.dom[1]:
            return 1.0
        raise Exception("value outside dom")


class MembershipCombined(Membership):
    def __init__(self, dom: tuple, funcs: List[Membership]):
        super().__init__(dom)
        self.funcs = funcs

    def __evaluate__(self, x):
        value = 0
        for f in self.funcs:
            value = max(value, f[x])
        return value
