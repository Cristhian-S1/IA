
from kanren import Relation, run, var, fact

x = var() 
human = Relation()

fact(human,'Socrates')

def mortal(x):
    return human(x)

sol = run(0,x,mortal(x))
print(sol)
