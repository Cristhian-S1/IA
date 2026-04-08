# https://logic.puzzlebaron.com
# origen: curso IA 2022


from logicpuzzles import *
from time import perf_counter

# Hay cuatro objetos
objeto1 = (250, var(), var())
objeto2 = (325, var(), var())
objeto3 = (400, var(), var())
objeto4 = (475, var(), var())
objetos = (objeto1, objeto2, objeto3, objeto4)

# objeto(valor, objeto, lugar)
def objectsproblem(objetos):
    return lall(
                # 1. El anillo de diamantes se vendió por 75 dólares más que el objeto encontrado en Heffen Lane.
                right_of(objetos, (var(), 'diamond ring', var()), (var(), var(), 'Heffen Lane')),

                # 2. El objeto encontrado en Heffen Lane se vendió por 150 dólares menos que la pieza encontrada en Front Beach.
                left_of(objetos, (var(), var(), 'Heffen Lane'), (var(), var(), 'Front Beach'), 2),

                # 3. La cadena de oro se vendió por algo más que la pieza encontrada en Burr Woods.
                somewhat_right_of(objetos, (var(), 'gold chain', var()), (var(), var(), 'Burr Woods')),

                # 4. El reloj de pulsera fue el artículo que se vendió por $475 o el objeto que se vendió por $250.
                lany(eq((475, 'wristwatch', var()), objeto4), eq((250, 'wristwatch', var()), objeto1)),

                # 5. De la bala de cañón y el artículo que se vendió por $475, uno se encontró en Dimmot Woods y el otro en Front Beach.
                conde((membero((var(), 'cannonball', 'Dimmot Woods'), objetos), eq((475, var(), 'Front Beach'), objeto4)), ((membero((var(), 'cannonball', 'Front Beach'), objetos), eq((475, var(), 'Dimmot Woods'), objeto4)))),
        )

start = perf_counter()
solutions = run(0, objetos, objectsproblem(objetos))
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)