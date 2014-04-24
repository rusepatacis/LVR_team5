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

#nekaj osnovnih primerov uporabe
print simplify(Not(Not(a2))) #brise dvojne negacije
print simplify(Or([V("X"),Not(V("X"))])) #prepozna tavtologijo
print simplify(And([V("X"),Not(V("X"))]))
print simplify(And([V("X"),Tru()])) #pobrise nepotrebne spremenljivke
print simplify(And([V("X"),V("X"),V("Y")])) #spremenljivke
print simplify(And([V("X"),V("X"),V("Y"),Fls()]))
print simplify(Or([Or([V("X"), V("Y")]), Or([V("Y"), V("Z")])]))
print simplify(Not(And([V("X"),V("Y")]))) #potisnemo negacijo navznoter
print simplify(Not(Equiv(V("X"),V("Y")))) #razbije izraz na konjunkcije in disjunkcije ter potisne negacijo navznoter


"""
######################################################
#################SAT PREVEDBE#########################
######################################################
"""

from team5_sat_solver.prevedba_hadamard import hadamardova_matrika

#generacija logicne funkcije, katere resitev predstavlja hadamardovo matriko
#funkcijo uporabimo tako, da kot parameter vnesemo zeljeno velicino matrike, algoritem pa nam bo nato vrnil logicno funkcijo
#katere resitev bo predstavljala hadamardovo matriko.
h2 = hadamardova_matrika(2)
h3 = hadamardova_matrika(3)
h4 = hadamardova_matrika(4)
h8 = hadamardova_matrika(8)

print h2
print h3
print h4
""""""""""""""
""""""""""""""
from team5_sat_solver.prevedba_coloring import barvanje
#Kot vhod podamo neusmerjen graf. Povezave med vozlisci predstavimo s pari npr. G = [(v1,v2), (v2,v5), (v2,v3), ...]
#Potrebno je podati tudi stevilo barv
#Metoda vrne logicno enacbo, katere resitev bo predstavljalo barvanje grafa,
#ce enacba ni resljiva, graf ni obarljiv s podanim stevilom barv.

G = [(V("a"),V("b")),(V("a"),V("c")),(V("c"),V("b"))] #trikotnik
print barvanje(G,3)
"""""""""""
"""""""""""
#kot vhod podamo slovar (dictionary), kjer sta koordinati sudokuja predstavljeni kot dvoterica, vrednost pa predstavlja
#znano vrednost sudokuja na tistem mestu
#algoritem nato logicno enacbo katere resitev predstavlja resitev za dani sudoku.

#Tole je resen sudoku, za testiranje pobrisi par random vrednosti (koordinata + stevilka)
sud = {(1,1):5,(1,2):3,(1,3):4,(1,4):6,(1,5):7,(1,6):8,(1,7):9,(1,8):1,(1,9):2,
        (2,1):6,(2,2):7,(2,3):2,(2,4):1,(2,5):9,(2,6):5,(2,7):3,(2,8):4,(2,9):8,
        (3,1):1,(3,2):9,(3,3):8,(3,4):3,(3,5):4,(3,6):2,(3,7):5,(3,8):6,(3,9):7,
        (4,1):8,(4,2):5,(4,3):9,(4,4):7,(4,5):6,(4,6):1,(4,7):4,(4,8):2,(4,9):3,
        (5,1):4,(5,2):2,(5,3):6,(5,4):8,(5,5):5,(5,6):3,(5,7):7,(5,8):9,(5,9):1,
        (6,1):7,(6,2):1,(6,3):3,(6,4):9,(6,5):2,(6,6):4,(6,7):8,(6,8):5,(6,9):6,
        (7,1):9,(7,2):6,(7,3):1,(7,4):5,(7,5):3,(7,6):7,(7,7):2,(7,8):8,(7,9):4,
        (8,1):2,(8,2):8,(8,3):7,(8,4):4,(8,5):1,(8,6):9,(8,7):6,(8,8):3,(8,9):5,
        (9,1):3,(9,2):4,(9,3):5,(9,4):2,(9,5):8,(9,6):6,(9,7):1,(9,8):7,(9,9):9}

#print X2SATsudoku(sud) #TODO zakaj tole ne dela?

"""
######################################################
#################DPLL#########################
######################################################
"""
#metoda prejme za parameter logicno formulo
#metoda vrne resitev formule, ce je to mogoce
#Opozorilo! Paziti moramo, da so negacije nahajo pri spremenljivkah! Potrebno je torej klicati metodo simplify preden
#vsavimo formulo v dpll.

"""

f1 = And([V("X"), V("Y")]) #TODO to tuki crasha v unit testu pa deluje :S
dpll(f1)

#print dpll(V("X"))
print dpll(And([V("X"), V("Y")]))
print dpll(And([XOR(V("X",V("Y"))),Or([V("X"),V("Y")])]))



f2 = (Or([And([XOR(V("a1,1"),V("a2,1")),Not(XOR(V("a1,2"),V("a2,2")))]),
                 And([Not(XOR(V("a1,1"),V("a2,1"))),XOR(V("a1,2"),V("a2,2"))])]))

#print dpll(push_not(f2)) #hadamarova matrika stopnje 2
#WTF, to v unit testu deluje, tukaj pa crasha :S

"""