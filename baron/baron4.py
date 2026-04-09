from kanren import *
from logicpuzzles import *
 
 # scores, birds, woods
 # puntos, pajaros, madera 
casa1 = (72,var(),var())
casa2 = (76,var(),var())
casa3 = (80,var(),var())
casa4 = (84,var(),var())
casas = (casa1,casa2,casa3,casa4)

def restricciones(casas):
    return lall(

        #1. La casita para pajaros para carboneros obtuvo
        # 4 puntos menos que la casita hecha de cipres
        left_of(casas, (var(),"carbonero",var()), (var(),var(),"cipres")),

        #2. La casita que obtuvo 80 puntos es para chochines
        eq( casa3[1], "cochines" ),

        #3. La casita de cedro obtuvo mas puntos que la casita de abeto
        somewhat_right_of(casas, (var(),var(),"cedro"), (var(),var(),"abeto")),

        #4. La casita de pino obtuvo 76 puntos
        eq(casa2[2], "pino"),

        #5. La casita para golondrinas era o bien la casita de cedro
        # o bien la casita de pino
        lany( 
            membero( (var(),"martin", "cedro"), casas ),
            eq(casa2, (76,"martin", var()))
         ), neq(casa2, (76,"martin","cedro")), 
        

         #Dominio pajaros
         #carbonero, martin
         membero( (var(), "cochines", var()), casas ),
         membero( (var(), "shallow", var()), casas )

         #Dominio madera
         #cipres, cedro, abeto,pino
    )

result = run(0, casas, restricciones(casas))
print(result)