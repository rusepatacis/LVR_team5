__author__ = 'Jaka & Jani'
#coding UTF-8

"""
##############################################
###############Operandi#######################
##############################################
"""
from operands import *


# True
Tru()
# False
Fls()
# Variable
V("imeSpremenljivke")

# And
a1 = And([V("X"), V("Y")])  # Enostaven izraz (X and Y).
# Vgnezden izraz  (X and (Y and Z)), namesto And bi lahko dali tudi Or ali drugi izraz.
a2 = And([V("X"), And([V("Y"), V("Z")])])
a3 = And([V("X"), V("Y"), V("Z")])  # Zgornji izraz lahko krajse napisemo tako (samo zato, ker imamo same konjunkcije).

# Or
o1 = Or([V("X"), V("Y")])   # Enostaven izraz (X or Y).
o2 = Or([V("X"), Or([V("Y"), V("Z")])])     # Enako kot pri konjunkciji.
o3 = Or([V("X"), V("Y"), V("Z")])

# Implication
i1 = Imp(V("X"), V("Y"))     # Enostaven izraz (X sledi Y).
i2 = Imp(a1, o1)    # Vgnezden izraz, (a1 sledi o2) (a1, o2 definirani zgoraj).

# Equivalence
e1 = Equiv(V("X"),V("Y"))   # Enostaven izraz (X equi Y)
e2 = Imp(a1, o1)    # Vgnezdeni izrazi, (a1 equi o2) (a1, o2 definirani zgoraj).

# XOR
x1 = XOR(V("X"),V("Y"))     # Enostaven izraz (X xor Y).
x2 = XOR(a1, o2)    # Vgnezden izraz (a1 xor o2).

#Not
Not(V("X"))     # Negacija spremenljivke.
Not(a1)     # Negacija izraza.

"""
######################################################
#################Simplify#############################
######################################################
"""
from simplify import *
print simplify(Not(Not(a2))) #brise dvojne negacije
print simplify(Or([V("X"),Not(V("X"))])) #prepozna tavtologijo
print simplify(And([V("X"),Not(V("X"))]))
print simplify(And([V("X"),Tru()])) #pobrise nepotrebne spremenljivke
print simplify(And([V("X"),V("X"),V("Y")])) #spremenljivke
print simplify(And([V("X"),V("X"),V("Y"),Fls()]))

t1 = Or([Or([V("X"), V("Y")]), Or([V("Y"), V("Z")])])
print simplify(t1)