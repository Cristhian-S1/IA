# https://logic.puzzlebaron.com
# La Reserva Makombo rescata y rehabilita jirafas que han sido heridas o abandonadas en la naturaleza. 
# Usando solo las pistas a continuación, determine la altura, la edad y el país de origen de cada jirafa
# que se encuentra actualmente en la reserva.

from logicpuzzles import *
from time import perf_counter

# Hay cuatro jirafas
jirafa1 = (10, var(), var())
jirafa2 = (11, var(), var())
jirafa3 = (12, var(), var())
jirafa4 = (13, var(), var())
jirafas = (jirafa1, jirafa2, jirafa3, jirafa4)

# jirafas(altura, nombre, pais)
def giraffeproblem(jirafas):
    return lall(
        # 1. La jirafa Zakita es 1 pie más baja que la jirafa de Tanzania.
        left_of(jirafas, (var(), 'Zakita', var()), (var(), var(), 'Tanzania')),

        # 2. La jirafa Morutana vino de Somalia.
        membero((var(), 'Morutana', 'Somalia'), jirafas),

        # 3. La jirafa que mide 10 pies de alto es de Botswana o es la jirafa Jebedah.
        lany(eq((10, 'Jebedah', var()), jirafa1), eq((10, var(), 'Botswana'), jirafa1)),
        neq((10, 'Jebedah', 'Botswana'), jirafa1),
    
        # 4. La jirafa de Tanzania es 1 pie más bajo que la jirafa Angrit.
        left_of(jirafas, (var(), var(), 'Tanzania'), (var(), 'Angrit', var())),

        # 5. Valores en los dominios faltantes
        membero((var(), 'Jebedah', var()), jirafas),
        membero((var(), var(), 'Chad'), jirafas),
        membero((var(), var(), 'Botswana'), jirafas)
        )

start = perf_counter()
solutions = run(0, jirafas, giraffeproblem(jirafas))
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)