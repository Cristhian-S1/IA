import random

IZQ = 0   # Borde izquierdo
DER = 1   # Borde derecho
ARR = 2   # Borde superior (arriba)
ABJ = 3   # Borde inferior (abajo)

def reconstruir(solucion_plana, tamanio_tablero):
    """
    Convierte la lista plana que devuelve MiniKanren en una cuadrícula 2D.

    MiniKanren resuelve sobre una lista lineal de variables (celdas).
    Esta función reorganiza esa lista en filas y columnas para
    que el resultado sea legible y compatible con las demás funciones.

    Entrada:
        solucion_plana   -- list[tuple]: lista con N*N piezas en orden fila-mayor.
                            Ej: [(0,1,2,3), (1,2,3,4), ...] para un tablero 2x2
        tamanio_tablero  -- int: lado del tablero cuadrado (N). Ej: 2, 3, 4

    Salida:
        tablero -- list[list[tuple]]: cuadrícula 2D de piezas.
                   tablero[fila][columna] es la pieza en esa posición.
    """
    tablero = []
    for fila in range(tamanio_tablero):
        filas = []
        for columna in range(tamanio_tablero):
            # Índice lineal → posición 2D: índice = fila * N + columna
            filas.append(solucion_plana[fila * tamanio_tablero + columna])
        tablero.append(filas)
    return tablero

def verificar_solucion(tablero):
    """
    Valida que todas las restricciones de borde estén satisfechas en el tablero resuelto.

    Recorre cada par de celdas adyacentes (horizontal y vertical) y comprueba
    que los bordes que se tocan sean iguales. Imprime los conflictos encontrados.

    Entrada:
        tablero -- list[list[tuple]] | None: cuadrícula 2D con las piezas colocadas.
                   None indica que el solver no encontró solución.

    Salida:
        bool: True si todas las restricciones se cumplen, False si hay al menos un error
              o si el tablero es None.

    Variables internas relevantes:
        errores -- int: contador acumulado de restricciones violadas.
    """
    if tablero is None:
        return False

    tamanio_tablero = len(tablero)
    errores = 0

    for fila in range(tamanio_tablero):
        for columna in range(tamanio_tablero):
            # R1: Horizontal — el borde derecho de (fila,col) debe coincidir
            #     con el borde izquierdo de (fila, col+1)
            if columna + 1 < tamanio_tablero:
                if tablero[fila][columna][DER] != tablero[fila][columna + 1][IZQ]:
                    print(f"  X Horizontal ({fila},{columna})->({fila},{columna+1}): "
                          f"{tablero[fila][columna][DER]} != {tablero[fila][columna+1][IZQ]}")
                    errores += 1

            # R2: Vertical — el borde inferior de (fila,col) debe coincidir
            #     con el borde superior de (fila+1, col)
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
    """
    Muestra el tablero en consola con un formato legible por humanos.

    Imprime cada pieza como (izq der arr abj) en una línea por fila.

    Entrada:
        tablero -- list[list[tuple]] | None: cuadrícula 2D a mostrar.
                   Si es None imprime un mensaje de sin solución.
        titulo  -- str: encabezado que se muestra antes del tablero.
    """
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
    """
    Genera un puzzle Tetravex aleatorio con solución garantizada.

    Construye el tablero posición por posición forzando que los bordes
    internos coincidan con los vecinos ya colocados (izquierdo y superior).
    Luego baraja las piezas para que el orden de entrada al solver sea aleatorio.

    Entrada:
        tamanio_tablero      -- int: lado del tablero cuadrado (N). Ej: 2, 3, 4
        valor_maximo_ficha   -- int: valor máximo que puede tener un borde (inclusive).
                                Por defecto 9, dando valores 0-9.

    Salida:
        tetravex -- list[list[tuple]]: cuadrícula 2D con las piezas desordenadas.
                    Contiene exactamente N*N piezas únicas con al menos una solución.

    Variables internas relevantes:
        tablero  -- list[list[tuple]]: grilla auxiliar donde se construye el puzzle
                    con bordes coherentes antes de mezclar.
        piezas   -- list[tuple]: versión plana de `tablero`, mezclada con shuffle.
                    Entrada directa para reconstruir el `tetravex` desordenado.
    """
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

    # piezas: lista plana con las N*N piezas coherentes, listas para mezclar
    piezas = [tablero[fila][columna] for fila in range(tamanio_tablero) for columna in range(tamanio_tablero)]
    random.shuffle(piezas)

    # Reestructurar como lista de listas (desordenada)
    tetravex = []
    for fila in range(tamanio_tablero):
        filas = []
        for columna in range(tamanio_tablero):
            filas.append(piezas[fila * tamanio_tablero + columna])
        tetravex.append(filas)

    return tetravex

def leer_puzzle_manual(tamanio_tablero):
    """
    Lee las piezas del puzzle desde la entrada estándar (teclado).

    Solicita al usuario N*N piezas en formato "izquierda derecha arriba abajo".
    Valida que cada pieza tenga exactamente 4 enteros antes de aceptarla.

    Entrada:
        tamanio_tablero -- int: lado del tablero cuadrado (N).

    Salida:
        tetravex -- list[list[tuple]]: cuadrícula 2D con las piezas ingresadas
                    en el mismo orden en que el usuario las proporcionó.

    Variables internas relevantes:
        piezas       -- list[tuple]: acumulador plano de las piezas leídas
                        antes de reorganizarlas en 2D.
        pieza_cruda  -- str: línea de texto cruda ingresada por el usuario.
        pieza_tupla  -- tuple[int,...]: conversión de `pieza_cruda` a tupla de enteros.
    """
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
