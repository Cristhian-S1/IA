# https://logic.puzzlebaron.com
# Help Dustin figure out his book store's "Best-Sellers List" by matching each book to its author, 
# and determining its page-count and number of copies sold last week.

from logicpuzzles import *
from time import perf_counter

# Hay cuatro copias
copies1 = (12, var(), var())
copies2 = (19, var(), var())
copies3 = (26, var(), var())
copies4 = (33, var(), var())
books = (copies1, copies2, copies3, copies4)

# copias(ventas, autor, titulo)
def booksproblem(books):
    return lall(
        # 1. Daniel Hansen's book sold 7 fewer copies than Call of Duty.
        left_of(books, (var(), 'Daniel Hansen', var()), (var(), var(), 'Call of Duty')),

        # 2. Call of Duty sold 19 copies.
        eq((19, var(), 'Call of Duty'), copies2),

        # 3. Jeff Holman's book is either Wendalissa or the title that sold 19 copies.
        lany(membero((var(), 'Jeff Holman', 'Wendalissa'), books), eq((19, 'Jeff Holman', var()), copies2)),
        neq((19, 'Jeff Holman', 'Wendalissa'), copies2),
         
        # 4. The title that sold 19 copies was written by Alexis Olson.
        eq((19, 'Alexis Olson', var()), copies2),

        # 5. Dessert Oasis sold 7 more copies than Alexis Olson's book.
        right_of(books, (var(), var(), 'Dessert Oasis'), (var(), 'Alexis Olson', var())),

        # 6. Valores en los dominios faltantes
        membero((var(), 'Bill Ortega', var()), books),
        membero((var(), var(), 'Two for Tennis'), books)
        )

start = perf_counter()
solutions = run(0, books, booksproblem(books))
end = perf_counter()

print(solutions)

execution_time = (end - start)
print(execution_time)