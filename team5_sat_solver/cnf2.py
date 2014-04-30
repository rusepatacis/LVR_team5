__author__ = 'Jani'

from operands import *
from simplify import *

def convertToCNF(f):
    """
    Prevede funkcijo v CNF obliko.
    Kot vhod prejme funkcijo. Funkcija mora biti v primerni obliki (negacije
    so lahko le pred spremenljivkami).
    """
    if isinstance(f,(V,Not,Tru,Fls)):
        return f
    if isinstance(f, And):
        combined = []#ze v cnf obliki, samo zdruzimo skupaj posamezne konjunkcije
        for p in f.formule:
            combined.append(convertToCNF(p))
        return simplify(And(combined))
    if isinstance(f, Or):
        combined = []#moramo pretvoriti v CNF
        for p in f.formule:
            combined.append(convertToCNF(p))
        combined = kombinacije(combined)#pretvorimo tako, da naredimo vse mozne kombinacije med konjunkcijo in disjunkcijo
        comb2 = []
        for p in combined:
            comb2.append(Or(p))


        return And(comb2)


def kombinacije(f):
    """
    Prejme formulo (logicno), ter nam vrne vse mozne kombinacije na neki visini (ce na formulo gledamo kot drevo)
    """
    comb = []
    for i in f:
        if isinstance(i,V):
            comb = kombinacijeGenerator(comb,[i])
        elif isinstance(i,Not):
            comb = kombinacijeGenerator(comb,[i])
        else:
            comb = kombinacijeGenerator(comb,i.formule)
    return comb


def kombinacijeGenerator(comb,f):
    """
    Tole nam generira kombinacije z posamezno vejo.
    """
    tempComb = []
    for i in f:
        if not comb:
            return f
        for j in comb:
            if isinstance(i,Or): #s tem preprecimo vgnezdene Or stavke
                i = i.formule
            #Pozorni moramo biti, v kakem formatu dobimo vrednosti
            if type(j) == list:
                if type(i) == list:
                    tempComb.append(j+i)
                else:
                    tempComb.append(j+[i])
            else:
                if type(i) == list:
                    tempComb.append([j]+i)
                else:
                    tempComb.append([j,i])
    #Vrnemo seznam kombinacij.
    return tempComb
