# https://logic.puzzlebaron.com
# origen: curso IA 2022

# Ayuda a Ramon a descubrir el nuevo horario de clases del último año. haga coincidir cada uno de su clase
# con el período apropiado y determine el maestro y el número de salón de cada uno

from logicpuzzles import *
from time import perf_counter

# Hay cuatro posibles salas
sala1 = (1, var(), var()) 
sala2 = (2, var(), var())
sala3 = (3, var(), var())
sala4 = (4, var(), var())
salas = (sala1, sala2, sala3, sala4)

# rooms(period, roomNumer, teacher)
def roomsproblem(salas):
    return lall(
        #1. La sala 215 partio 2 periodos despues de la clase del Sr. Lester. Lester partio 2 periodos antes de la sala 215
        right_of(salas, (var(), 215, var()), (var(), var(), 'Lester'), 2),
        
        #2. La clase del Sr. Jiménez es la clase del cuarto período o la clase en el salón 129
        lany(eq((4, var(), 'Jimenez'), sala4), membero((var(), 129, 'Jimenez'), salas)),
        neq((4, 129, 'Jimenez'), sala4),
        
        #4.La clase en la sala 322 se lleva a cabo 2 períodos antes de la clase del Sr. Duffy 
        left_of(salas, (var(), 322, var()), (var(), var(), 'Duffy'), 2),
 
        # datos no mencionados
        membero((var(), var(), 'Underwood'), salas),
        membero((var(), 129, var()), salas),
        membero((var(), 412, var()), salas)
        )

start = perf_counter()
solutions = run(0, salas, roomsproblem(salas),

#3. Las cuatro clases son la clase del salón 322, la clase del tercer período, la clase del segundo período y la clase del Sr. Underwood.
            differents(salas, ((2,3), (322,), ('Underwood',)))
    )
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)