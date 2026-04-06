import random

IZQ = 0   # Borde izquierdo
DER = 1   # Borde derecho
ARR = 2   # Borde superior (arriba)
ABJ = 3   # Borde inferior (abajo)

def reconstruir(solucion_plana, tamanio_tablero):
    """ Recibe la lista plana que devuelve MiniKanren y la convierte de vuelta a una lista de listas o 2D"""
    tablero = []
    for fila in range(tamanio_tablero):
        filas = []
        for columna in range(tamanio_tablero):
            filas.append(solucion_plana[fila * tamanio_tablero + columna])
        tablero.append(filas)
    return tablero

def verificar_solucion(tablero):
    if tablero is None:
        return False

    tamanio_tablero = len(tablero)
    errores = 0

    for fila in range(tamanio_tablero):
        for columna in range(tamanio_tablero):
            # R1: Horizontal
            if columna + 1 < tamanio_tablero:
                if tablero[fila][columna][DER] != tablero[fila][columna + 1][IZQ]:
                    print(f"  X Horizontal ({fila},{columna})->({fila},{columna+1}): "
                          f"{tablero[fila][columna][DER]} != {tablero[fila][columna+1][IZQ]}")
                    errores += 1

            # R2: Vertical
            if fila + 1 < tamanio_tablero:
                if tablero[fila][columna][ABJ] != tablero[fila + 1][columna][ARR]:
                    print(f"  X Vertical ({fila},{columna})->({fila+1},{columna}): "
                          f"{tablero[fila][columna][ABJ]} != {tablero[fila+1][columna][ARR]}")
                    errores += 1

    if errores == 0:
        print("  [OK] Solucion valida — todas las restricciones satisfechas.")
    else:
        print(f"  [FAIL] {errores} restriccion(es) violada(s).")

    return errores == 0

def imprimir_puzzle(tablero, titulo="TetraVex"):
    if tablero is None:
        print(f"\n{titulo}: Sin solucion!")
        return

    print(f"\n{titulo}:")
    for fila in tablero:
        partes = []
        for pieza in fila:
            partes.append(f"({pieza[IZQ]} {pieza[DER]} {pieza[ARR]} {pieza[ABJ]})")
        print("  " + " ".join(partes))

def tetravex_aleatorio(tamanio_tablero, valor_maximo_ficha=9):
    tablero = [[None for _ in range(tamanio_tablero)] for _ in range(tamanio_tablero)]

    for fila in range(tamanio_tablero):
        for columna in range(tamanio_tablero):
            izq    = random.randint(0, valor_maximo_ficha)
            der    = random.randint(0, valor_maximo_ficha)
            arriba = random.randint(0, valor_maximo_ficha)
            abajo  = random.randint(0, valor_maximo_ficha)

            # Forzar coincidencia con vecino izquierdo
            if columna > 0:
                izq = tablero[fila][columna - 1][DER]

            # Forzar coincidencia con vecino superior
            if fila > 0:
                arriba = tablero[fila - 1][columna][ABJ]

            tablero[fila][columna] = (izq, der, arriba, abajo)

    # Mezclar piezas aleatoriamente
    piezas = [tablero[fila][columna] for fila in range(tamanio_tablero) for columna in range(tamanio_tablero)]
    random.shuffle(piezas)

    # Reestructurar como lista de listas
    tetravex = []
    for fila in range(tamanio_tablero):
        filas = []
        for columna in range(tamanio_tablero):
            filas.append(piezas[fila * tamanio_tablero + columna])
        tetravex.append(filas)

    return tetravex

def leer_puzzle_manual(tamanio_tablero):
    print(f"\nIngrese las {tamanio_tablero * tamanio_tablero} piezas del puzzle {tamanio_tablero}x{tamanio_tablero}.")
    print("Formato por pieza: izquierda derecha arriba abajo")
    print("Ejemplo: 7 0 6 4\n")

    piezas = []
    for i in range(tamanio_tablero * tamanio_tablero):
        while True:
            try:
                pieza_cruda = input(f"  Pieza {i + 1}: ").strip()
                pieza_tupla = tuple(int(x) for x in pieza_cruda.split())
                if len(pieza_tupla) != 4:
                    print("    -> Error: ingrese exactamente 4 numeros.")
                    continue
                piezas.append(pieza_tupla)
                break
            except ValueError:
                print("    -> Error: ingrese numeros enteros validos.")

    tetravex = []
    for fila in range(tamanio_tablero):
        filas = []
        for columna in range(tamanio_tablero):
            filas.append(piezas[fila * tamanio_tablero + columna])
        tetravex.append(filas)

    return tetravex

