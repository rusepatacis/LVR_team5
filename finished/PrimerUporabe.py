__author__ = 'Jaka & Jani'
#coding UTF-8

from CNF import *
from Coloring import *
from DPLL import *
from Hadamard import *
from operands import *
from Simplify import *
from Sudoku import *
from Utils import *

"""
##############################################
###############Operandi#######################
##############################################
"""
#True
Tru()
#False
Fls()
#Variable
V("imeSpremenljivke")

#And
a1 = And([V("X"),V("Y")]) #enostaven izraz (X and Y)
a2 = And([V("X"),And([V("Y"),V("Z")])]) #vgnezden izraz  (X and (Y and Z)), namesto
#and bi lahko dali tudi OR, ali drugi izraz
a3 = And([V("X"),V("Y"),V("Z")]) #zgorji izraz lahko krajse napisemo tako (samo zato, ker so vsi and)

#Or
o1 = Or([V("X"),V("Y")]) #enostaven izraz (X or Y)
o2 = Or([V("X"),Or([V("Y"),V("Z")])]) #enako kot pri konjunkciji
o3 = Or([V("X"),V("Y"),V("Z")])

#Implication
i1 = Imp(V("X"),V("Y")) #enostaven izraz (X sledi Y)
i2 = Imp(a1,o1) #vgnezden, (a1 sledi o2) (a1,o2 definirani zgoraj)

#Equivalence
e1 = Equiv(V("X"),V("Y")) #enostaven izraz (X equi Y)
e2 = Imp(a1,o1) #vgnezdeni izrazi, (a1 equi o2) (a1,o2 definirani zgoraj)

#XOR
x1 = XOR(V("X"),V("Y")) #enostaven izraz (X xor Y)
x2 = XOR(a1,o2) #vgnezden izraz (a1 xor o2)

#Not
Not(V("X")) #Negacija spremenljivke
Not(a1) #Negacija izraza

"""
######################################################
#################Simplify#############################
######################################################
"""
print simplify(Not(Not(a2)))

#TODO ostali primeri (To bom ze js naredu, razn za sudoku, ce imas kako idejo kako naredit povej)



