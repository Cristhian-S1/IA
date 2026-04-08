# https://en.wikipedia.org/wiki/Zebra_Puzzle
from kanren import *

def right_of(l, p, q):
    return membero((q, p), list(zip(l, l[1:])))

def next_to(l, p, q):
    return lany(right_of(l, p, q), right_of(l, q, p))

# There are five houses
house1, house2, house3, house4, house5 = var(), var(), var(), var(), var()

houses = [house1, house2, house3, house4, house5]

# house(nac, color, pet, drink, smoke)

def zebraproblem(houses):
    return lall(
    # The Englishman lives in the red house
    membero (('Englishman', 'red', var(), var(), var()), houses),
    # The Spaniard owns the dog
    membero (('Spaniard', var(), 'dog', var(), var()), houses),
    # Coffee is drunk in the green house
    membero ((var(), 'green', var(), 'coffee', var()), houses),
    # The Ukrainian drinks tea
    membero (('Ukrainian', var(), var(), 'tea', var()), houses),
    # The green house is immediately to the right of the ivory house
    right_of(houses, 
        (var(), 'green', var(), var(), var()),
        (var(), 'ivory', var(), var(), var())),
    # The Old Gold smoker owns snails
    membero ((var(), var(), 'snails', var(), 'Old Gold'), houses),
    # Kools are smoked in the yellow house
    membero ((var(), 'yellow', var(), var(), 'Kools'), houses),
    # Milk is drunk in the middle house
    eq(house3, (var(), var(), var(), 'milk', var())),
    # The Norwegian lives in the first house
    eq(house1, ('Norwegian', var(), var(), var(), var())),
    # The man who smokes Chesterfields lives in the house next to the man with the fox
    next_to(houses,
        (var(), var(), var(), var(), 'Chesterfield'),
        (var(), var(), 'fox', var(), var())),
    # Kools are smoked in the house next to the house where he horse is kept
    next_to(houses,
        (var(), var(), var(), var(), 'Kools'),
        (var(), var(), 'horse', var(), var())),
    # The Lucky Strike smoker drinks orange juice
    membero((var(), var(), var(), 'juice', 'Lucky Strike'), houses),
    # The Japanese smokes Parliaments
    membero(('Japanese', var(), var(), var(), 'Parliament'), houses),
    # The Norwegian lives next to the blue house
    next_to(houses,
        ('Norwegian', var(), var(), var(), var()),
        (var(), 'blue', var(), var(), var())),

    # Someone drinks water, which one?
    membero((var(), var(), var(), 'water', var()), houses),
    # Someone owns a zebra, which one?
    membero((var(), var(), 'zebra', var(), var()), houses) )

solutions = run(0, houses, zebraproblem(houses))

water_drinker = [h for h in solutions[0] if 'water' in h]
zebra_keeper  = [h for h in solutions[0] if 'zebra' in h]

print("El bebedor de agua es el: {}".format(water_drinker[0][0]))
print("El dueño de la zebra es el: {}".format(zebra_keeper[0][0]))