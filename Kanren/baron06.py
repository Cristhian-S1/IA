# https://logic.puzzlebaron.com
# origen: curso IA 2022

# Se ha anunciado un premio que otorga 50 millones de dólares a la primera compañía privada
# en enviar con éxito una sonda a Neptuno. Usando las pistas, se debe emparejar a cada compañía
# con su cohete y país de origen y determinar el mes en que se lanzará su sonda.

from logicpuzzles import *
from time import perf_counter

# Hay cinco sondas
sonda1 = ('January', var(), var(), var())
sonda2 = ('February', var(), var(), var())
sonda3 = ('March', var(), var(), var())
sonda4 = ('April', var(), var(), var())
sonda5 = ('May', var(), var(), var())
sondas = (sonda1, sonda2, sonda3, sonda4, sonda5)

#sonda(mes, nombre, compañia, pais)
def sondasproblem(sondas):
    return lall(
        # 1. El cohete lanzado por Irán será lanzado 2 meses después que Dreadco.
        right_of(sondas, (var(), var(), var(), 'Iran'), (var(), 'Dreadco', var(), var()), 2),

        # 2. Del cohete desarrollado por Techtrin y el cohete que se lanzará en Marzo, uno es de Irán y el otro es Exatris.
        conde((membero((var(), var(), 'Techtrin', 'Iran'), sondas), eq(('March', 'Exatris', var(), var()), sonda3)),
              (membero((var(), 'Exatris', 'Techtrin', var()), sondas), eq(('March', var(), var(), 'Iran'), sonda3))),
        neq(('March', 'Exatris', 'Techtrin', 'Iran'), sonda3),

        # 3. Worul es de Alemania.
        membero((var(), 'Worul', var(), 'Germany'), sondas),

        # 4. El cohete de Polonia se lanzará en algún momento antes del cohete desarrollado por Ubersplore.
        somewhat_left_of(sondas, (var(), var(), var(), 'Poland'), (var(), var(), 'Ubersplore', var())),

        # 5. El cohete de Costa Rica está hecho por Vexatech.
        membero((var(), var(), 'Vexatech', 'Costa Rica'), sondas),

        # 6. El cohete desarrollado por SpaceZen se lanzará 1 mes después del cohete desarrollado por Ubersplore
        right_of(sondas, (var(), var(), 'SpaceZen', var()), (var(), var(), 'Ubersplore', var())),
        
        # 7. El cohete desarrollado por Vexatech es el Worul o el Athios.
        lany(membero((var(), 'Worul', 'Vexatech', var()), sondas), membero((var(), 'Athios', 'Vexatech', var()), sondas)),
    
        # 8. El Athios no se lanzará en Mayo.
        neq(('May', 'Athios'), (sonda5[0], sonda5[1])),

        # 10. datos no mencionados
        membero((var(), 'Athios', var(), var()), sondas),
        membero((var(), 'Exatris', var(), var()), sondas),
        membero((var(), 'Gralax', var(), var()), sondas),
        membero((var(), var(), 'Permias', var()), sondas),
        membero((var(), var(), 'Techtrin', var()), sondas),
        membero((var(), var(), var(), 'Rusia'), sondas)
    )

start = perf_counter()
solutions = run(0, sondas, sondasproblem(sondas),
            
# 9. Los cinco cohetes son el cohete desarrollado por Ubersplore, el cohete de Costa Rica, el cohete que se lanzará en Enero, el Exatris, y el cohete de Irán.
                differents(sondas, (('January',), ('Exatris',), ('Ubersplore',), ('Costa Rica', 'Iran',))),
            )
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)