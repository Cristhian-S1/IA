# Usar la implementacion miniKanren de kanren para python 

from kanren import Relation, facts, run, var 
from kanren.constraints import neq
from kanren.core import conde, lall, lany, Zzz

father = Relation()
mother = Relation()

x = var()
y = var()

facts(father,('Abraham','Orville'),
             ('Herb','Abraham'),
             ('Homer','Abraham'),
             ('Marge','Clancy'),
             ('Patty','Clancy'),
             ('Selma','Clancy'),
             ('Bart','Homer'),
             ('Lisa','Homer'),
             ('Maggie','Homer'))

facts(mother,('Homer','Mona'),
             ('Marge','Jackie'),
             ('Patty','Jackie'),
             ('Selma','Jackie'),
             ('Bart','Marge'),
             ('Lisa','Marge'),
             ('Maggie','Marge'),
             ('Ling','Selma'))

# parent es el padre o madre de x
def parent(x,y):
    return lany(father(x,y), mother(x,y))

# grandparent es el abuelo o abuela de x
def grandparent(x,y):
    z = var()
    return lall(parent(x,z), parent(z,y))

# sibling es el hermano de x
def sibling(x,y):
    z = var()
    return lall(parent(x,z), parent(y,z), neq(x,y))

# ancestros de x
def ancestor(x,y):
    z = var()
    # Zzz posterga la evaluación de la llamada recursiva hasta que los
    # objetivos actuales sean satisfechos
    return conde([parent(x,y)], [parent(x,z), Zzz(ancestor,z,y)])