# https://logic.puzzlebaron.com
# origen: curso IA 2022


from logicpuzzles import *
from time import perf_counter

# Hay cuatro podcast
podcast1 = ('1 million', var(), var())
podcast2 = ('2 million', var(), var())
podcast3 = ('3 million', var(), var())
podcast4 = ('4 million', var(), var())
podcasts = (podcast1, podcast2, podcast3, podcast4)

# podcast(descargas, anfitrion, año)
def podcastproblem(podcasts):
    return lall(
        # 1. Del show de Bobby Bora y el show de Al Acosta, uno tiene 2 millones de descargas y el otro comenzo en 2014.
        conde((eq(('2 million', 'Bobby Bora', var()), podcast2), membero((var(), 'Al Acosta', 2014), podcasts)), (membero((var(), 'Bobby Bora', 2014), podcasts), eq(('2 million', 'Al Acosta', var()), podcast2))),

        # 2. El podcast de Al Acosta es el podcast con 3 millones de descargas o el programa que comenzo en 2009.
        lany(eq(('3 million', 'Al Acosta', var()), podcast3), membero((var(), 'Al Acosta', 2009), podcasts)),
        neq(('3 million', 'Al Acosta', 2009), podcast3),

        # 3. El programa que comenzó en 2009 tiene 1 millón de descargas más que el podcast que comenzo en 2013.
        right_of(podcasts, (var(), var(), 2009), (var(), var(), 2013)),

        # 4. El show de Bobby Bora comenzo en 2009.
        membero((var(), 'Bobby Bora', 2009), podcasts),

        # 5. El podcast de Geneva Gold tiene mas descargas que el programa de Bobby Bora.
        somewhat_right_of(podcasts, (var(), 'Geneva Gold', var()), (var(), 'Bobby Bora', var())),

        # 6. Valores en los dominios faltantes
        membero((var(), 'Dixie Dean', var()), podcasts),
        membero((var(), var(), 2010), podcasts),
        )

start = perf_counter()
solutions = run(0, podcasts, podcastproblem(podcasts))
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)