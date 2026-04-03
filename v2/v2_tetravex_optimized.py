import random
import time
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

def coincidencia_horizontal(pieza_izq, pieza_der):
    l1, r1, t1, b1 = var(), var(), var(), var()
    l2, r2, t2, b2 = var(), var(), var(), var()
    return lall(
        eq(pieza_izq, (l1, r1, t1, b1)),
        eq(pieza_der, (l2, r2, t2, b2)),
        eq(r1, l2)
    )

def coincidencia_vertical(pieza_sup, pieza_inf):
    l1, r1, t1, b1 = var(), var(), var(), var()
    l2, r2, t2, b2 = var(), var(), var(), var()
    return lall(
        eq(pieza_sup, (l1, r1, t1, b1)),
        eq(pieza_inf, (l2, r2, t2, b2)),
        eq(b1, t2)
    )

def resolver_tetravex(puzzle_dict):
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
        return reconstruir(result[0], n)
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

def reconstruir(flat_solution, n):
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

def imprimir_puzzle_diamante(grid, titulo="Puzzle"):
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

def generar_puzzle_aleatorio(n, max_val=9):
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

def benchmark(sizes=None, intentos=3, max_val=9):
    if sizes is None:
        sizes = [2, 3, 4]
    resultados = {}

    print("\n" + "=" * 65)
    print("  BENCHMARK — Analisis de complejidad temporal")
    print("=" * 65)

    for n in sizes:
        tiempos = []
        print(f"\n  Tablero {n}x{n} ({n * n} piezas):")

        for t in range(intentos):
            puzzle_input = generar_puzzle_aleatorio(n, max_val)
            puzzle_dict = crear_puzzle(puzzle_input)

            inicio = time.time()
            solucion = resolver_tetravex(puzzle_dict)
            transcurrido = time.time() - inicio

            valida = verificar_solucion(solucion) if solucion else False
            estado = "OK" if valida else "FAIL"
            print(f"    Intento {t + 1}: {transcurrido:.4f}s [{estado}]")
            tiempos.append(transcurrido)

        promedio = sum(tiempos) / len(tiempos)
        resultados[n] = tiempos
        print(f"    -- Promedio: {promedio:.4f}s")

    # Tabla resumen
    print("\n  +----------+---------+----------+----------+")
    print("  | Tamanio  | Piezas  | Promedio | Maximo   |")
    print("  +----------+---------+----------+----------+")
    for n, tiempos in resultados.items():
        prom = sum(tiempos) / len(tiempos)
        maxi = max(tiempos)
        print(f"  |   {n}x{n}    |   {n*n:>2}    | {prom:>6.4f}s | {maxi:>6.4f}s |")
    print("  +----------+---------+----------+----------+")

    return resultados

def graficar_resultados(resultados):
    try:
        import matplotlib.pyplot as plt

        sizes = list(resultados.keys())
        promedios = [sum(t) / len(t) for t in resultados.values()]
        labels = [f"{n}x{n}\n({n*n} pz)" for n in sizes]

        colores = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6']

        fig, ax = plt.subplots(figsize=(8, 5))
        barras = ax.bar(labels, promedios, color=colores[:len(sizes)])

        for barra, prom in zip(barras, promedios):
            ax.text(barra.get_x() + barra.get_width() / 2,
                    barra.get_height() + 0.01,
                    f'{prom:.4f}s',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax.set_xlabel('Tamano del tablero', fontsize=12)
        ax.set_ylabel('Tiempo promedio (segundos)', fontsize=12)
        ax.set_title('TetraVex: Crecimiento del tiempo de resolucion\n'
                     '(Comportamiento NP-Completo)',
                     fontsize=13, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig('tetravex_benchmark.png', dpi=150)
        plt.show()
        print("  Grafico guardado como 'tetravex_benchmark.png'")

    except ImportError:
        print("  matplotlib no disponible. Datos para graficar:")
        for n, tiempos in resultados.items():
            prom = sum(tiempos) / len(tiempos)
            print(f"    {n}x{n}: {prom:.4f}s")
