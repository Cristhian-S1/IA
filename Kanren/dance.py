from kanren import *
from kanren.constraints import neq

#para fijar el orden de las parejas
ballroom = ((var(),'red'), (var(),'green'), (var(),'blue'))

#todas las parejas son de distinto color
def differents(ballroom):
    return lall(neq(d1,d2) for d1,d2 in ballroom)

#el baile
def dance(ballroom):
    return lall(
        membero(('red','green'), ballroom),
        membero(('green',var()), ballroom),
        membero(('blue',var()), ballroom),
        differents(ballroom)
        )

solution = run(0,ballroom, dance(ballroom))

print(solution)
