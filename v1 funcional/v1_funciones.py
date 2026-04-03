from kanren import var, run, eq, membero, conde, lall
from kanren.constraints import neq

from v1_misc import (
    reconstruir
)

IZQ = 0   # Borde izquierdo
DER = 1   # Borde derecho
ARR = 2   # Borde superior (arriba)
ABJ = 3   # Borde inferior (abajo)

def crear_puzzle(puzzle_input):
    n = len(puzzle_input)
    tiles = []
    for fila in puzzle_input:
        for pieza in fila:
            tiles.append(tuple(pieza))
    return {"n": n, "tiles": tiles}

def coincidencia_horizontal(pieza_izq, pieza_der):
    l1, r1, t1, b1 = var(), var(), var(), var()
    l2, r2, t2, b2 = var(), var(), var(), var()
    return lall(
        eq(pieza_izq, (l1, r1, t1, b1)),   # Destructurar pieza izquierda
        eq(pieza_der, (l2, r2, t2, b2)),   # Destructurar pieza derecha
        eq(r1, l2)                         # Restricción R1: der(izq) == izq(der)
    )

def coincidencia_vertical(pieza_sup, pieza_inf):
    l1, r1, t1, b1 = var(), var(), var(), var()
    l2, r2, t2, b2 = var(), var(), var(), var()
    return lall(
        eq(pieza_sup, (l1, r1, t1, b1)),   # Destructurar pieza superior
        eq(pieza_inf, (l2, r2, t2, b2)),   # Destructurar pieza inferior
        eq(b1, t2)                          # Restricción R2: abj(sup) == arr(inf)
    )

def resolver_tetravex(puzzle_dict):
    n = puzzle_dict["n"]
    tiles = puzzle_dict["tiles"]

    grid = [[var(f'cell_{r}_{c}') for c in range(n)] for r in range(n)]
    flat = [grid[r][c] for r in range(n) for c in range(n)]

    goals = []
    for r in range(n):
        for c in range(n):
            idx = r * n + c 
            goals.append(membero(grid[r][c], tiles))

            if c > 0:
                goals.append(coincidencia_horizontal(grid[r][c - 1], grid[r][c]))

            if r > 0:
                goals.append(coincidencia_vertical(grid[r - 1][c], grid[r][c]))

            for prev_idx in range(idx):
                pr, pc = prev_idx // n, prev_idx % n
                goals.append(neq(grid[pr][pc], grid[r][c]))

    result = run(1, flat, *goals)

    # Reconstruimos la grilla nxn 
    if result:
        solution = result[0]
        return reconstruir(solution, n)
    
    return None
