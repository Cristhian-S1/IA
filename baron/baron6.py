from kanren import *
from logicpuzzles import *

universidad1 = (525, var(), var())
universidad2 = (550, var(), var())
universidad3 = (575, var(), var())
universidad4 = (600, var(), var())
universidades = (universidad1,universidad2,universidad3,universidad4)

def restrictions(universidades):
    return lall(
        #1. The car with a high speed of 62 MPH drove 50 fewer miles than the Cober.
        #1. El automóvil con una velocidad máxima de 62 millas por hora recorrió 50 millas menos que el Cober.
        left_of(universidades, (var(),var(),62), (var(),"cober",var()), 2),

        #2. The Leden had a high speed of 62 MPH.
        #2. El Leden tenía una velocidad máxima de 62 millas por hora.
        membero( (var(),"leden",62), universidades ),

        #3. The automobile with a high speed of 65 MPH drove somewhat farther than the Cober.
        #3. El automóvil con una velocidad máxima de 65 millas por hora recorrió una distancia algo mayor que el Cober.
        somewhat_right_of(universidades, (var(),var(),65), (var(),"cober",var())),
        ##Inferencia Cober recorrio 575 y tiene un velocidad de 67 o 74

        #4. The car with a high speed of 67 MPH drove somewhat farther than the Garusky.
        #4. El automóvil con una velocidad máxima de 67 millas por hora recorrió una distancia algo mayor que el Garusky.
        somewhat_right_of(universidades, (var(),var(),67), (var(), "garusky", var())),
        #Inferencia Garusky recorrio 525 o 550

        #dominio
        membero((var(),"poltris",var()), universidades),
        membero((var(),var(),74), universidades)
    )

results = run(0, universidades, restrictions(universidades))
for v in results:
    print(v)
