from kanren import var, run, eq, membero, lall
from kanren.constraints import neq

from funciones_misc import (
    reconstruir
)

IZQ = 0   # Borde izquierdo
DER = 1   # Borde derecho
ARR = 2   # Borde superior (arriba)
ABJ = 3   # Borde inferior (abajo)

def crear_puzzle(tetravex_lista_lista_tupla):
    # Aplana el tablero 2D en un dict {tamanio, piezas} que consume el solver.
    tamanio = len(tetravex_lista_lista_tupla)
    celdas = []
    for fila in tetravex_lista_lista_tupla:
        for celda in fila:
            celdas.append(tuple(celda))
    return {"tamanio": tamanio, "piezas": celdas}

def coincidencia_horizontal(pieza_izq, pieza_der):
    # Goal MiniKanren: borde derecho de pieza_izq == borde izquierdo de pieza_der.
    izquierda1, derecha1, arriba1, abajo1 = var(), var(), var(), var()
    izquierda2, derecha2, arriba2, abajo2 = var(), var(), var(), var()
    return lall(
        eq(pieza_izq, (izquierda1, derecha1, arriba1, abajo1)),   # Destructurar pieza izquierda
        eq(pieza_der, (izquierda2, derecha2, arriba2, abajo2)),   # Destructurar pieza derecha
        eq(derecha1, izquierda2)                         # Restricción R1: der(izq) == izq(der)
    )

def coincidencia_vertical(pieza_sup, pieza_inf):
    # Goal MiniKanren: borde inferior de pieza_sup == borde superior de pieza_inf.
    izquierda1, derecha1, arriba1, abajo1 = var(), var(), var(), var()
    izquierda2, derecha2, arriba2, abajo2 = var(), var(), var(), var()
    return lall(
        eq(pieza_sup, (izquierda1, derecha1, arriba1, abajo1)),   # Destructurar pieza superior
        eq(pieza_inf, (izquierda2, derecha2, arriba2, abajo2)),   # Destructurar pieza inferior
        eq(abajo1, arriba2)                         # Restricción R2: abj(sup) == arr(inf)
    )

def resolver_tetravex(tetravex_diccionario):
    # Resuelve el puzzle con MiniKanren: una variable por celda con restricciones de membresía, adyacencia y unicidad.
    tamanio = tetravex_diccionario["tamanio"]
    piezas = tetravex_diccionario["piezas"]
    n = tamanio * tamanio

    # celdas: N*N variables lógicas que MiniKanren resolverá
    celdas = [var(f'c{i}') for i in range(n)]
    objetivos = []

    for indice_tablero in range(n):
        fila, columna = divmod(indice_tablero, tamanio)

        # (1) membero: asigna un valor concreto a la celda
        objetivos.append(membero(celdas[indice_tablero], piezas))

        # (2) adyacencia: poda inmediatamente si el valor asignado no
        #     coincide con el borde del vecino ya colocado
        if columna > 0:
            objetivos.append(coincidencia_horizontal(celdas[indice_tablero - 1], celdas[indice_tablero]))
        if fila > 0:
            objetivos.append(coincidencia_vertical(celdas[indice_tablero - tamanio], celdas[indice_tablero]))

        # (3) unicidad: la celda no puede repetir ninguna pieza anterior
        for prev in range(indice_tablero):
            objetivos.append(neq(celdas[prev], celdas[indice_tablero]))

    # resultado: tupla con las soluciones encontradas; pedimos solo 1
    resultado = run(1, celdas, *objetivos)
    return reconstruir(resultado[0], tamanio) if resultado else None
