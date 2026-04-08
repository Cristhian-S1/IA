# https://logic.puzzlebaron.com
# origen: curso IA 2022


from logicpuzzles import *
from time import perf_counter

# Hay cuatro objetos
planeta1 = (41, var(), var())
planeta2 = (43, var(), var())
planeta3 = (45, var(), var())
planeta4 = (47, var(), var())
planetas = (planeta1, planeta2, planeta3, planeta4)

# planeta(años luz, nombre, estrella)
def planetsproblem(planetas):
    return lall(
            # 1. De Hinveng y la estrella que orbita el exoplaneta VJD 913, uno está a 41 años luz de la Tierra y el otro está a 45 años luz de la Tierra.
            conde((eq((41, 'Hinveng', var()), planeta1), eq((45, var(), 'VJD 913'), planeta3)), (eq((45, 'Hinveng', var()), planeta1), eq((41, var(), 'VJD 913'), planeta3))),

            # 2. Fihin está 2 años luz más lejos de nosotros que Ereph.
            right_of(planetas, (var(), 'Fihin', var()), (var(), 'Ereph', var())),

            # 3. Istryn es el planeta a 41 años luz de la Tierra o la estrella que orbita el exoplaneta EX 53.
            lany(eq((41, 'Istryn', var()), planeta1), membero((var(), 'Istryn', 'EX 53'), planetas)),
            neq((41, 'Istryn', 'EX 53'), planeta1), 

            # 4. El planeta que orbita la estrella HV 491 está 2 años luz más cerca de nosotros que Ereph.
            left_of(planetas, (var(), var(), 'HV 491'), (var(), 'Ereph', var())),

            # 5. Valores en los dominios faltantes
            membero((var(), var(),'PLC 120'), planetas),
            )

start = perf_counter()
solutions = run(0, planetas, planetsproblem(planetas))
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)