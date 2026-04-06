import time
from logica_kanren import crear_puzzle, resolver_tetravex
from funciones_misc import (
    tetravex_aleatorio,verificar_solucion
)

def benchmark(tamanio=None, intentos=3, valor_maximo_ficha=9):
    if tamanio is None:
        tamanio = [2, 3, 4]

    resultados = {}

    print("\n" + "=" * 65)
    print("  BENCHMARK — Analisis de complejidad temporal")
    print("=" * 65)

    for n in tamanio:
        tiempos = []
        print(f"\n  Tablero {n}x{n} ({n * n} piezas):")

        for t in range(intentos):
            tetravex_2d = tetravex_aleatorio(n, valor_maximo_ficha)
            tetravex_dict = crear_puzzle(tetravex_2d)

            inicio = time.time()
            solucion = resolver_tetravex(tetravex_dict)
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

        tamanio = list(resultados.keys())
        promedios = [sum(t) / len(t) for t in resultados.values()]
        etiqueta = [f"{n}x{n}\n({n*n} pz)" for n in tamanio]

        colores = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6']

        fig, ax = plt.subplots(figsize=(8, 5))
        barras = ax.bar(etiqueta, promedios, color=colores[:len(tamanio)])

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
