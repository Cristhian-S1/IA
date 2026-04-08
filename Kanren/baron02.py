# https://logic.puzzlebaron.com/play.php?u2=8acf8fd20e0aad8567638347a3555df9

from logicpuzzles import *
from time import perf_counter

# Hay cuatro animales
animal1 = (15000, var(), var())
animal2 = (16500, var(), var())
animal3 = (18000, var(), var())
animal4 = (19500, var(), var())
animales = (animal1, animal2, animal3, animal4)

# animal(nombre, ubicacion)
def oceananimals(animales):
    return lall(
    # 1. The specimen found at 15,000 ft is either the bristlemouth or the specimen discovered in the Willis Trench.
        lany(eq((15000, 'bristlemouth', var()), animal1), eq((15000, var(), 'Willis Trench'), animal1)),
        neq((1500, 'bristlemouth', 'Willis Trench'), animal1),

    # 2. The anglerfish was found at 18,000 ft.
        eq((18000,'anglerfish', var()), animal3),
    
    # 3. The bristlemouth was found 1,500 feet higher up than the specimen discovered in the Fallon Deep.
        left_of(animales, (var(), 'bristlemouth', var()), (var(), var(), 'Fallon Deep')),
    
    # 4. The specimen discovered in the Zini Trench was found somewhat lower down than the anglerfish.
        somewhat_right_of(animales, (var(), var(), 'Zini Trench'), (var(), 'anglerfish', var())),
    
    # 5. The lancetfish was found at 15,000 ft.
        eq((15000, 'lancetfish', var()), animal1),
    
    # 6. otros valores de los dominios
        membero((var(), 'viperfish', var()), animales),
        membero((var(), var(),'Malinga Trench'), animales)
        )

start = perf_counter()
solutions = run(0, animales, oceananimals(animales))
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)
