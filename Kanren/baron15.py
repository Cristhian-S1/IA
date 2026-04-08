# https://logic.puzzlebaron.com
# 4x7
# Challenging

# Julia ha contratado a varias personas nuevas para que trabajen como administradores de atracciones
# para el parque de atracciones Walton World. Necesita verificar sus resultados después de su primer
# día completo de trabajo. Ayúdela a relacionar a cada nuevo empleado con su paseo y sección del parque
# (desglosados ​​por color), así como la cantidad de personas a las que atendió durante ese día.

# Solución:
# (((50, 'Herbert', 'Loop-D-Loop', 'red'), 
#   (75, 'Andy', 'The Breaker', 'green'), 
#   (100, 'Orlando', 'The Screamer', 'yellow'), 
#   (125, 'Sergio', 'Speed Devil', 'orange'), 
#   (150, 'Lyle', 'Agony Alley', 'blue'), 
#   (175, 'Isaac', 'Demon Drop', 'pink'), 
#   (200, 'Chris', 'Zinjo', 'purple')),)
#
# Tiempo: 1270.0976487000007 [segundos]
#

from logicpuzzles import *
from time import perf_counter

# Hay siete empleados
empleado1 = ( 50, var(), var(), var())
empleado2 = ( 75, var(), var(), var())
empleado3 = (100, var(), var(), var())
empleado4 = (125, var(), var(), var())
empleado5 = (150, var(), var(), var())
empleado6 = (175, var(), var(), var())
empleado7 = (200, var(), var(), var())
empleados = (empleado1, empleado2, empleado3, empleado4, empleado5, empleado6, empleado7)

# empleado(visitantes, nombre, juego, seccion)
def peopleproblem(planetas):
    return lall(
            # 1. De Herbert y el empleado que atendió a 175 pasajeros, uno administra Loop-D-Loop y 
            # el otro administra Demon Drop.
            conde((membero((var(), 'Herbert', 'Loop-D-Loop', var()), empleados), eq((175, var(), 'Demon Drop', var()), empleado6)),
                  (membero((var(), 'Herbert', 'Demon Drop', var()), empleados), eq((175, var(), 'Loop-D-Loop', var()), empleado6))),
            
            # 2. El trabajador que administra Agony Alley atendió a 25 pasajeros menos que la persona que administra Demon Drop.
            left_of(empleados, (var(), var(), 'Agony Alley', var()), (var(), var(), 'Demon Drop', var())),

            # 3. Del empleado que trabaja en la sección azul y la persona que maneja Demon Drop, uno atendió a 150 visitantes y el otro es Isaac.
            conde((eq((150, var(), var(), 'blue'), empleado5), membero((var(), 'Isaac', 'Demon Drop', var()), empleados)),
                  (membero((var(), var(), 'Isaac', 'blue'), empleados), eq((150, var(), 'Demon Drop', var()), empleado5))),
            neq((150, 'Isaac', 'Demon Drop', 'blue'), empleado5),

            # 4. Del empleado que dirige The Breaker e Isaac, uno atendió a 75 visitantes y el otro trabaja en la sección rosa.
            conde((eq((75, var(), 'The Breaker', var()), empleado2), membero((var(), 'Isaac', var(), 'pink'), empleados)),
                  (membero((var(), var(), 'The Breaker', 'pink'), empleados), eq((75, 'Isaac', var(), var()), empleado2))),
            neq((75, 'Isaac', 'The Breaker', 'pink'), empleado5),

            # 5. La persona que administra Agony Alley atendió a menos pasajeros que Chris.
            somewhat_left_of(empleados, (var(), var(), 'Agony Alley', var()), (var(), 'Chris', var(), var())),

            # 6. El trabajador que gestiona The Screamer trabaja en la sección amarilla.
            membero((var(), var(), 'The Screamer', 'yellow'), empleados),

            # 7. Andy es el trabajador que administra Demon Drop o el trabajador que trabaja en la sección verde.
            lany(membero((var(), 'Andy', 'Demon Drop', var()), empleados), membero((var(), 'Andy', var(), 'green'), empleados)),

            # 8. El empleado que trabaja en la sección naranja es Herbert o la persona que atendió a 125 visitantes.
            lany(membero((var(), 'Herbert', var(), 'orange'), empleados), eq((125, var(), var(), 'orange'), empleado4)),
            neq((125, 'Herbert', 'orange'), tuple(empleado4[i] for i in (0, 1, 3))),

            # 9. La persona que administra The Screamer atendió a más pasajeros que el empleado que trabaja en la sección roja.
            somewhat_right_of(empleados, (var(), var(), 'The Screamer', var()), (var(), var(), var(), 'red')),

            # 10. El empleado que atendió a 100 pasajeros trabaja en la sección amarilla.
            eq((100, var(), var(), 'yellow'), empleado3),

            # 13. El trabajador que trabaja en la sección amarilla atendió a menos visitantes que Sergio.
            somewhat_left_of(empleados, (var(), var(), var(), 'yellow'), (var(), 'Sergio', var(), var())),

            # 15. Valores en los dominios faltantes
            membero((var(), 'Lyle', var(), var()) ,empleados),
            membero((var(), 'Orlando', var(), var()) ,empleados),
            membero((var(), var(), 'Speed Devil', var()) ,empleados),
            membero((var(), var(), 'Zinjo', var()) ,empleados),
            membero((var(), var(), var(), 'purple') ,empleados),          
            )

start = perf_counter()
solutions = run(0, empleados, peopleproblem(empleados),
                # 11. Lyle no trabaja en la sección amarilla.
                nmembero(empleados, ('Lyle', 'yellow'), (1,3)),           

                # 12. Ni el trabajador que trabaja en la sección rosa ni el empleado que trabaja en la sección naranja es Lyle.
                nmembero(empleados, ('Lyle', 'pink'), (1,3)), 
                nmembero(empleados, ('Lyle', 'orange'), (1,3)),

                # 14. Los siete empleados son la persona que dirige Speed ​​Devil, Herbert, 
                # el empleado que trabaja en la sección amarilla, el empleado que atendió a 200 visitantes, 
                # la persona que trabaja en la sección rosa, el empleado que trabaja en la sección azul y 
                # la persona que trabaja en la sección verde.
                differents(empleados, ((200,), ('Herbert',), ('Speed Devil',), ('yellow', 'pink', 'blue', 'green',)))
            )
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)
