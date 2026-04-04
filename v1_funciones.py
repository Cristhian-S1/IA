from kanren import var, run, eq, membero, conde, lall
from kanren.constraints import neq

from v1_misc import (
    reconstruir
)

IZQ = 0   # Borde izquierdo
DER = 1   # Borde derecho
ARR = 2   # Borde superior (arriba)
ABJ = 3   # Borde inferior (abajo)

def crear_puzzle(tetravex_lista_lista_tupla):
    tamanio = len(tetravex_lista_lista_tupla)
    celdas = []
    for fila in tetravex_lista_lista_tupla:
        for pieza in fila:
            celdas.append(tuple(pieza))
    return {"tamanio": tamanio, "piezas": celdas}

def coincidencia_horizontal(pieza_izq, pieza_der):
    izquierda1, derecha1, arriba1, abajo1 = var(), var(), var(), var()
    izquierda2, derecha2, arriba2, abajo2 = var(), var(), var(), var()
    return lall(
        eq(pieza_izq, (izquierda1, derecha1, arriba1, abajo1)),   # Destructurar pieza izquierda
        eq(pieza_der, (izquierda2, derecha2, arriba2, abajo2)),   # Destructurar pieza derecha
        eq(derecha1, izquierda2)                         # Restricción R1: der(izq) == izq(der)
    )

def coincidencia_vertical(pieza_sup, pieza_inf):
    izquierda1, derecha1, arriba1, abajo1 = var(), var(), var(), var()
    izquierda2, derecha2, arriba2, abajo2 = var(), var(), var(), var()
    return lall(
        eq(pieza_sup, (izquierda1, derecha1, arriba1, abajo1)),   # Destructurar pieza superior
        eq(pieza_inf, (izquierda2, derecha2, arriba2, abajo2)),   # Destructurar pieza inferior
        eq(abajo1, arriba2)                         # Restricción R2: abj(sup) == arr(inf)
    )

def resolver_tetravex(tetravex_diccionario):
    tamanio = tetravex_diccionario["tamanio"]
    pieza = tetravex_diccionario["piezas"]

    tablero = [[var(f'cell_{fila}_{columna}') for columna in range(tamanio)] for fila in range(tamanio)]
    plano = [tablero[fila][columna] for fila in range(tamanio) for columna in range(tamanio)]

    objetivos = []
    for fila in range(tamanio):
        for columna in range(tamanio):
            identificador = fila * tamanio + columna 
            objetivos.append(membero(tablero[fila][columna], pieza))

            if columna > 0:
                objetivos.append(coincidencia_horizontal(tablero[fila][columna - 1], tablero[fila][columna]))

            if fila > 0:
                objetivos.append(coincidencia_vertical(tablero[fila - 1][columna], tablero[fila][columna]))

            for prev_identificador in range(identificador):
                p_fila, p_columna = prev_identificador // tamanio, prev_identificador % tamanio
                objetivos.append(neq(tablero[p_fila][p_columna], tablero[fila][columna]))

    resulto = run(1, plano, *objetivos)

    # Reconstruimos la grilla nxn 
    if resulto:
        solucion = resulto[0]
        return reconstruir(solucion, tamanio)
    
    return None
