__author__ = 'Jani'

from operands import *
from simplify import *

def convertToCNF(f):
    if isinstance(f,(V,Not,Tru,Fls)):
        return f
    if isinstance(f, And):
        combined = []
        for p in f.formule:
            combined.append(convertToCNF(p))
        return simplify(And(combined))
    if isinstance(f, Or):
        combined = []
        for p in f.formule:
            combined.append(convertToCNF(p))
        combined = kombinacije(combined)
        comb2 = []
        for p in combined:
            comb2.append(Or(p))


        return And(comb2)


def kombinacije(f):
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
    tempComb = []
    for i in f:
        if not comb:
            return f
        for j in comb:
            if isinstance(i,Or): #s tem preprecimo vgnezdene Or stavke
                i = i.formule

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
    return tempComb
