from sid.linguistic_variable import *
from sid.functions import *
from sid.rule import *
from sid.main import *
from sid.methods import *


servicio_pobre = LinguisticValue(
    "servicio", "pobre", MembershipTrapezoidal((0, 10), 0, 0, 2, 4))
servicio_bueno = LinguisticValue(
    "servicio", "bueno", MembershipTrapezoidal((0, 10), 3, 5, 7, 8))
servicio_excelente = LinguisticValue(
    "servicio", "excelente", MembershipTrapezoidal((0, 10), 7, 8, 10, 10))
servicio = LinguisticVar(
    "servicio", [servicio_pobre, servicio_bueno, servicio_excelente])


comida_mala = LinguisticValue(
    "comida", "mala", MembershipTrapezoidal((0, 10), 0, 0, 3, 5))
comida_deliciosa = LinguisticValue(
    "comida", "deliciosa", MembershipTrapezoidal(
        (0, 10), 7, 8, 10, 10)
)
comida = LinguisticVar(
    "comida", [comida_mala, comida_deliciosa]
)

propina_poca = LinguisticValue(
    "propina", "poca", MembershipTrapezoidal((0, 10), 0, 0, 3, 4)
)

propina_promedio = LinguisticValue(
    "propina", "promedio", MembershipTrapezoidal((0, 10), 3, 4, 7, 8)
)

propina_generosa = LinguisticValue(
    "propina", "generosa",  MembershipTrapezoidal(
        (0, 10), 7, 8, 10, 10)
)

propina = LinguisticVar(
    "propina", [propina_poca, propina_promedio, propina_generosa])


R1 = Rule(
    ExpressionAtomic(servicio_pobre) | ExpressionAtomic(comida_mala),
    propina_poca
)

R2 = Rule(
    ExpressionAtomic(servicio_bueno),
    propina_promedio
)

R3 = Rule(
    ExpressionAtomic(servicio_excelente) | ExpressionAtomic(
        comida_deliciosa),
    propina_generosa
)


s = SID([R1, R2, R3], [propina], AM_LARSEN,
        set([DM_CENTROID, DM_BISECCION, DM_FIRSTMAX, DM_LASTMAX, DM_AVEMAX]))
inp = {
    "servicio": 4,
    "comida": 7.5
}
s(inp)
s.plot()
s.reset()
inp = {
    "servicio": 6,
    "comida": 7.5
}
s(inp)
s.plot()
