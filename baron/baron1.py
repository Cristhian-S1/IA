from kanren import run, var, eq, membero, lany, lall
from kanren.constraints import neq
from logicpuzzles import *

# year, golfers, scores
golfer1 = (1920, var(), var())
golfer2 = (1921, var(), var())
golfer3 = (1922, var(), var())
golfer4 = (1923, var(), var())
golfers = (golfer1,golfer2,golfer3,golfer4)

def restriccion1(golfers):
    # 1. Denise Detz ganó su torneo en algún momento 
    # anterior a la golfista que obtuvo un 60.
    # somewhat_left_of(golfers, (var(), var(), (60)), (var(), "Denise", var()))
    return somewhat_left_of(golfers, (var(), "Denise", var()), (var(), var(), 60))

def restriccion2(golfers):
    #2. Denise Detz logró un 59.
    # eq( (var(), "Denise", var()), (var(), var(), 59) )
    return membero( (var(), "Denise", 59), golfers )

def restriccion3():
    # 3. Denise Detz, Bonita Bitz y la persona
    # que ganó en 1921 eran todas golfistas diferentes.
    return lall(
        neq(golfer2[1], "Denise"),
        neq(golfer2[1], "Bonita"),
    )

def restriccion4(golfers):
    # 4. La persona que obtuvo un 61 ganó su torneo
    #  en algún momento posterior a Bonita Bitz.
    golfer_61 = (var(), var(), 61)
    bonita = (var(), "Bonita", var())
    return somewhat_right_of( golfers, golfer_61, bonita)

def restriccion5(golfers):
    # 5. Nellie Nolan ganó su torneo 
    # en algún momento anterior a Denise Detz.
    nellie = (var(),"Nellie",var())
    denise = (var(), "Denise", var())
    return somewhat_left_of(golfers, nellie, denise)

def nombres_unicos():
    return lall(
        neq(golfer1[1], golfer2[1]),
        neq(golfer1[1], golfer3[1]),
        neq(golfer1[1], golfer4[1]),
        neq(golfer2[1], golfer3[1]),
        neq(golfer2[1], golfer4[1]),
        neq(golfer3[1], golfer4[1]),
    )

def restos():
    bonita = (var(),"Bonita",var())
    denise = (var(),"Denise",var())
    shari  = (var(),"Shari",var())
    return lall(
        membero(bonita, (golfer1,golfer3)),
        membero(denise, (golfer3, golfer4)),
        membero(shari,  golfers),
        membero( (var(),var(),60), golfers ),
        membero( (var(),var(),67), golfers )
     )

def restricciones(golfers):
    return lall(restriccion1(golfers),restriccion2(golfers),restriccion3(),restriccion4(golfers),restriccion5(golfers), restos(), nombres_unicos())

result = run(0, golfers, restricciones(golfers))
print(result)