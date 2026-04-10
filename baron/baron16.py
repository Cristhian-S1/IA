#CluesStoryNotesAnswers
#1. The piece with the opal is either the ring that cost $1300 or Virginia's ring.
#2. The piece with the sapphire cost less than the ring with the amethyst.
#3. Opal's ring cost 200 dollars less than the piece with the opal.
#4. Opal's piece cost 100 dollars more than Lorraine's piece.
#5. The ring that cost $1100 has the ruby.

from kanren import *
from logicpuzzles import *

# Variables para aritmética de precios (declaradas FUERA de la función)
price_opal_person = var()  # precio del anillo de la PERSONA Opal
price_opal_gem    = var()  # precio del anillo con la GEMA opal
price_sapphire    = var()  # precio del anillo con sapphire
price_amethyst    = var()  # precio del anillo con amethyst
price_lorraine    = var()  # precio del anillo de Lorraine

piece1 = (1100, var(), var())
piece2 = (1200, var(), var())
piece3 = (1300, var(), var())
piece4 = (1400, var(), var())
pieces = (piece1, piece2, piece3, piece4)

def solverProblem(pieces):
    return lall(

        # --- Dominios compradores ---
        membero((var(), 'lorraine', var()), pieces),
        membero((var(), 'opal',     var()), pieces),
        membero((var(), 'rebecca',  var()), pieces),
        membero((var(), 'virginia', var()), pieces),

        # --- Dominios gemas ---
        membero((var(), var(), 'amethyst'), pieces),
        membero((var(), var(), 'opal'),     pieces),
        membero((var(), var(), 'ruby'),     pieces),
        membero((var(), var(), 'sapphire'), pieces),

        # --- Pista 1: la gema opal cuesta 1300 O es de virginia ---
        lany(
            membero((1300, var(),      'opal'), pieces),
            membero((var(), 'virginia', 'opal'), pieces)
        ),

        # --- Pista 2: sapphire cuesta menos que amethyst ---
        membero((price_sapphire, var(), 'sapphire'), pieces),
        membero((price_amethyst, var(), 'amethyst'), pieces),
        membero(
            (price_sapphire, price_amethyst),
            [(1100,1200),(1100,1300),(1100,1400),
             (1200,1300),(1200,1400),(1300,1400)]
        ),

        # --- Pista 3: Opal cuesta 200 menos que la gema opal ---
        membero((price_opal_person, 'opal', var()), pieces),
        membero((price_opal_gem,    var(), 'opal'), pieces),
        membero(
            (price_opal_person, price_opal_gem),
            [(1100, 1300), (1200, 1400)]
        ),

        # --- Pista 4: Opal cuesta 100 más que Lorraine ---
        membero((price_lorraine, 'lorraine', var()), pieces),
        membero(
            (price_opal_person, price_lorraine),
            [(1200,1100),(1300,1200),(1400,1300)]
        ),

        # --- Pista 5: el anillo de 1100 tiene ruby ---
        eq((1100, var(), 'ruby'), piece1),
    )

solutions = run(0, pieces, solverProblem(pieces))
print(len(solutions))
for s in solutions:
    for p in s:
        print(f'  ${p[0]}: {p[1]:10} — {p[2]}')