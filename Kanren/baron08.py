# https://logic.puzzlebaron.com
# origen: curso IA 2022

# Un grupo de apoyo local para aerófobos (aquellos que le tienen miedo a los vuelos) 
# tiene varios miembros que necesitan tomar un vuelo. Haga coincidir cada aerófobo 
# con su fecha de vuelo y destino, y determine qué “amuleto de la suerte” tiene la 
# intención de llevar cada uno.

from logicpuzzles import *
from time import perf_counter

# Hay cuatro aerófobos
aerofobo1 = ('January', var(), var())
aerofobo2 = ('February', var(), var())
aerofobo3 = ('March', var(), var())
aerofobo4 = ('April', var(), var())
aerofobos = (aerofobo1, aerofobo2, aerofobo3, aerofobo4)

# aerofobo(mes, nombre, amuleto)
def flyersproblem(aerofobos):
    return lall(
        #1. Yolanda es la aerófoba que se va en enero o la pasajera con la espoleta.
        lany(eq(('January', 'Yolanda', var()), aerofobo1), membero((var(), 'Yolanda', 'Espoleta'), aerofobos)),
        neq(('January', 'Yolanda', 'Espoleta'), aerofobo1),

        #3. El aerófobo con la moneda se irá 1 mes antes que Katie.
        left_of(aerofobos, (var(), var(), 'Moneda'), (var(), 'Katie', var())),

        #4. El viajero que sale en abril traerá su pata de conejo.
        eq(('April', var(), 'Pata de Conejo'), aerofobo4),

        #5. El aerófobo con el talismán saldrá 1 mes después que el pasajero con la moneda.
        right_of(aerofobos, (var(), var(), 'Talisman'), (var(), var(), 'Moneda')),

        #6. Datos no mencionados
        membero((var(), 'Yolanda', var()), aerofobos),
        membero((var(), 'Troy', var()), aerofobos),
        membero((var(), 'Neal', var()), aerofobos),
        membero((var(), var(), 'Espoleta'), aerofobos)
    )

start = perf_counter()
solutions = run(0, aerofobos, flyersproblem(aerofobos),
#2. Los cuatro voladores son; el aerófobo que se va en enero, Troy, Katie y el pasajero con la pata de conejo
                differents(aerofobos, (('January',), ('Troy', 'Katie',), ('Pata de Conejo',)))
    )
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)