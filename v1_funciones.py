from kanren import var, run, eq, membero, lall
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
    piezas = tetravex_diccionario["piezas"]
    n = tamanio * tamanio

    celdas = [var(f'c{i}') for i in range(n)]
    objetivos = []

    for idx in range(n):
        fila, columna = divmod(idx, tamanio)

        # (1) membero: asigna un valor concreto a la celda
        objetivos.append(membero(celdas[idx], piezas))

        # (2) adyacencia: poda inmediatamente si el valor asignado no
        #     coincide con el borde del vecino ya colocado
        if columna > 0:
            objetivos.append(coincidencia_horizontal(celdas[idx - 1], celdas[idx]))
        if fila > 0:
            objetivos.append(coincidencia_vertical(celdas[idx - tamanio], celdas[idx]))

        # (3) unicidad: la celda no puede repetir ninguna pieza anterior
        for prev in range(idx):
            objetivos.append(neq(celdas[prev], celdas[idx]))

    resultado = run(1, celdas, *objetivos)
    return reconstruir(resultado[0], tamanio) if resultado else None
