from kanren import *
from kanren.constraints import neq
import numpy as np
from itertools import combinations
from time import perf_counter
import samples_sudoku as ss

# Solución:
# (((1, 6, 4, 9, 5, 7, 2, 8, 3),
#   (3, 8, 5, 6, 2, 1, 9, 7, 4), 
#   (7, 2, 9, 4, 3, 8, 6, 5, 1), 
#   (5, 3, 7, 2, 8, 9, 4, 1, 6), 
#   (4, 1, 2, 7, 6, 3, 8, 9, 5), 
#   (6, 9, 8, 5, 1, 4, 3, 2, 7), 
#   (8, 4, 3, 1, 9, 5, 7, 6, 2), 
#   (9, 5, 6, 3, 7, 2, 1, 4, 8), 
#   (2, 7, 1, 8, 4, 6, 5, 3, 9)),)
#
# Tiempo: 4134.324505 [segundos]
#

#crea la grilla con variables var de kanren
def create_grid():
    return tuple(tuple(var('{}{}'.format(i, j)) for j in range(9)) for i in range(9))

# restringe la grilla a los valores originales del sudoku
def restrict_sudoku(agrid, sudoku):
    return lall(eq(agrid[i,j], sudoku[i,j]) for i in range(9) for j in range(9) if sudoku[i,j] != 0)

# restinge los valores de las variables var al rango 1..9
def domains(agrid):
    return lall(membero(agrid[i,j], (1,2,3,4,5,6,7,8,9,)) for i in range(9) for j in range(9)) 

# restinge todos los valores diferentes en cada fila de la grilla
def differents(agrid):
    return lall(neq(r1,r2) for row in agrid for r1,r2 in combinations(row,2))

# retona una matriz de celdas de 3x3 de la grilla original
def celda(agrid):
    return np.stack(list(agrid[i1:i2,j1:j2].flatten() for i1,i2 in ((0,3),(3,6),(6,9)) for j1,j2 in ((0,3),(3,6),(6,9))))

def solve_sudoku(agrid, sudoku):
    return lall(
        restrict_sudoku(agrid, sudoku),

        differents(agrid),
        differents(agrid.transpose()),
        differents(celda(agrid)),

        domains(agrid),
        )

# main
grid = create_grid()

agrid  = np.array(grid)
sudoku = np.array(ss.diabolic)

start = perf_counter()
# solutions no funciona con matrices numpy (parametro grid)
solutions = run(0, grid, solve_sudoku(agrid, sudoku))
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)
