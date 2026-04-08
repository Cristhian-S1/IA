from kanren import *
from kanren.constraints import neq

# amigo(nombre, bebida)
amigo1 = ('Alberto', var())
amigo2 = ('Berta', var())
amigo3 = ('Carlos', var())
amigos = (amigo1, amigo2, amigo3)

def teproblem(amigos):
    return lall(
        # 1. Cada uno de ellos pide te o cafe
        membero(amigo1[1], ['te', 'cafe']),
        membero(amigo2[1], ['te', 'cafe']),
        membero(amigo3[1], ['te', 'cafe']),

        # 2. Si Alberto pide cafe, entonces Berta pide lo mismo que Carlos 
        lany(neq(amigo1[1], 'cafe'), eq(amigo2[1], amigo3[1])),
        
        # 3. Si Berta pide cafe, entonces Alberto pide la bebida que no pide Carlos
        lany(neq(amigo2[1], 'cafe'), neq(amigo1[1], amigo3[1])),
        
        # 4. Si Carlos pide te, entonces Alberto pide la misma bebida que Berta
        lany(neq(amigo3[1], 'te'), eq(amigo1[1], amigo2[1])),
        )

solutions = run(0, amigos, teproblem(amigos))

# Todas las soluciones (mundos) posibles
print('Todas las soluciones posibles: ')
for i, s in enumerate(solutions, start=1):      
    print('{}. {}'.format(i,s))
print()

# Quien siempre pide la misma bebida (en todos los mundos posibles)
# Estrategia: Se crea un conjunto (a) para cada uno de los estados posibles de cada amigo (i) 
# en cada solucion encontrada (s).
# Se verifica que todos los estados sean el mismo: len(set(a)) == 1

print('¿Quén pide siempre lo mismo?: ')
for a in [[s[i] for s in solutions] for i in (0,1,2)]:
    if len(set(a)) == 1:
        print(set(a))