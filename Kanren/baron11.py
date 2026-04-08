# https://logic.puzzlebaron.com
# origen: curso IA 2022


from logicpuzzles import *
from time import perf_counter

# Hay cuatro anuncios
anuncio1 = (625, var(), var())
anuncio2 = (775, var(), var())
anuncio3 = (925, var(), var())
anuncio4 = (1075, var(), var())
anuncios = (anuncio1, anuncio2, anuncio3, anuncio4)

# anuncio(respuesta, director, tipo)
def adproblem(anuncios):
    return lall(
        # 1. El anuncio de TV ha generado 1075 respuestas.
        eq((1075, var(), 'Tv commercial'), anuncio4),

        # 2. Del anuncio con 1075 respuestas y a campaña con 625 respuestas, uno es el anuncio del periodico
        # y el otro fue producido por Julie Jordan.
        conde((eq((1075, var(), 'Newspaper ad'), anuncio4), eq((625, 'Julie Jordan', var()), anuncio1)), (eq((1075, 'Julie Jordan', var()), anuncio4), eq((625, var(), 'Newspaper ad'), anuncio1))),
   
        # 3. El anuncio del periodico ha generado 150 respuestas menos que el anuncio generado por Eddie Evans
        left_of(anuncios, (var(), var(), 'Newspaper ad'), (var(), 'Eddie Evans', var())),

        # 4. El anuncio producido por Hal Hopkins ha generado menos respuestas que el anuncio generado por Iva Ingram
        somewhat_left_of(anuncios, (var(), 'Hal Hopkins', var()), (var(), 'Iva Ingram', var())),

        # 5. el anuncio de radio ha generado 925 respuestas
        eq((925, var(), 'radio spot'), anuncio3),

        # 6. Valores en los dominios faltantes
        membero((var(), var(), 'web campaign'), anuncios)
    )

start = perf_counter()
solutions = run(0, anuncios, adproblem(anuncios))
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)
