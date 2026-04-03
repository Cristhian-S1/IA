import time
from v1_tetravex import (
    crear_puzzle, resolver_tetravex, imprimir_puzzle, imprimir_puzzle_diamante,
    verificar_solucion, generar_puzzle_aleatorio, leer_puzzle_manual,
    benchmark, graficar_resultados
)

"""Menú interactivo con opciones para el Tetravex"""
print()
print("=" * 65)
print("  Tetravex con MiniKanren")
print("=" * 65)

while True:
    print("\n  +-------------------------------------------+")
    print("  |            MENU PRINCIPAL                  |")
    print("  +-------------------------------------------+")
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

        print(f"\n  Resolviendo con miniKanren...")
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

        print(f"\n  Resolviendo con miniKanren...")
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

    elif opcion == "3":
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
