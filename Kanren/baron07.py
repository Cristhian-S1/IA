# https://logic.puzzlebaron.com
# origen: curso IA 2022

# Un notorio ladrón de arte, finalmente ha sido capturado. Mientras buscaban en su casa, 
# los investigadores descubrieron un tesoro oculto de pinturas perdidas hace mucho tiempo, 
# cada una de un artista famoso diferente. Usando las pistas, empareje cada pintura con su
# artista y el diseño en que fue pintada, y determine cuántos años ha estado desaparecida
# cada pieza de valor.

from logicpuzzles import *
from time import perf_counter

# Hay cuatro pinturas

pintura1 = (1987, var(), var(), var())
pintura2 = (1905, var(), var(), var())
pintura3 = (1913, var(), var(), var())
pintura4 = (1921, var(), var(), var())
pinturas = (pintura1, pintura2, pintura3, pintura4)

#pintura(año, nombre, artista, desaparecida)
def paintsproblem(pinturas):
    return lall(
        # 1.La pieza que ha estado desaparecida durante 13 años fue pintada 8 años después de la obra maestra de Zhale.
        right_of(pinturas, (var(), var(), var(), 13), (var(), var(), 'Zhale', var())),

        # 2. La pieza de 1921 es "Clockwork".
        eq(pintura4, (1921, 'Clockwork', var(), var())),

        # 3. El cuadro de Curo Cersal es "Willow Bend".
        membero((var(), 'Willow Bend', 'Curo Cersal', var()), pinturas),

        # 4. De la pieza de Curo Cersal y "Lost in time", una lleva 20 años desaparecida y la otra 19 años.
        conde((membero((var(), var(), 'Curo Cersal', 20), pinturas), membero((var(), 'Lost in time', var(), 19), pinturas)),
              (membero((var(), var(), 'Curo Cersal', 19), pinturas), membero((var(), 'Lost in time', var(), 20), pinturas))),

        # 6. La pintura que ha estado desaparecida durante 19 años fue pintada 8 años después de "Tantrum".
        right_of(pinturas, (var(), var(), var(), 19), (var(), 'Tantrum', var(), var())),

        # 7. Datos no mencionados
        membero((var(), var(), "Dray D'Amici", var()), pinturas),
        membero((var(), var(), "Fuji Fukiro", var()), pinturas),
        membero((var(), var(), var(), 10), pinturas)
    )

start = perf_counter()
solutions = run(0, pinturas, paintsproblem(pinturas),
#5- La pintura de Fuji Fukiro, la pintura de 1905 y la pintura que ha estado desaparecida durante 13 años son tres pinturas diferentes.
            differents(pinturas, ((1905,), (var(),), ('Fuji Fukiro',), (13,)))
    )
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)
