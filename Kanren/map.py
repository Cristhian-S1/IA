from kanren import run, var, lall, membero
from kanren.constraints import neq

wa, nt, sa, q, nsw, v = var(), var(), var(), var(), var(), var()

australia = (wa, nt, sa, q, nsw, v)

mapa = ((wa,nt), (wa,sa), (nt,sa), (nt,q), (sa,q), (sa,nsw), (sa,v), (q,nsw), (v,nsw))

def domain(regiones) :
    return lall(membero(r,['red','green','blue']) for r in regiones)

def differents(vecinos):
    return lall(neq(r1,r2) for r1,r2 in vecinos)

colors = run(0, australia, domain(australia), differents(mapa))

print(colors)
