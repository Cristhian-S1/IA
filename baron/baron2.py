from kanren import *
from kanren.constraints import neq
from logicpuzzles import *

#pieces count, subjects, techniques
piece1 = (150, var(), var())
piece2 = (200, var(), var())
piece3 = (250, var(), var())
piece4 = (300, var(), var())
pieces = (piece1,piece2,piece3,piece4)

def restriction1(list_p):
    # 1. La obra floral utiliza la técnica del grabado.
    return membero((var(),"floral","grabado"), list_p)
def restriction2(list_p):
    # 2. La obra con motivos de la fauna tiene 
    # 50 piezas más que la ventana con retratos.
    return right_of(list_p, (var(),"fauna",var()), (var(),"retrato",var()))
def restriction3():
    # 3. La obra compuesta por 150 piezas, la obra 
    # geométrica y el panel grabado eran todas ventanas diferentes.
    return lall(
        neq(piece1, (var(), "geometrica", var())),
        neq(piece1, (var(), var(), "grabado"))
    )
def restriction4():
    # 4. La obra con acabado arenado era o bien 
    # la obra compuesta por 300 piezas o bien la ventana geométrica.
    arena = (var(), var(), "arenado") 
    return lany(
        eq(arena, piece4),
        eq(arena, (var(), "geometrica", var()))
    ) 
def restriction5():
    # 5. El panel compuesto por 150 piezas utiliza la técnica del plomo.
    return membero(piece1, (var(), var(),"plomo" ))
def restos(list_p):
    return lall(
        membero( (var(), var(), "pintado"), list_p),
    )
def restrictions(list_p):
    return lall(
        restriction1(list_p), restriction2(list_p),
        restriction3(),restriction4(),
        restriction5(), restos(list_p)
    )
result = run(0, pieces, restrictions(pieces))

print(result)