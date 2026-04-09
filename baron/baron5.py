from kanren import *
from logicpuzzles import *

#months, witnesses, locations
avistamiento1 = ("march",var(),var())
avistamiento2 = ("april",var(),var())
avistamiento3 = ("may",var(),var())
avistamiento4 = ("june",var(),var())
avistamientos = (avistamiento1, avistamiento2, avistamiento3, avistamiento4)

def restrictions(avistamientos):
    return lall(

        #1. El avistamiento de Ida tuvo lugar en Twin Pines.
        #1. Ida's sighting took place at Twin Pines.
        membero( (var(),"ida","twin_pines"), avistamientos ),

        #2. El relato de Peggy tuvo lugar en Bald Hill Run.
        #2. Peggy's account took place at Bald Hill Run.
        membero( (var(),"peggy","bald_hill_run"), avistamientos ),

        #3. El relato de Juniper Springs tuvo lugar un mes antes del suceso de Ada.
        #3. The account at Juniper Springs took place 1 month before Ada's event.
        left_of(avistamientos, (var(),var(),"juniper_springs"),(var(),"ada",var()),1),

        #4. El relato de Ida fue el de Bald Hill Run o el de mayo.
        #4. Ida's account was either the account at Bald Hill Run or the May account.
        eq(avistamiento3[1], "ida"),

        #dominios
        membero( (var(), "bobbie",var()), avistamientos ),
        membero( (var(), var(), "seryl_forest"), avistamientos )
    )


result = run(0,avistamientos, restrictions(avistamientos))
print(result)