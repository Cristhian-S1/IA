# https://logic.puzzlebaron.com
# origen: curso IA 2022


from logicpuzzles import *
from time import perf_counter

# Hay cuatro monitos
monito1 = (4, var(), var())
monito2 = (7, var(), var())
monito3 = (10, var(), var())
monito4 = (13, var(), var())
monitos = (monito1, monito2, monito3, monito4)

# monito(edad, nombre, cuidador)
def monkeyproblem(monitos):
    return lall(
        # 1. Quirrell es el animal con el que trabaja Dolly O es el de 13 años.
        lany(membero((var(), 'Quirrell', 'Dolly'), monitos), eq((13, 'Quirrell', var()), monito4)),
        neq((13, 'Quirrell', 'Dolly'), monito4),

        # 2. El mono de 13 años es cuidado por Gracie.
        eq((13, var(), 'Gracie'), monito4),
        
        # 3. Rajesh tiene 13 años.
        eq((13, 'Rajesh', var()), monito4),

        # 4. Pemson es mas viejo que el mono cuidado por Beatrice. 
        somewhat_right_of(monitos, (var(), 'Pemson', var()), (var(), var(), 'Beatrice') ),

        # 5. El mono de 7 años es cuidado por Dolly o Rajesh
        lany(eq((7, var(), 'Dolly'), monito2), eq((7, var(), 'Rajesh'), monito2)),

        # 6. Valores en los dominios faltantes
        membero((var(), 'Nikatrice', var()), monitos),
        membero((var(), var(), 'Aldo'), monitos)
    )

start = perf_counter()
solutions = run(0,monitos,monkeyproblem(monitos))
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)