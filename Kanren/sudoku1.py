from kanren import *
from kanren.constraints import neq
from itertools import combinations, chain
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
# Tiempo: 3672.1879042000005 [segundos]
#

#crea la grilla con variables var de kanren
def create_grid():
    return tuple(tuple(var('{}{}'.format(i, j)) for j in range(9)) for i in range(9))

def transpose_grid():
    return tuple(tuple(var('{}{}'.format(j, i)) for j in range(9)) for i in range(9))

# restringe la grilla a los valores originales del sudoku
def restrict_sudoku(grid, sudoku):
    return lall(eq(grid[i][j], sudoku[i][j]) for i in range(9) for j in range(9) if sudoku[i][j] != 0)

# restinge los valores de las variables var al rango 1..9
def domains(grid):
    return lall(membero(grid[i][j], (1,2,3,4,5,6,7,8,9,)) for i in range(9) for j in range(9)) 

# restinge todos los valores diferentes en cada fila de la grilla
def differents(grid):
    return lall(neq(r1,r2) for row in grid for r1,r2 in combinations(row,2))

# retona un generador de celdas de 3x3 de la grilla original
def celda(grid):
    particiones = ((0,3),(3,6),(6,9))
    x = tuple(grid[i1:i2] for i1,i2 in particiones)
    return ((row1[j1:j2], row2[j1:j2], row3[j1:j2]) for row1, row2, row3 in x for j1,j2 in particiones)

# solver
def solve_sudoku(grid, tgrid, sudoku):
    return lall(
        restrict_sudoku(grid, sudoku),

        differents(grid),
        differents(tgrid),
        differents(tuple(tuple(chain(*row)) for row in celda(grid))),

        domains(grid),
        )

# main
sudoku = tuple(tuple(ss.diabolic[row]) for row in range(9))

grid = create_grid()
tgrid = transpose_grid()

start = perf_counter()
solutions = run(0, grid, solve_sudoku(grid, tgrid, sudoku))
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)
