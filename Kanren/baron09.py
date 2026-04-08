# https://logic.puzzlebaron.com
# origen: curso IA 2022

# La Fuerza Aérea de EE UU, está actualmente probando una serie de nuevos aviones supersónicos experimentales,
# cada uno construido por una compañía aeroespacial diferente. Usando solo las pistas, determinar el precio
# de cada avión, así como el nombre del avión y el nombre de la compañía que lo construyó.

from logicpuzzles import *
from time import perf_counter

# Hay cuatro aviones
avion1 = ('100M', var(), var())
avion2 = ('125M', var(), var())
avion3 = ('150M', var(), var())
avion4 = ('175M', var(), var())
aviones = (avion1, avion2, avion3, avion4)

# aerofobo(mes, nombre, amuleto)
def planesproblem(aviones):
    return lall(
        # 1. El raven-12 fue construido por Forsyth.
        membero((var(), 'raven-12', 'Forsyth'), aviones),

        # 2. El dragon-f15 cuesta 50 millones de dólares menos que el kessling.
        left_of(aviones, (var(), 'dragon-f15', var()), (var(), 'kessling', var()), 2),

        # 3. El dragon-f15 fue construido por Wiseman.
        membero((var(), 'dragon-f15', 'Wiseman'), aviones),

        # 4. El jett construido por MCConnell cuesta 25 millones de dólares menos que el avión construido por Wiseman
        left_of(aviones, (var(), var(), 'McConnell'), (var(), var(), 'Wiseman')),

        # 5. Valores en los dominios faltantes
        membero((var(), 'falcon-x2', var()), aviones),
        membero((var(), var(), 'Pittakan'), aviones)
    )

start = perf_counter()
solutions = run(0, aviones, planesproblem(aviones))
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)

