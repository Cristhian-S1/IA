"""
===============================================================================
    TETRAVEX SOLVER — Enfoque Declarativo con miniKanren (Solver V1)
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

  Ejemplo: (7, 0, 6, 4) →      6
                              7   0
                                4

  El puzzle completo se representa como un diccionario:
      {
          "n":     3,                          # dimensión del tablero
          "tiles": [(1,9,2,2), (1,9,4,9), ...] # lista plana de N² piezas
      }

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

# ── miniKanren ──
# var:     Crea una variable lógica (una incógnita).
# run:     Ejecuta el motor de búsqueda y devuelve soluciones.
# eq:      Unificación — fuerza que dos términos sean iguales.
# membero: Relación de pertenencia — x ∈ lista.
# conde:   Disyunción (OR) — al menos una de las cláusulas debe cumplirse.
# lall:    Conjunción (AND) — todas las metas deben cumplirse.
from kanren import var, run, eq, membero, conde, lall

# neq: Desigualdad — dos términos NO deben ser iguales.
# Es una restricción (constraint) que se propaga durante la búsqueda.
from kanren.constraints import neq


# =============================================================================
#  CONSTANTES DE ACCESO A LOS BORDES DE UNA PIEZA
# =============================================================================
# Cada pieza es una tupla (izquierda, derecha, arriba, abajo).
# Estas constantes hacen el código más legible:
#     pieza[IZQ] en lugar de pieza[0]

IZQ = 0   # Borde izquierdo
DER = 1   # Borde derecho
ARR = 2   # Borde superior (arriba)
ABJ = 3   # Borde inferior (abajo)


# =============================================================================
#  ESTRUCTURA DE DATOS DEL PUZZLE
# =============================================================================

def crear_puzzle(puzzle_input):
    """
    Crea la estructura de datos del puzzle a partir de la entrada.

    La estructura es un diccionario con:
        - "n":     dimensión del tablero (int)
        - "tiles": lista plana de N² piezas (list[tuple])

    Parámetros
    ----------
    puzzle_input : list[list[tuple]]
        Matriz N×N de piezas tal como se presenta al jugador.
        Ejemplo 3×3:
        [
            [(1,9,2,2), (1,9,4,9), (6,8,9,7)],
            [(9,9,2,9), (0,6,9,5), (0,1,5,4)],
            [(4,0,7,7), (5,1,4,7), (7,0,6,4)]
        ]

    Retorna
    -------
    dict
        {"n": 3, "tiles": [(1,9,2,2), (1,9,4,9), ...]}
    """
    n = len(puzzle_input)
    tiles = []
    for fila in puzzle_input:
        for pieza in fila:
            tiles.append(tuple(pieza))
    return {"n": n, "tiles": tiles}


# =============================================================================
#  RELACIONES DE ADYACENCIA (goals de miniKanren)
# =============================================================================

def match_horizontal(pieza_izq, pieza_der):
    """
    Meta (goal) de miniKanren:
        El borde DERECHO de 'pieza_izq' es igual al borde IZQUIERDO de 'pieza_der'.

    Funcionamiento paso a paso:
        1. Se crean 8 variables lógicas auxiliares (4 por pieza).
        2. eq(pieza_izq, (l1, r1, t1, b1))  →  "destructura" la pieza
           izquierda, asignando cada componente a una variable auxiliar.
        3. eq(pieza_der, (l2, r2, t2, b2))  →  destructura la pieza derecha.
        4. eq(r1, l2)  →  fuerza que derecha(izq) == izquierda(der).

    Ejemplo:
        pieza_izq = (7, 0, 6, 4)  →  r1 = 0
        pieza_der = (0, 1, 5, 4)  →  l2 = 0
        eq(0, 0) → ÉXITO ✓
    """
    l1, r1, t1, b1 = var(), var(), var(), var()
    l2, r2, t2, b2 = var(), var(), var(), var()
    return lall(
        eq(pieza_izq, (l1, r1, t1, b1)),   # Destructurar pieza izquierda
        eq(pieza_der, (l2, r2, t2, b2)),   # Destructurar pieza derecha
        eq(r1, l2)                          # Restricción R1: der(izq) == izq(der)
    )


def match_vertical(pieza_sup, pieza_inf):
    """
    Meta (goal) de miniKanren:
        El borde INFERIOR de 'pieza_sup' es igual al borde SUPERIOR de 'pieza_inf'.

    Funcionamiento:
        Igual que match_horizontal, pero compara b1 (abajo de la superior)
        con t2 (arriba de la inferior).

    Ejemplo:
        pieza_sup = (7, 0, 6, 4)  →  b1 = 4
        pieza_inf = (5, 1, 4, 7)  →  t2 = 4
        eq(4, 4) → ÉXITO ✓
    """
    l1, r1, t1, b1 = var(), var(), var(), var()
    l2, r2, t2, b2 = var(), var(), var(), var()
    return lall(
        eq(pieza_sup, (l1, r1, t1, b1)),   # Destructurar pieza superior
        eq(pieza_inf, (l2, r2, t2, b2)),   # Destructurar pieza inferior
        eq(b1, t2)                          # Restricción R2: abj(sup) == arr(inf)
    )


# =============================================================================
#  SOLVER V1:  membero + neq + match  (Declarativo puro)
# =============================================================================

def solve_tetravex(puzzle_dict):
    """
    Resuelve un puzzle TetraVex usando miniKanren de forma declarativa.

    ┌──────────────────────────────────────────────────────────────────┐
    │  Idea central:                                                   │
    │  Declarar las tres familias de restricciones del CSP como metas  │
    │  independientes de miniKanren, y dejar que el motor de búsqueda  │
    │  encuentre una asignación que las satisfaga simultáneamente.      │
    └──────────────────────────────────────────────────────────────────┘

    Paso 1 — Variables lógicas:
        Se crea una variable lógica por cada celda del tablero.
        celda[r][c] = var("cell_r_c")

    Paso 2 — Dominio (membero):
        Para cada celda, se declara que su valor pertenece al conjunto
        de piezas disponibles:
            membero(celda[r][c], lista_de_piezas)
        Internamente, membero genera un punto de elección (conde) con
        una alternativa por cada pieza de la lista.

    Paso 3 — Adyacencia (match_horizontal / match_vertical):
        Se declaran las restricciones de bordes entre celdas vecinas.
        Se colocan INMEDIATAMENTE después del membero de la celda
        correspondiente para que miniKanren pode ramas inválidas
        lo antes posible.

    Paso 4 — Unicidad (neq):
        Se declara que cada par de celdas debe tener piezas distintas:
            neq(celda[i], celda[j])  para todo i ≠ j
        neq es una restricción de desigualdad que miniKanren verifica
        incrementalmente durante la búsqueda.

    Paso 5 — Ejecución (run):
        run(1, variables, *metas)  →  busca 1 solución que satisfaga
        todas las metas simultáneamente.

    Parámetros
    ----------
    puzzle_dict : dict
        Estructura creada por crear_puzzle():
        {"n": int, "tiles": list[tuple]}

    Retorna
    -------
    list[list[tuple]] o None
        Tablero resuelto como grilla N×N, o None si no hay solución.
    """
    n = puzzle_dict["n"]
    tiles = puzzle_dict["tiles"]

    # ── Paso 1: Crear variables lógicas ──
    # Cada celda del tablero es una incógnita que miniKanren debe resolver.
    # grid[r][c] es la variable para la fila r, columna c.
    grid = [[var(f'cell_{r}_{c}') for c in range(n)] for r in range(n)]

    # Lista plana de variables para pasarla a run() como consulta
    flat = [grid[r][c] for r in range(n) for c in range(n)]

    # ── Pasos 2, 3 y 4: Construir lista de metas (goals) ──
    #
    # IMPORTANTE — Estrategia de ordenamiento:
    #   Para cada celda (recorriendo fila por fila, izquierda a derecha):
    #     a) Declarar dominio (membero)
    #     b) Declarar adyacencia con vecinos ya procesados (match)
    #     c) Declarar unicidad con todas las celdas anteriores (neq)
    #
    #   Este orden intercalado permite a miniKanren detectar
    #   inconsistencias tempranamente y podar el árbol de búsqueda.
    #   Si pusiéramos todos los membero primero, luego todos los neq,
    #   y luego todos los match, miniKanren generaría muchas más
    #   combinaciones antes de descartarlas.

    goals = []

    for r in range(n):
        for c in range(n):
            idx = r * n + c  # Índice lineal de esta celda

            # ─── (a) DOMINIO ───
            # membero(celda, piezas) equivale internamente a:
            #   conde(
            #       [eq(celda, pieza_0)],
            #       [eq(celda, pieza_1)],
            #       ...
            #       [eq(celda, pieza_{N²-1})]
            #   )
            # Esto le dice a miniKanren: "esta celda puede ser
            # cualquiera de las piezas disponibles".
            goals.append(membero(grid[r][c], tiles))

            # ─── (b) ADYACENCIA ───
            # Se añaden justo después del membero para que miniKanren
            # pueda verificar la restricción inmediatamente al elegir
            # un valor para esta celda.

            # Horizontal: derecha del vecino izquierdo == izquierda actual
            if c > 0:
                goals.append(match_horizontal(grid[r][c - 1], grid[r][c]))

            # Vertical: abajo del vecino superior == arriba actual
            if r > 0:
                goals.append(match_vertical(grid[r - 1][c], grid[r][c]))

            # ─── (c) UNICIDAD ───
            # neq(a, b) agrega una restricción de desigualdad que se
            # mantiene activa durante la búsqueda. Cuando ambas variables
            # obtienen valores concretos, miniKanren verifica que difieran.
            for prev_idx in range(idx):
                pr, pc = prev_idx // n, prev_idx % n
                goals.append(neq(grid[pr][pc], grid[r][c]))

    # ── Paso 5: Ejecutar el solver de miniKanren ──
    # run(1, flat, *goals):
    #   - 1:     buscar exactamente 1 solución
    #   - flat:  variables cuyo valor queremos conocer
    #   - goals: todas las metas que deben satisfacerse
    #
    # miniKanren explora el espacio con interleaving search,
    # probando valores de membero y verificando neq + match.
    result = run(1, flat, *goals)

    # ── Reconstruir la grilla N×N ──
    if result:
        solution = result[0]
        return reshapear(solution, n)

    return None


# =============================================================================
#  UTILIDADES
# =============================================================================

def reshapear(flat_solution, n):
    """Convierte una solución plana (tupla de N² piezas) en grilla N×N."""
    grid = []
    for r in range(n):
        fila = []
        for c in range(n):
            fila.append(flat_solution[r * n + c])
        grid.append(fila)
    return grid


def imprimir_puzzle(grid, titulo="Puzzle"):
    """
    Imprime el tablero en formato compacto de tuplas.

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


def imprimir_visual(grid, titulo="Puzzle"):
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
        # Línea superior: borde de arriba de cada pieza
        linea_top = ""
        for c in range(n):
            linea_top += f"   {grid[r][c][ARR]}   "
            if c < n - 1:
                linea_top += "|"
        print("  " + linea_top)

        # Línea media: borde izquierdo y derecho
        linea_mid = ""
        for c in range(n):
            linea_mid += f" {grid[r][c][IZQ]}   {grid[r][c][DER]} "
            if c < n - 1:
                linea_mid += "|"
        print("  " + linea_mid)

        # Línea inferior: borde de abajo
        linea_bot = ""
        for c in range(n):
            linea_bot += f"   {grid[r][c][ABJ]}   "
            if c < n - 1:
                linea_bot += "|"
        print("  " + linea_bot)

        # Separador entre filas
        if r < n - 1:
            print("  " + ("-------+" * (n - 1)) + "-------")


def verificar_solucion(grid):
    """
    Verifica que una solución satisfaga TODAS las restricciones CSP.

    Comprueba:
      (R1) Horizontal: pieza[r][c][DER] == pieza[r][c+1][IZQ]
      (R2) Vertical:   pieza[r][c][ABJ] == pieza[r+1][c][ARR]

    Retorna
    -------
    bool
        True si todas las restricciones se cumplen.
    """
    if grid is None:
        return False

    n = len(grid)
    errores = 0

    for r in range(n):
        for c in range(n):
            # R1: Horizontal
            if c + 1 < n:
                if grid[r][c][DER] != grid[r][c + 1][IZQ]:
                    print(f"  X Horizontal ({r},{c})->({r},{c+1}): "
                          f"{grid[r][c][DER]} != {grid[r][c+1][IZQ]}")
                    errores += 1

            # R2: Vertical
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
    """
    Genera un puzzle TetraVex aleatorio y resoluble de tamaño N×N.

    Estrategia:
      1. Construir un tablero resuelto: asignar bordes aleatorios,
         forzando coincidencia en bordes adyacentes.
      2. Extraer las piezas y mezclarlas aleatoriamente.
      3. Retornar como lista de listas (formato de entrada estándar).

    Parámetros
    ----------
    n : int
        Dimensión del tablero.
    max_val : int
        Valor máximo para los bordes (rango 0 a max_val).

    Retorna
    -------
    list[list[tuple]]
        Puzzle mezclado en formato de entrada.
    """
    grid = [[None for _ in range(n)] for _ in range(n)]

    for r in range(n):
        for c in range(n):
            izq    = random.randint(0, max_val)
            der    = random.randint(0, max_val)
            arriba = random.randint(0, max_val)
            abajo  = random.randint(0, max_val)

            # Forzar coincidencia con vecino izquierdo
            if c > 0:
                izq = grid[r][c - 1][DER]

            # Forzar coincidencia con vecino superior
            if r > 0:
                arriba = grid[r - 1][c][ABJ]

            grid[r][c] = (izq, der, arriba, abajo)

    # Mezclar piezas aleatoriamente
    piezas = [grid[r][c] for r in range(n) for c in range(n)]
    random.shuffle(piezas)

    # Reestructurar como lista de listas
    puzzle = []
    for r in range(n):
        fila = []
        for c in range(n):
            fila.append(piezas[r * n + c])
        puzzle.append(fila)

    return puzzle


def leer_puzzle_manual(n):
    """
    Lee un puzzle N×N ingresado manualmente por el usuario.

    Formato por pieza: cuatro enteros separados por espacio.
    Orden: izquierda derecha arriba abajo
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

def benchmark(sizes=None, intentos=3, max_val=9):
    """
    Ejecuta pruebas de rendimiento para analizar el crecimiento temporal.

    TetraVex es NP-Completo (Demaine & Demaine, 2007):
    - No se conoce algoritmo que lo resuelva en tiempo polinomial.
    - El tiempo crece exponencialmente con el tamaño del tablero.
    - Se puede verificar una solución en tiempo polinomial (clase NP).
    - Se reduce desde problemas NP-Completos conocidos.

    Parámetros
    ----------
    sizes : list[int]
        Tamaños de tablero a probar.
    intentos : int
        Número de puzzles aleatorios por tamaño (se reporta promedio).
    max_val : int
        Rango de valores en las piezas.

    Retorna
    -------
    dict[int, list[float]]
        {tamaño: [tiempo_1, tiempo_2, ...]}
    """
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
            puzzle_input = generar_puzzle(n, max_val)
            puzzle_dict = crear_puzzle(puzzle_input)

            inicio = time.time()
            solucion = solve_tetravex(puzzle_dict)
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
    """
    Genera un gráfico de barras con los tiempos de benchmark.
    Requiere matplotlib (pip install matplotlib).
    """
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


# =============================================================================
#  PROGRAMA PRINCIPAL — Menú Interactivo
# =============================================================================

def menu_principal():
    """Menú interactivo del solver."""

    print()
    print("=" * 65)
    print("  TETRAVEX SOLVER — miniKanren (Enfoque Declarativo V1)")
    print("  Representacion del Conocimiento y Razonamiento")
    print("  Taller 1 — Universidad de Tarapaca, 1/2026")
    print("=" * 65)

    # Variable para almacenar resultados del benchmark
    ultimos_resultados = None

    while True:
        print("\n  +-------------------------------------------+")
        print("  |            MENU PRINCIPAL                  |")
        print("  +-------------------------------------------+")
        print("  |  1. Resolver ejemplo del PDF (3x3)         |")
        print("  |  2. Generar y resolver puzzle aleatorio     |")
        print("  |  3. Ingresar puzzle manualmente             |")
        print("  |  4. Benchmark (analisis NP-Completo)        |")
        print("  |  5. Graficar resultados de benchmark        |")
        print("  |  6. Salir                                   |")
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
                reshapear(puzzle_dict["tiles"], puzzle_dict["n"]),
                "Piezas de entrada"
            )

            print("\n  Resolviendo con miniKanren (membero + neq + match)...")
            inicio = time.time()
            solucion = solve_tetravex(puzzle_dict)
            t = time.time() - inicio

            imprimir_puzzle(solucion, "Solucion encontrada")
            imprimir_visual(solucion, "Solucion (vista visual)")
            print(f"\n  Tiempo de resolucion: {t:.4f} segundos")
            verificar_solucion(solucion)

            # Comparar con la solución esperada del PDF
            esperada = [
                [(7, 0, 6, 4), (0, 1, 5, 4), (1, 9, 2, 2)],
                [(5, 1, 4, 7), (1, 9, 4, 9), (9, 9, 2, 9)],
                [(4, 0, 7, 7), (0, 6, 9, 5), (6, 8, 9, 7)]
            ]
            if solucion == esperada:
                print("  Coincide exactamente con la solucion del PDF.")
            elif solucion is not None:
                print("  Solucion valida (puede diferir del PDF si hay")
                print("  multiples soluciones validas).")

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
            puzzle_input = generar_puzzle(n)
            puzzle_dict = crear_puzzle(puzzle_input)

            imprimir_puzzle(puzzle_input, f"Puzzle generado ({n}x{n})")

            print(f"\n  Resolviendo con miniKanren...")
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

            print(f"\n  Resolviendo con miniKanren...")
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

        # ── 4: Benchmark ──
        elif opcion == "4":
            print("\n  Tamanos a probar:")
            print("    a) 2x2, 3x3")
            print("    b) 2x2, 3x3, 4x4")
            print("    c) 2x2, 3x3, 4x4, 5x5  (puede ser lento)")
            sel = input("  Seleccione: ").strip().lower()

            mapa = {
                'a': [2, 3],
                'b': [2, 3, 4],
                'c': [2, 3, 4, 5]
            }
            sizes = mapa.get(sel, [2, 3, 4])

            inp = input("  Numero de intentos por tamano (default 3): ").strip()
            intentos = int(inp) if inp.isdigit() else 3

            ultimos_resultados = benchmark(sizes=sizes, intentos=intentos)

        # ── 5: Graficar ──
        elif opcion == "5":
            if ultimos_resultados:
                graficar_resultados(ultimos_resultados)
            else:
                print("  Primero ejecute un benchmark (opcion 4).")

        # ── 6: Salir ──
        elif opcion == "6":
            print("\n  Hasta luego!\n")
            break

        else:
            print("  Opcion no valida. Intente de nuevo.")


# =============================================================================
#  PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    menu_principal()
