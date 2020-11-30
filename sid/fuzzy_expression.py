from sid.linguistic_variable import LinguisticValue


class Expression:
    def __invert__(self):
        return ExpressionInvert(self)

    def __and__(self, other):
        return ExpressionAnd(self, other)

    def __or__(self, other):
        return ExpressionOr(self, other)

    def __repr__(self):
        return str(self.value)


class ExpressionInvert(Expression):
    def __init__(self, expr: Expression):
        self.expr = expr

    def __call__(self, inp) -> float:
        return 1 - self.expr(inp)


class ExpressionAnd(Expression):
    def __init__(self, l_expr: Expression, r_expr: Expression):
        self.l_expr = l_expr
        self.r_expr = r_expr

    def __call__(self, inp) -> float:
        return min(self.l_expr(inp), self.r_expr(inp))


class ExpressionOr(Expression):
    def __init__(self, l_expr: Expression, r_expr: Expression):
        self.l_epr = l_expr
        self.r_expr = r_expr

    def __call__(self, inp):
        return max(self.l_epr(inp), self.r_expr(inp))


class ExpressionAtomic(Expression):
    def __init__(self, ling_value: LinguisticValue):
        self.ling_value = ling_value

    def __call__(self, inp: dict) -> float:
        return self.ling_value(inp)
