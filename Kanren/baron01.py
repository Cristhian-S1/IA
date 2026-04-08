# https://logic.puzzlebaron.com

from logicpuzzles import *
from time import perf_counter

# Hay cuatro prestamos
prestamo1 = ( 1,var(),var())
prestamo2 = ( 8,var(),var())
prestamo3 = (15,var(),var())
prestamo4 = (22,var(),var())
prestamos = (prestamo1, prestamo2, prestamo3, prestamo4)

# prestamo(dia, nombre, libro)
def borrowsproblem(prestamos):
    return lall(
    # 1. Ora's book was due on September 8.
    eq((8, 'ora', var()), prestamo2),
    
    # 2. "Dancing Well" was due 1 week after Yvette's book.
    right_of(prestamos, (var(), var(), 'dancing well'), (var(), 'yvette', var())),

    # 3. "Ohio Haunts" was due 2 weeks before "Kip and Ken".
    left_of(prestamos, (var(), var(), 'ohio haunts'), (var(), var(), 'kip and ken'), 2),

    # 4. Cory's book was due on September 15.
    eq((15,'cory',var()), prestamo3),
    
    # 5. otros valores de los dominios
    membero((var(), 'wayne', var()), prestamos),
    membero((var(), var(), 'stars bellow'), prestamos)
    )

start = perf_counter()
solutions = run(0, prestamos, borrowsproblem(prestamos))
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)