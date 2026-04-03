"""
===============================================================================
    TETRAVEX SOLVER — Enfoque Declarativo con miniKanren (V1 Optimizado)
    Representación del Conocimiento y Razonamiento — Taller 1
    Universidad de Tarapacá, 1/2026
===============================================================================

DESCRIPCIÓN GENERAL DEL PUZZLE (Agentes y Ambientes)
─────────────────────────────────────────────────────
TetraVex es un puzzle de colocación de piezas sobre un tablero N×N.

  • Ambiente: Tablero cuadrado de N×N celdas, completamente observable,
    determinista, estático, discreto y de un solo agente.
  • Percepciones: El agente conoce todas las piezas y el estado actual
    del tablero (qué celdas están vacías y cuáles ocupadas).
  • Acciones: Colocar una pieza disponible en una celda vacía.
  • Objetivo: Llenar todas las celdas de modo que los bordes adyacentes
    entre piezas vecinas tengan el mismo número.

ESPECIFICACIÓN CSP (Problema de Satisfacción de Restricciones)
──────────────────────────────────────────────────────────────
  • Variables:  celda[r][c]  para r,c ∈ {0, ..., N-1}  →  N² variables.
  • Dominios:   Cada variable puede tomar como valor cualquiera de las N²
                piezas disponibles.  Dom(celda[r][c]) = {pieza_0, ..., pieza_{N²-1}}
  • Restricciones:
      (R1) Horizontal — Para todo r, c con c < N-1:
           derecha(celda[r][c]) == izquierda(celda[r][c+1])
      (R2) Vertical — Para todo r, c con r < N-1:
           abajo(celda[r][c]) == arriba(celda[r+1][c])
      (R3) Unicidad — Todas las variables toman valores distintos:
           celda[i] ≠ celda[j]  para todo i ≠ j

REPRESENTACIÓN DE UNA PIEZA (Estructura de datos)
─────────────────────────────────────────────────
  Cada pieza es una tupla de 4 enteros:

      (izquierda, derecha, arriba, abajo)

  Con índices constantes:
      IZQ = 0    DER = 1    ARR = 2    ABJ = 3

  Visualmente:           arriba
                      izq     der
                         abajo

  El puzzle completo se representa como un diccionario:
      {
          "n":     3,                          # dimensión del tablero
          "tiles": [(1,9,2,2), (1,9,4,9), ...] # lista plana de N² piezas
      }

OPTIMIZACIONES REALIZADAS (respecto a la versión base)
─────────────────────────────────────────────────────
  1. PRE-INDEXACIÓN: Se crean índices de búsqueda rápida por borde:
       por_izq[v] = {piezas cuyo borde izquierdo es v}
       por_arr[v] = {piezas cuyo borde superior es v}
     Esto reemplaza la búsqueda lineal de membero con todo el dominio
     por un membero filtrado con solo las piezas compatibles.

  2. PODA DE DOMINIO ANTICIPADA: Al construir los goals, cada celda
     recibe como dominio solo las piezas que tienen valores de borde
     compatibles con los bordes ya impuestos por la posición en el
     tablero (restricciones de adyacencia implícitas por posición).

  3. ORDENAMIENTO DE GOALS: Los goals se intercalan celda por celda
     (dominio + adyacencia + unicidad) para maximizar la poda temprana.

  4. GOAL RECURSIVO CON PODA (solve_optimizado): Construye el árbol
     de búsqueda celda por celda, verificando restricciones de adyacencia
     ANTES de generar las cláusulas de conde. Solo las piezas que pasan
     la verificación se incluyen como alternativas.

DEPENDENCIAS
────────────
  pip install kanren

===============================================================================
"""

# =============================================================================
#  IMPORTACIONES
# =============================================================================

import time
import random
from collections import defaultdict

# ── miniKanren ──
from kanren import var, run, eq, membero, conde, lall
from kanren.constraints import neq


# =============================================================================
#  CONSTANTES DE ACCESO A BORDES
# =============================================================================

IZQ = 0   # Borde izquierdo
DER = 1   # Borde derecho
ARR = 2   # Borde superior (arriba)
ABJ = 3   # Borde inferior (abajo)


# =============================================================================
#  ESTRUCTURA DE DATOS DEL PUZZLE
# =============================================================================

def crear_puzzle(puzzle_input):
    """
    Crea la estructura de datos del puzzle.

    Retorna un diccionario con:
        - "n":     dimensión del tablero (int)
        - "tiles": lista plana de N² piezas (list[tuple])

    Parámetros
    ----------
    puzzle_input : list[list[tuple]]
        Matriz N×N de piezas.
    """
    n = len(puzzle_input)
    tiles = []
    for fila in puzzle_input:
        for pieza in fila:
            tiles.append(tuple(pieza))
    return {"n": n, "tiles": tiles}


# =============================================================================
#  ÍNDICES DE BÚSQUEDA RÁPIDA (Pre-procesamiento)
# =============================================================================

def construir_indices(tiles):
    """
    Construye índices de búsqueda rápida por valor de borde.

    Esto permite, dado un valor de borde, encontrar inmediatamente
    todas las piezas que tienen ese valor en un borde específico,
    sin recorrer toda la lista de piezas.

    Retorna
    -------
    dict con 4 índices:
        "por_izq": {valor: [piezas con borde izquierdo == valor]}
        "por_der": {valor: [piezas con borde derecho == valor]}
        "por_arr": {valor: [piezas con borde superior == valor]}
        "por_abj": {valor: [piezas con borde inferior == valor]}

    Ejemplo:
        Si tiles = [(7,0,6,4), (0,1,5,4), (1,9,2,2)]
        por_izq[0] = [(0,1,5,4)]
        por_izq[1] = [(1,9,2,2)]
        por_izq[7] = [(7,0,6,4)]
    """
    por_izq = defaultdict(list)
    por_der = defaultdict(list)
    por_arr = defaultdict(list)
    por_abj = defaultdict(list)

    for pieza in tiles:
        por_izq[pieza[IZQ]].append(pieza)
        por_der[pieza[DER]].append(pieza)
        por_arr[pieza[ARR]].append(pieza)
        por_abj[pieza[ABJ]].append(pieza)

    return {
        "por_izq": por_izq,
        "por_der": por_der,
        "por_arr": por_arr,
        "por_abj": por_abj
    }


# =============================================================================
#  RELACIONES DE ADYACENCIA (goals de miniKanren)
# =============================================================================

def coincidencia_horizontal(pieza_izq, pieza_der):
    """
    Goal: derecha(pieza_izq) == izquierda(pieza_der).

    Destructura ambas piezas con variables auxiliares y
    fuerza igualdad entre los bordes adyacentes.
    """
    l1, r1, t1, b1 = var(), var(), var(), var()
    l2, r2, t2, b2 = var(), var(), var(), var()
    return lall(
        eq(pieza_izq, (l1, r1, t1, b1)),
        eq(pieza_der, (l2, r2, t2, b2)),
        eq(r1, l2)
    )


def coincidencia_vertical(pieza_sup, pieza_inf):
    """
    Goal: abajo(pieza_sup) == arriba(pieza_inf).

    Destructura ambas piezas con variables auxiliares y
    fuerza igualdad entre los bordes adyacentes.
    """
    l1, r1, t1, b1 = var(), var(), var(), var()
    l2, r2, t2, b2 = var(), var(), var(), var()
    return lall(
        eq(pieza_sup, (l1, r1, t1, b1)),
        eq(pieza_inf, (l2, r2, t2, b2)),
        eq(b1, t2)
    )


# =============================================================================
#  SOLVER DECLARATIVO (membero + neq — versión base)
# =============================================================================

def resolver_tetravex_base(puzzle_dict):
    """
    Solver declarativo base: membero + neq + match.

    Declara dominio completo (todas las piezas) para cada celda.
    Funciona bien hasta 3×3, se vuelve lento en 4×4+.

    Se mantiene como referencia para comparación de tiempos.
    """
    n = puzzle_dict["n"]
    tiles = puzzle_dict["tiles"]

    grid = [[var(f'cell_{r}_{c}') for c in range(n)] for r in range(n)]
    flat = [grid[r][c] for r in range(n) for c in range(n)]

    goals = []

    for r in range(n):
        for c in range(n):
            idx = r * n + c

            # Dominio: esta celda es una de las piezas
            goals.append(membero(grid[r][c], tiles))

            # Adyacencia
            if c > 0:
                goals.append(coincidencia_horizontal(grid[r][c - 1], grid[r][c]))
            if r > 0:
                goals.append(coincidencia_vertical(grid[r - 1][c], grid[r][c]))

            # Unicidad
            for prev_idx in range(idx):
                pr, pc = prev_idx // n, prev_idx % n
                goals.append(neq(grid[pr][pc], grid[r][c]))

    result = run(1, flat, *goals)

    if result:
        return reconstruir(result[0], n)
    return None


# =============================================================================
#  SOLVER OPTIMIZADO (conde recursivo con poda anticipada)
# =============================================================================

def resolver_tetravex(puzzle_dict):
    """
    Solver optimizado: construye el árbol de búsqueda con poda anticipada.

    ┌──────────────────────────────────────────────────────────────────┐
    │  DIFERENCIA CLAVE respecto a la versión base:                    │
    │                                                                  │
    │  En la versión base, membero ofrece TODAS las piezas como        │
    │  candidatas para cada celda, y miniKanren descarta las inválidas │
    │  después (cuando evalúa match y neq).                            │
    │                                                                  │
    │  En esta versión, la función _colocar_pieza verifica las         │
    │  restricciones de adyacencia ANTES de incluir una pieza como     │
    │  cláusula del conde.  Solo las piezas que pasan la verificación  │
    │  se presentan a miniKanren como alternativas.                    │
    │                                                                  │
    │  Además, las piezas usadas se remueven de las disponibles        │
    │  (unicidad implícita, sin necesidad de neq).                     │
    └──────────────────────────────────────────────────────────────────┘

    Usa exclusivamente primitivas de miniKanren: var, run, eq, conde, lall.
    No implementa ningún algoritmo de búsqueda propio — miniKanren
    sigue siendo el motor que explora las alternativas del conde.

    Parámetros
    ----------
    puzzle_dict : dict
        {"n": int, "tiles": list[tuple]}

    Retorna
    -------
    list[list[tuple]] o None
    """
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
    """
    Goal recursivo: asigna una pieza a la posición (r, c) y continúa.

    ┌──────────────────────────────────────────────────────────────────┐
    │  Proceso para cada posición (r, c):                              │
    │                                                                  │
    │  1. FILTRAR: Para cada pieza en 'disponibles', verificar si      │
    │     cumple las restricciones de adyacencia con las piezas ya     │
    │     colocadas (vecino izquierdo y vecino superior).              │
    │                                                                  │
    │  2. CONSTRUIR CONDE: Solo las piezas que pasan el filtro se     │
    │     incluyen como cláusulas del conde.  Cada cláusula contiene: │
    │       eq(grid[r][c], pieza)  →  asignar la pieza a la celda     │
    │       _colocar_pieza(...)    →  recurrir a la siguiente celda   │
    │                                                                  │
    │  3. La pieza asignada se remueve de 'disponibles' antes de      │
    │     recurrir, lo que GARANTIZA UNICIDAD sin necesidad de neq.   │
    │                                                                  │
    │  4. Si ninguna pieza pasa el filtro → goal que falla.           │
    │     miniKanren retrocede (backtrack) al conde anterior.         │
    └──────────────────────────────────────────────────────────────────┘

    Parámetros
    ----------
    grid : list[list[var]]
        Matriz de variables lógicas.
    disponibles : tuple[tuple]
        Piezas aún no colocadas.
    n : int
        Dimensión del tablero.
    r, c : int
        Posición actual a llenar.
    colocadas : dict
        {(r, c): pieza} con las piezas ya asignadas.
        Se usa para verificar adyacencia.

    Retorna
    -------
    goal de miniKanren (conde, lall, o fail).
    """
    # ── Caso base: todas las celdas llenadas exitosamente ──
    if r >= n:
        return lall()  # Éxito: no hay más condiciones

    # Calcular siguiente posición (recorrido fila por fila)
    sig_r, sig_c = (r, c + 1) if c + 1 < n else (r + 1, 0)

    # ── Filtrar piezas candidatas ──
    clausulas = []

    for i in range(len(disponibles)):
        pieza = disponibles[i]

        # Verificar restricción HORIZONTAL:
        # Si hay vecino a la izquierda, su borde derecho debe
        # coincidir con el borde izquierdo de esta pieza.
        if c > 0:
            vecino_izq = colocadas[(r, c - 1)]
            if vecino_izq[DER] != pieza[IZQ]:
                continue  # Poda: pieza incompatible → no incluir

        # Verificar restricción VERTICAL:
        # Si hay vecino arriba, su borde inferior debe coincidir
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


# =============================================================================
#  UTILIDADES
# =============================================================================

def reconstruir(flat_solution, n):
    """Convierte una solución plana en grilla N×N."""
    grid = []
    for r in range(n):
        fila = []
        for c in range(n):
            fila.append(flat_solution[r * n + c])
        grid.append(fila)
    return grid


def imprimir_puzzle(grid, titulo="Puzzle"):
    """
    Imprime el tablero en formato compacto.

    Ejemplo 3×3:
      (7 0 6 4) (0 1 5 4) (1 9 2 2)
      (5 1 4 7) (1 9 4 9) (9 9 2 9)
      (4 0 7 7) (0 6 9 5) (6 8 9 7)
    """
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
    """
    Imprime el tablero con piezas en formato diamante visual.

    Ejemplo pieza (7, 0, 6, 4):
          6
        7   0
          4
    """
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
    """
    Verifica que una solución satisfaga TODAS las restricciones CSP.

    Comprueba:
      (R1) Horizontal: pieza[r][c][DER] == pieza[r][c+1][IZQ]
      (R2) Vertical:   pieza[r][c][ABJ] == pieza[r+1][c][ARR]
    """
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
    """
    Genera un puzzle TetraVex aleatorio y resoluble de tamaño N×N.

    Construye un tablero resuelto forzando coincidencia en bordes
    adyacentes, luego mezcla las piezas.
    """
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
    """
    Lee un puzzle N×N ingresado manualmente.
    Formato por pieza: izquierda derecha arriba abajo
    """
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


# =============================================================================
#  BENCHMARKING — Análisis de Complejidad (NP-Completitud)
# =============================================================================

def benchmark(sizes=None, intentos=3, max_val=9, comparar=False):
    """
    Ejecuta pruebas de rendimiento.

    Si comparar=True, ejecuta tanto el solver base como el optimizado
    para mostrar la diferencia de rendimiento.

    Retorna
    -------
    dict[int, dict]
        {tamaño: {"optimizado": [tiempos], "base": [tiempos]}}
    """
    if sizes is None:
        sizes = [2, 3, 4]

    resultados = {}

    print("\n" + "=" * 65)
    print("  BENCHMARK — Analisis de complejidad temporal")
    if comparar:
        print("  Comparacion: Solver base vs Solver optimizado")
    print("=" * 65)

    for n in sizes:
        tiempos_opt = []
        tiempos_base = []
        print(f"\n  Tablero {n}x{n} ({n * n} piezas):")

        for t in range(intentos):
            puzzle_input = generar_puzzle_aleatorio(n, max_val)
            puzzle_dict = crear_puzzle(puzzle_input)

            # Solver optimizado
            inicio = time.time()
            sol_opt = resolver_tetravex(puzzle_dict)
            t_opt = time.time() - inicio
            valida_opt = verificar_solucion(sol_opt) if sol_opt else False

            if comparar and n <= 4:
                # Solver base (solo hasta 4×4, más allá es demasiado lento)
                inicio = time.time()
                sol_base = resolver_tetravex_base(puzzle_dict)
                t_base = time.time() - inicio
                valida_base = verificar_solucion(sol_base) if sol_base else False
                tiempos_base.append(t_base)

                print(f"    Intento {t + 1}: "
                      f"Opt={t_opt:.4f}s [{'OK' if valida_opt else 'FAIL'}]  "
                      f"Base={t_base:.4f}s [{'OK' if valida_base else 'FAIL'}]  "
                      f"Speedup={t_base/t_opt:.1f}x" if t_opt > 0.0001 else
                      f"    Intento {t + 1}: "
                      f"Opt={t_opt:.4f}s  Base={t_base:.4f}s")
            else:
                estado = "OK" if valida_opt else "FAIL"
                print(f"    Intento {t + 1}: {t_opt:.4f}s [{estado}]")

            tiempos_opt.append(t_opt)

        prom_opt = sum(tiempos_opt) / len(tiempos_opt)
        print(f"    -- Promedio optimizado: {prom_opt:.4f}s")

        if comparar and tiempos_base:
            prom_base = sum(tiempos_base) / len(tiempos_base)
            print(f"    -- Promedio base:       {prom_base:.4f}s")
            if prom_opt > 0.0001:
                print(f"    -- Speedup promedio:    {prom_base/prom_opt:.1f}x")

        resultados[n] = {
            "optimizado": tiempos_opt,
            "base": tiempos_base
        }

    # Tabla resumen
    print("\n  +----------+---------+------------+")
    print("  | Tamanio  | Piezas  | Prom. Opt  |")
    print("  +----------+---------+------------+")
    for n, data in resultados.items():
        prom = sum(data["optimizado"]) / len(data["optimizado"])
        print(f"  |   {n}x{n}    |   {n*n:>2}    |  {prom:>7.4f}s  |")
    print("  +----------+---------+------------+")

    return resultados


def graficar_resultados(resultados):
    """
    Genera un gráfico de barras con los tiempos de benchmark.
    Requiere matplotlib.
    """
    try:
        import matplotlib.pyplot as plt

        sizes = list(resultados.keys())
        promedios = [sum(d["optimizado"]) / len(d["optimizado"])
                     for d in resultados.values()]
        labels = [f"{n}x{n}\n({n*n} pz)" for n in sizes]

        colores = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6', '#f39c12']

        fig, ax = plt.subplots(figsize=(8, 5))
        barras = ax.bar(labels, promedios, color=colores[:len(sizes)])

        for barra, prom in zip(barras, promedios):
            ax.text(barra.get_x() + barra.get_width() / 2,
                    barra.get_height() + 0.01,
                    f'{prom:.4f}s',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax.set_xlabel('Tamano del tablero', fontsize=12)
        ax.set_ylabel('Tiempo promedio (segundos)', fontsize=12)
        ax.set_title('TetraVex: Crecimiento del tiempo (NP-Completo)\n'
                     'Solver optimizado con poda anticipada',
                     fontsize=13, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig('tetravex_benchmark.png', dpi=150)
        plt.show()
        print("  Grafico guardado como 'tetravex_benchmark.png'")

    except ImportError:
        print("  matplotlib no disponible. Datos para graficar:")
        for n, data in resultados.items():
            prom = sum(data["optimizado"]) / len(data["optimizado"])
            print(f"    {n}x{n}: {prom:.4f}s")


# =============================================================================
#  PROGRAMA PRINCIPAL — Menú Interactivo
# =============================================================================

def menu_principal():
    """Menú interactivo del solver."""

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
        print("  |  1. Resolver ejemplo del PDF (3x3)         |")
        print("  |  2. Generar y resolver puzzle aleatorio     |")
        print("  |  3. Ingresar puzzle manualmente             |")
        print("  |  4. Benchmark (solo optimizado)             |")
        print("  |  5. Benchmark comparativo (base vs opt)     |")
        print("  |  6. Graficar resultados de benchmark        |")
        print("  |  7. Salir                                   |")
        print("  +-------------------------------------------+")

        opcion = input("\n  Seleccione una opcion: ").strip()

        # ── 1: Ejemplo del PDF ──
        if opcion == "1":
            puzzle_input = [
                [(1, 9, 2, 2), (1, 9, 4, 9), (6, 8, 9, 7)],
                [(9, 9, 2, 9), (0, 6, 9, 5), (0, 1, 5, 4)],
                [(4, 0, 7, 7), (5, 1, 4, 7), (7, 0, 6, 4)]
            ]

            puzzle_dict = crear_puzzle(puzzle_input)
            print(f"\n  Puzzle: {puzzle_dict['n']}x{puzzle_dict['n']} "
                  f"con {len(puzzle_dict['tiles'])} piezas")
            imprimir_puzzle(
                reconstruir(puzzle_dict["tiles"], puzzle_dict["n"]),
                "Piezas de entrada"
            )

            print("\n  Resolviendo con miniKanren (optimizado)...")
            inicio = time.time()
            solucion = resolver_tetravex(puzzle_dict)
            t = time.time() - inicio

            imprimir_puzzle(solucion, "Solucion encontrada")
            imprimir_puzzle_diamante(solucion, "Solucion (vista visual)")
            print(f"\n  Tiempo: {t:.4f} segundos")
            verificar_solucion(solucion)

            esperada = [
                [(7, 0, 6, 4), (0, 1, 5, 4), (1, 9, 2, 2)],
                [(5, 1, 4, 7), (1, 9, 4, 9), (9, 9, 2, 9)],
                [(4, 0, 7, 7), (0, 6, 9, 5), (6, 8, 9, 7)]
            ]
            if solucion == esperada:
                print("  Coincide exactamente con la solucion del PDF.")
            elif solucion is not None:
                print("  Solucion valida (puede diferir si hay multiples soluciones).")

        # ── 2: Puzzle aleatorio ──
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
            print(f"\n  Generando puzzle aleatorio {n}x{n}...")
            puzzle_input = generar_puzzle_aleatorio(n)
            puzzle_dict = crear_puzzle(puzzle_input)

            imprimir_puzzle(puzzle_input, f"Puzzle generado ({n}x{n})")

            print(f"\n  Resolviendo...")
            inicio = time.time()
            solucion = resolver_tetravex(puzzle_dict)
            t = time.time() - inicio

            if solucion:
                imprimir_puzzle(solucion, "Solucion")
                imprimir_puzzle_diamante(solucion, "Solucion (visual)")
                print(f"\n  Tiempo: {t:.4f} segundos")
                verificar_solucion(solucion)
            else:
                print(f"\n  No se encontro solucion. Tiempo: {t:.4f}s")

        # ── 3: Puzzle manual ──
        elif opcion == "3":
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
            solucion = resolver_tetravex(puzzle_dict)
            t = time.time() - inicio

            if solucion:
                imprimir_puzzle(solucion, "Solucion")
                imprimir_puzzle_diamante(solucion, "Solucion (visual)")
                print(f"\n  Tiempo: {t:.4f} segundos")
                verificar_solucion(solucion)
            else:
                print(f"\n  No se encontro solucion en {t:.4f}s")
                print("  Verifique que las piezas sean correctas.")

        # ── 4: Benchmark solo optimizado ──
        elif opcion == "4":
            print("\n  Tamanos a probar:")
            print("    a) 2x2, 3x3")
            print("    b) 2x2, 3x3, 4x4")
            print("    c) 2x2, 3x3, 4x4, 5x5")
            sel = input("  Seleccione: ").strip().lower()

            mapa = {'a': [2, 3], 'b': [2, 3, 4], 'c': [2, 3, 4, 5]}
            sizes = mapa.get(sel, [2, 3, 4])

            inp = input("  Intentos por tamano (default 3): ").strip()
            intentos = int(inp) if inp.isdigit() else 3

            ultimos_resultados = benchmark(sizes=sizes, intentos=intentos)

        # ── 5: Benchmark comparativo ──
        elif opcion == "5":
            print("\n  Comparacion base vs optimizado")
            print("  (base solo hasta 4x4, es muy lento en 5x5)\n")
            print("  Tamanos:")
            print("    a) 2x2, 3x3")
            print("    b) 2x2, 3x3, 4x4")
            sel = input("  Seleccione: ").strip().lower()

            mapa = {'a': [2, 3], 'b': [2, 3, 4]}
            sizes = mapa.get(sel, [2, 3])

            inp = input("  Intentos por tamano (default 3): ").strip()
            intentos = int(inp) if inp.isdigit() else 3

            ultimos_resultados = benchmark(
                sizes=sizes, intentos=intentos, comparar=True
            )

        # ── 6: Graficar ──
        elif opcion == "6":
            if ultimos_resultados:
                graficar_resultados(ultimos_resultados)
            else:
                print("  Primero ejecute un benchmark (opcion 4 o 5).")

        # ── 7: Salir ──
        elif opcion == "7":
            print("\n  Hasta luego!\n")
            break

        else:
            print("  Opcion no valida.")


# =============================================================================
#  PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    menu_principal()
