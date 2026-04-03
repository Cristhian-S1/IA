import time
import random
from collections import defaultdict
from kanren import var, run, eq, membero, conde, lall
from kanren.constraints import neq

IZQ = 0   # Borde izquierdo
DER = 1   # Borde derecho
ARR = 2   # Borde arriba
ABJ = 3   # Borde abajo
def crear_puzzle(puzzle_input):
    n = len(puzzle_input)
    tiles = []
    for fila in puzzle_input:
        for pieza in fila:
            tiles.append(tuple(pieza))
    return {"n": n, "tiles": tiles}

def construir_indices(tiles):
    por_izq = defaultdict(list)
    por_der = defaultdict(list)
    por_arr = defaultdict(list)
    por_abj = defaultdict(list)

    for pieza in tiles:
        por_izq[pieza[IZQ]].append(pieza)
        por_der[pieza[DER]].append(pieza)
        por_arr[pieza[ARR]].append(pieza)
        por_abj[pieza[ABJ]].append(pieza)

    return { "por_izq": por_izq, "por_der": por_der, "por_arr": por_arr, "por_abj": por_abj }

def match_horizontal(pieza_izq, pieza_der):
    l1, r1, t1, b1 = var(), var(), var(), var()
    l2, r2, t2, b2 = var(), var(), var(), var()
    return lall(
        eq(pieza_izq, (l1, r1, t1, b1)),
        eq(pieza_der, (l2, r2, t2, b2)),
        eq(r1, l2)
    )

def match_vertical(pieza_sup, pieza_inf):
    l1, r1, t1, b1 = var(), var(), var(), var()
    l2, r2, t2, b2 = var(), var(), var(), var()
    return lall(
        eq(pieza_sup, (l1, r1, t1, b1)),
        eq(pieza_inf, (l2, r2, t2, b2)),
        eq(b1, t2)
    )

def solve_tetravex(puzzle_dict):
    n = puzzle_dict["n"]
    tiles = puzzle_dict["tiles"]

    # Crear variables lógicas para cada celda
    grid = [[var(f'cell_{r}_{c}') for c in range(n)] for r in range(n)]
    flat = [grid[r][c] for r in range(n) for c in range(n)]

    # Construir el goal recursivo que asigna pieza por pieza
    goal = _colocar_pieza(grid, tuple(tiles), n, 0, 0, {})
    # Ejecutar miniKanren
    result = run(1, flat, goal)

    if result:
        return reshapear(result[0], n)
    return None

def _colocar_pieza(grid, disponibles, n, r, c, colocadas):
    # ── Caso base: todas las celdas llenadas exitosamente ──
    if r >= n:
        return lall()  # Éxito: no hay más condiciones

    # Calcular siguiente posición (recorrido fila por fila)
    sig_r, sig_c = (r, c + 1) if c + 1 < n else (r + 1, 0)

    # ── Filtrar piezas candidatas ──
    clausulas = []

    for i in range(len(disponibles)):
        pieza = disponibles[i]

        # Verificar restricción HORIZONTAL: Si hay vecino a la izquierda, su borde derecho debe
        # coincidir con el borde izquierdo de esta pieza.
        if c > 0:
            vecino_izq = colocadas[(r, c - 1)]
            if vecino_izq[DER] != pieza[IZQ]:
                continue  # Poda: pieza incompatible → no incluir

        # Verificar restricción VERTICAL: Si hay vecino arriba, su borde inferior debe coincidir
        # con el borde superior de esta pieza.
        if r > 0:
            vecino_sup = colocadas[(r - 1, c)]
            if vecino_sup[ABJ] != pieza[ARR]:
                continue  # Poda: pieza incompatible → no incluir

        # ── Pieza válida: construir cláusula para conde ──
        nuevas_disponibles = disponibles[:i] + disponibles[i+1:]
        nuevas_colocadas = dict(colocadas)
        nuevas_colocadas[(r, c)] = pieza

        clausulas.append([
            eq(grid[r][c], pieza),                                              # Unificar celda con pieza
            _colocar_pieza(grid, nuevas_disponibles, n, sig_r, sig_c, nuevas_colocadas)  # Recurrir
        ])

    # ── Si no hay candidatas válidas → goal que falla ──
    if not clausulas:
        return lambda s: iter([])  # Fail: miniKanren hace backtrack

    # ── conde: miniKanren explorará cada alternativa ──
    return conde(*clausulas)

def reshapear(flat_solution, n):
    grid = []
    for r in range(n):
        fila = []
        for c in range(n):
            fila.append(flat_solution[r * n + c])
        grid.append(fila)
    return grid

def imprimir_puzzle(grid, titulo="Puzzle"):
    if grid is None:
        print(f"\n{titulo}: Sin solucion!")
        return

    print(f"\n{titulo}:")
    for fila in grid:
        partes = []
        for pieza in fila:
            partes.append(f"({pieza[IZQ]} {pieza[DER]} {pieza[ARR]} {pieza[ABJ]})")
        print("  " + " ".join(partes))

def imprimir_visual(grid, titulo="Puzzle"):
    if grid is None:
        print(f"\n{titulo}: Sin solucion!")
        return

    print(f"\n{titulo}:")
    n = len(grid)

    for r in range(n):
        linea_top = ""
        for c in range(n):
            linea_top += f"   {grid[r][c][ARR]}   "
            if c < n - 1:
                linea_top += "|"
        print("  " + linea_top)

        linea_mid = ""
        for c in range(n):
            linea_mid += f" {grid[r][c][IZQ]}   {grid[r][c][DER]} "
            if c < n - 1:
                linea_mid += "|"
        print("  " + linea_mid)

        linea_bot = ""
        for c in range(n):
            linea_bot += f"   {grid[r][c][ABJ]}   "
            if c < n - 1:
                linea_bot += "|"
        print("  " + linea_bot)

        if r < n - 1:
            print("  " + ("-------+" * (n - 1)) + "-------")

def verificar_solucion(grid):
    if grid is None:
        return False

    n = len(grid)
    errores = 0

    for r in range(n):
        for c in range(n):
            if c + 1 < n:
                if grid[r][c][DER] != grid[r][c + 1][IZQ]:
                    print(f"  X Horizontal ({r},{c})->({r},{c+1}): "
                          f"{grid[r][c][DER]} != {grid[r][c+1][IZQ]}")
                    errores += 1
            if r + 1 < n:
                if grid[r][c][ABJ] != grid[r + 1][c][ARR]:
                    print(f"  X Vertical ({r},{c})->({r+1},{c}): "
                          f"{grid[r][c][ABJ]} != {grid[r+1][c][ARR]}")
                    errores += 1

    if errores == 0:
        print("  [OK] Solucion valida — todas las restricciones satisfechas.")
    else:
        print(f"  [FAIL] {errores} restriccion(es) violada(s).")

    return errores == 0

def generar_puzzle(n, max_val=9):
    grid = [[None for _ in range(n)] for _ in range(n)]

    for r in range(n):
        for c in range(n):
            izq    = random.randint(0, max_val)
            der    = random.randint(0, max_val)
            arriba = random.randint(0, max_val)
            abajo  = random.randint(0, max_val)

            if c > 0:
                izq = grid[r][c - 1][DER]
            if r > 0:
                arriba = grid[r - 1][c][ABJ]

            grid[r][c] = (izq, der, arriba, abajo)

    piezas = [grid[r][c] for r in range(n) for c in range(n)]
    random.shuffle(piezas)

    puzzle = []
    for r in range(n):
        fila = []
        for c in range(n):
            fila.append(piezas[r * n + c])
        puzzle.append(fila)
    return puzzle

def leer_puzzle_manual(n):
    print(f"\nIngrese las {n * n} piezas del puzzle {n}x{n}.")
    print("Formato por pieza: izquierda derecha arriba abajo")
    print("Ejemplo: 7 0 6 4\n")

    piezas = []
    for i in range(n * n):
        while True:
            try:
                entrada = input(f"  Pieza {i + 1}: ").strip()
                valores = tuple(int(x) for x in entrada.split())
                if len(valores) != 4:
                    print("    -> Error: ingrese exactamente 4 numeros.")
                    continue
                piezas.append(valores)
                break
            except ValueError:
                print("    -> Error: ingrese numeros enteros validos.")
    puzzle = []
    for r in range(n):
        fila = []
        for c in range(n):
            fila.append(piezas[r * n + c])
        puzzle.append(fila)
    return puzzle

def menu_principal():
    print()
    print("=" * 65)
    print("  TETRAVEX SOLVER — miniKanren (Declarativo Optimizado)")
    print("  Representacion del Conocimiento y Razonamiento")
    print("  Taller 1 — Universidad de Tarapaca, 1/2026")
    print("=" * 65)

    ultimos_resultados = None

    while True:
        print("\n  +-------------------------------------------+")
        print("  |            MENU PRINCIPAL                  |")
        print("  +-------------------------------------------+")
        print("  |  1. Generar y resolver puzzle aleatorio     |")
        print("  |  2. Ingresar puzzle manualmente             |")
        print("  |  3. Salir                                   |")
        print("  +-------------------------------------------+")

        opcion = input("\n  Seleccione una opcion: ").strip()

        # ── 1: Puzzle aleatorio ──
        if opcion == "1":
            print("\n  Tamano del tablero:")
            print("    a) 2x2  (4 piezas)")
            print("    b) 3x3  (9 piezas)")
            print("    c) 4x4  (16 piezas)")
            print("    d) 5x5  (25 piezas)")
            tam = input("  Seleccione: ").strip().lower()

            mapa_tam = {'a': 2, 'b': 3, 'c': 4, 'd': 5}
            if tam not in mapa_tam:
                print("  Opcion no valida.")
                continue

            n = mapa_tam[tam]
            print(f"\n  Generando puzzle aleatorio {n}x{n}...")
            puzzle_input = generar_puzzle(n)
            puzzle_dict = crear_puzzle(puzzle_input)

            imprimir_puzzle(puzzle_input, f"Puzzle generado ({n}x{n})")

            print(f"\n  Resolviendo...")
            inicio = time.time()
            solucion = solve_tetravex(puzzle_dict)
            t = time.time() - inicio

            if solucion:
                imprimir_puzzle(solucion, "Solucion")
                imprimir_visual(solucion, "Solucion (visual)")
                print(f"\n  Tiempo: {t:.4f} segundos")
                verificar_solucion(solucion)
            else:
                print(f"\n  No se encontro solucion. Tiempo: {t:.4f}s")

        # ── 2: Puzzle manual ──
        elif opcion == "2":
            print("\n  Tamano del tablero:")
            print("    a) 2x2  (4 piezas)")
            print("    b) 3x3  (9 piezas)")
            print("    c) 4x4  (16 piezas)")
            print("    d) 5x5  (25 piezas)")
            tam = input("  Seleccione: ").strip().lower()

            mapa_tam = {'a': 2, 'b': 3, 'c': 4, 'd': 5}
            if tam not in mapa_tam:
                print("  Opcion no valida.")
                continue

            n = mapa_tam[tam]
            puzzle_input = leer_puzzle_manual(n)
            puzzle_dict = crear_puzzle(puzzle_input)

            imprimir_puzzle(puzzle_input, f"Puzzle ingresado ({n}x{n})")

            print(f"\n  Resolviendo...")
            inicio = time.time()
            solucion = solve_tetravex(puzzle_dict)
            t = time.time() - inicio

            if solucion:
                imprimir_puzzle(solucion, "Solucion")
                imprimir_visual(solucion, "Solucion (visual)")
                print(f"\n  Tiempo: {t:.4f} segundos")
                verificar_solucion(solucion)
            else:
                print(f"\n  No se encontro solucion en {t:.4f}s")
                print("  Verifique que las piezas sean correctas.")

        # ── 3: Salir ──
        elif opcion == "3":
            print("\n  Hasta luego!\n")
            break

        else:
            print("  Opcion no valida.")

if __name__ == "__main__":
    menu_principal()
