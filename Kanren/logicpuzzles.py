# logic puzzles library
# author: Ricardo Valdivia
# date: 28-03-2023

from kanren import *
from kanren.constraints import neq
from itertools import combinations, product


# FUNCIONES POSICIONALES

def left_of(l, p, q, n=1):
    """left_of es verdadero si p esta a la izquierda de q (n posiciones) en la lista l.""" 
    return membero((p, q), list(zip(l, l[n:])))

def right_of(l, p, q, n=1):
    """right_of es verdadero si p esta a la derecha de q (n posiciones) en la lista l."""
    return left_of(l, q, p, n)

def next_to(l, p, q, n=1):
    """next_of es verdadero si p esta a la izquierda o derecha de q (n posiciones) en la lista l."""
    return lany(left_of(l, p, q, n), left_of(l, q, p, n))

def somewhat_left_of(l, p, q):
    """somewhat_left_of es verdadero si p esta en algún lugar a la izquierda de q en la lista l."""
    return membero((p,q), list(combinations(l,2)))

def somewhat_right_of(l, p, q):
    """somewhat_right_of es verdadero si p esta en algún lugar a la derecha de q en la lista l."""
    return somewhat_left_of(l, q, p)

# FUNCION NMEMBERO 

def nmembero(l, p, idx):
    """nmembero es verdadero si p no es miembro (en particular considerando los atributos indexados por idx)
       de la lista l."""
    return lall(neq(p, tuple(r[i] for i in idx)) for r in l)

# FUNCIONES DIFFERENTS

def clean_var(p):
    """ clean_var verifica que cada componente en la lista de listas p no incluya variables no instanciadas."""
    for i in p:
        for j in i:
            if isvar(j): return(False)
    return(True)


def different(l, par, idx):
    """different verifica que cada pareja de atributos en la lista par no corresponda al mismo sujeto en la
       lista l. La pareja de indices del parámetro idx permite indexar los atributos correspondientes en la
       lista l."""
    return lall(neq(p, (r[idx[0]], r[idx[1]])) for p in par for r in l)

def differents(l, d):
    """differents verifica que cada atributo en la lista de listas d corresponda a un sujeto diferente
       de la lista l"""
    par = tuple(tuple(product(m, n)) for m, n in combinations(d, 2))
    idx = tuple(combinations((i for i in range(len(d))),2))
    
    return lall(different(l, p, i) for p, i in zip(par, idx) if clean_var(p))
