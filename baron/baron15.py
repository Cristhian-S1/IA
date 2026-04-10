from kanren import *
from logicpuzzles import *

ring1 = (1100, var(), var())
ring2 = (1200, var(), var())
ring3 = (1300, var(), var())
ring4 = (1400, var(), var())
rings = (ring1, ring2, ring3, ring4)

def restrictions(rings):
    return lall(
        #
        lany(
            membero( (var(),"virginia","opalo"), rings ),
            eq( ring3[2], "opalo" )
        ), neq(ring3, (1300, "virginia", "opalo")),

        #
        somewhat_left_of( rings, (var(),var(),"zafiro"), (var(),var(),"amatista") ),

        #
        left_of( rings, (var(),"opal",var()), (var(),var(),"opalo"), 2),

        #
        right_of( rings, (var(),"opal",var()), (var(),"lorraine",var()) ),

        #
        eq( ring1[2], "ruby" ),

        #Dominios
        membero( (var(),var(),"ruby"), rings ),
        
        membero( (var(),"rebecca",var()), rings ),
        membero( (var(),"virginia",var()), rings )
    )

results = run(0, rings, restrictions(rings))

for result in results:
    print(result)
