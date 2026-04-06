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
    """
    Convierte el tablero 2D en el formato de diccionario que espera el solver.

    Aplana la cuadrícula de piezas en una lista plana y registra el tamaño
    del tablero para que `resolver_tetravex` pueda reconstruir índices 2D.

    Entrada:
        tetravex_lista_lista_tupla -- list[list[tuple]]: cuadrícula NxN de piezas.
                                      Ej: [[(0,1,2,3),(4,5,6,7)], [(1,2,3,4),(5,6,7,8)]]

    Salida:
        dict con dos claves:
            "tamanio" -- int: lado N del tablero cuadrado.
            "piezas"  -- list[tuple]: lista plana con N*N piezas en orden fila-mayor.
                         Es el conjunto de valores posibles para cada celda del solver.
    """
    tamanio = len(tetravex_lista_lista_tupla)
    celdas = []
    for fila in tetravex_lista_lista_tupla:
        for celda in fila:
            celdas.append(tuple(celda))
    return {"tamanio": tamanio, "piezas": celdas}

def coincidencia_horizontal(pieza_izq, pieza_der):
    """
    Crea la restricción MiniKanren que obliga a que dos piezas adyacentes
    horizontalmente compartan el mismo valor de borde.

    Destructura ambas piezas en variables lógicas y añade la restricción
    R1: borde derecho de la pieza izquierda == borde izquierdo de la pieza derecha.

    Entrada:
        pieza_izq -- var (variable lógica MiniKanren): celda de la columna j.
        pieza_der -- var (variable lógica MiniKanren): celda de la columna j+1,
                     a la derecha de pieza_izq en la misma fila.

    Salida:
        lall goal: goal compuesto que unifica las estructuras de ambas piezas
                   y exige derecha1 == izquierda2.

    Variables internas relevantes:
        izquierda1..abajo1 -- var: componentes lógicos de pieza_izq (izq, der, arr, abj).
        izquierda2..abajo2 -- var: componentes lógicos de pieza_der (izq, der, arr, abj).
    """
    izquierda1, derecha1, arriba1, abajo1 = var(), var(), var(), var()
    izquierda2, derecha2, arriba2, abajo2 = var(), var(), var(), var()
    return lall(
        eq(pieza_izq, (izquierda1, derecha1, arriba1, abajo1)),   # Destructurar pieza izquierda
        eq(pieza_der, (izquierda2, derecha2, arriba2, abajo2)),   # Destructurar pieza derecha
        eq(derecha1, izquierda2)                         # Restricción R1: der(izq) == izq(der)
    )

def coincidencia_vertical(pieza_sup, pieza_inf):
    """
    Crea la restricción MiniKanren que obliga a que dos piezas adyacentes
    verticalmente compartan el mismo valor de borde.

    Destructura ambas piezas en variables lógicas y añade la restricción
    R2: borde inferior de la pieza superior == borde superior de la pieza inferior.

    Entrada:
        pieza_sup -- var (variable lógica MiniKanren): celda de la fila i.
        pieza_inf -- var (variable lógica MiniKanren): celda de la fila i+1,
                     directamente debajo de pieza_sup en la misma columna.

    Salida:
        lall goal: goal compuesto que unifica las estructuras de ambas piezas
                   y exige abajo1 == arriba2.

    Variables internas relevantes:
        izquierda1..abajo1 -- var: componentes lógicos de pieza_sup (izq, der, arr, abj).
        izquierda2..abajo2 -- var: componentes lógicos de pieza_inf (izq, der, arr, abj).
    """
    izquierda1, derecha1, arriba1, abajo1 = var(), var(), var(), var()
    izquierda2, derecha2, arriba2, abajo2 = var(), var(), var(), var()
    return lall(
        eq(pieza_sup, (izquierda1, derecha1, arriba1, abajo1)),   # Destructurar pieza superior
        eq(pieza_inf, (izquierda2, derecha2, arriba2, abajo2)),   # Destructurar pieza inferior
        eq(abajo1, arriba2)                         # Restricción R2: abj(sup) == arr(inf)
    )

def resolver_tetravex(tetravex_diccionario):
    """
    Núcleo del solver: plantea el puzzle como un problema de satisfacción de
    restricciones (CSP) y lo resuelve usando MiniKanren.

    Para cada celda del tablero crea una variable lógica y añade tres tipos
    de goals al motor de búsqueda:
        1. membero   — la celda debe tomar el valor de alguna pieza del conjunto.
        2. adyacencia — si tiene vecino izquierdo/superior, sus bordes deben coincidir.
        3. neq        — la celda no puede repetir ninguna pieza ya colocada.

    MiniKanren realiza búsqueda con backtracking sobre este espacio de restricciones.

    Entrada:
        tetravex_diccionario -- dict:
            "tamanio" -- int: lado N del tablero.
            "piezas"  -- list[tuple]: conjunto de N*N piezas disponibles.

    Salida:
        list[list[tuple]] | None: cuadrícula 2D con la solución encontrada,
                                  o None si no existe ninguna asignación válida.

    Variables internas relevantes:
        celdas         -- list[var]: lista de N*N variables lógicas, una por celda.
                          celdas[i] corresponde a la fila=i//N, columna=i%N.
        objetivos      -- list[goal]: acumulación de todos los goals (restricciones)
                          que MiniKanren debe satisfacer simultáneamente.
        indice_tablero -- int: índice lineal de la celda actual (0..N*N-1).
        fila, columna  -- int: coordenadas 2D derivadas de indice_tablero via divmod.
        resultado      -- tuple: respuesta de run(1, celdas, *objetivos).
                          Si hay solución, resultado[0] es la lista plana de piezas
                          asignadas en el mismo orden que `celdas`.
    """
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
