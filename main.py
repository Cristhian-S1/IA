import time
from logica_kanren import crear_puzzle, resolver_tetravex
from funciones_misc import (
    imprimir_puzzle,tetravex_aleatorio, leer_puzzle_manual,
    verificar_solucion
)
from benchmark import (benchmark, graficar_resultados)

"""Menú interactivo con opciones para el Tetravex"""
print()
print("Tetravex con MiniKanren")

ultimos_resultados = None

while True:
    print("\n  +-------------------------------------------+")
    print("  |            Menu Principal                   |")
    print("  +---------------------------------------------+")
    print("  |  1. Generar y resolver puzzle aleatorio     |")
    print("  |  2. Ingresar puzzle manualmente             |")
    print("  |  3. Benchmark                               |")
    print("  |  4. Graficar resultados de benchmark        |")
    print("  |  5. Salir                                   |")
    print("  +-------------------------------------------+")

    opcion = input("\n  Seleccione una opcion: ").strip()

    # ── 1: Puzzle aleatorio ──
    if opcion == "1":
        print("\n  Tamano del tablero:")
        print("    a) 2x2  (4 piezas)")
        print("    b) 3x3  (9 piezas)")
        print("    c) 4x4  (16 piezas)")
        print("    d) 5x5  (25 piezas)")
        tamanio_tablero = input("  Seleccione: ").strip().lower()

        tamanio_opciones = {'a': 2, 'b': 3, 'c': 4, 'd': 5}
        if tamanio_tablero not in tamanio_opciones:
            print("  Opcion no valida.")
            continue

        tamanio = tamanio_opciones[tamanio_tablero]
        print(f"\n  Generando puzzle aleatorio {tamanio}x{tamanio}...")

        # tetravex = [ [(),(),()], [(),(),()], [(),(),()] ] tetravex por fila
        tetravex_lista_lista_tupla = tetravex_aleatorio(tamanio)
        print("tetravex donde cada fila es una lista que contiene fichas tipo tupla ",tetravex_lista_lista_tupla)
        # {tamanio: 3, tetravex: [ (),(),(),(),(),(),() ]} tetravex plano
        tetravex_diccionario = crear_puzzle(tetravex_lista_lista_tupla)
        print("tetravex donde se tiene la clave del tamanio y el tablero",tetravex_diccionario)

        imprimir_puzzle(tetravex_lista_lista_tupla, f"Puzzle generado ({tamanio}x{tamanio})")

        print(f"\n  Resolviendo con miniKanren...")
        inicio = time.time()
        solucion = resolver_tetravex(tetravex_diccionario)
        t = time.time() - inicio

        if solucion:
            imprimir_puzzle(solucion, "Solucion")
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
        tamanio_tablero = input("  Seleccione: ").strip().lower()

        tamanio_opciones = {'a': 2, 'b': 3, 'c': 4, 'd': 5}
        if tamanio_tablero not in tamanio_opciones:
            print("  Opcion no valida.")
            continue

        n = tamanio_opciones[tamanio_tablero]
        tetravex_lista_lista_tupla = leer_puzzle_manual(n)
        tetravex_diccionario = crear_puzzle(tetravex_lista_lista_tupla)

        imprimir_puzzle(tetravex_lista_lista_tupla, f"Puzzle ingresado ({n}x{n})")

        print(f"\n  Resolviendo con miniKanren...")
        inicio = time.time()
        solucion = resolver_tetravex(tetravex_diccionario)
        t = time.time() - inicio

        if solucion:
            imprimir_puzzle(solucion, "Solucion")
            print(f"\n  Tiempo: {t:.4f} segundos")
            verificar_solucion(solucion)
        else:
            print(f"\n  No se encontro solucion en {t:.4f}s")
            print("  Verifique que las piezas sean correctas.")

    # ── 3: Benchmark ──
    elif opcion == "3":
        print("\n  Tamanos a probar:")
        print("    a) 2x2, 3x3")
        print("    b) 2x2, 3x3, 4x4")
        print("    c) 2x2, 3x3, 4x4, 5x5  (Demasiado lento)")
        sel = input("  Seleccione: ").strip().lower()

        mapa = {
            'a': [2, 3],
            'b': [2, 3, 4],
            'c': [2, 3, 4, 5]
        }
        tamanios = mapa.get(sel, [2, 3, 4])

        intentos_input = input("  Ingrese el numero de intentos (por defecto 3): ").strip()
        intentos = int(intentos_input) if intentos_input.isdigit() else 3

        ultimos_resultados = benchmark(tamanio=tamanios, intentos=intentos)

    # ── 4: Graficar ──
    elif opcion == "4":
        if ultimos_resultados:
            graficar_resultados(ultimos_resultados)
        else:
            print("  Primero ejecute un benchmark (opcion 4).")

    # ── 5: Salir ──
    elif opcion == "5":
        print("\n  Hasta luego!\n")
        break

    else:
        print("  Opcion no valida. Intente de nuevo.")
