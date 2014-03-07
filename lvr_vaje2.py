#coding:utf-8
__author__ = 'jaka'
from lvr_vaje1 import *

t1 = (And([Or([V("p"), V("q")]), Or([V("p"), V("r")])]))
t2 = Or([Imp([V("p"), V("q")]), V("p"), Imp([V("p"), V("q")])])

# Barvanje grafa

class XOR():
    def __init__(self, formule):
        self.formule = formule

    def __repr__(self):
        return "XOR"+str(self.formule)

    def vrednost(self, v):
        p, q = self.formule[0], self.formule[1]
        return And([
            Or([p, q]),
            Not(And([p, q]))
        ]).vrednost(v)


def X2SATsudoku(vhod):
    """
        vhod - slovar (i,j) -> stevilka
        Xijk --- na (i,j) je k
    """

    temp_vrstica = []
    for i in range(1,10):
        for a in range(1,9):
            for b in range(a+1,10):
                for k in range(1,10):
                    if (i,a) in vhod:
                        if vhod[(i,a)] == k:
                            temp_vrstica.append(XOR([
                                Tru,
                                V('X'+str(i)+str(b)+str(k))
                            ]))
                        else:
                            temp_vrstica.append(XOR([
                                False,
                                V('X'+str(i)+str(b)+str(k))
                            ]))
                    elif (i,b) in vhod:
                        if vhod[(i,b)] == k:
                            temp_vrstica.append(XOR([
                                Tru,
                                V('X'+str(i)+str(b)+str(k))
                            ]))
                        else:
                            temp_vrstica.append(XOR([
                                False,
                                V('X'+str(i)+str(b)+str(k))
                            ]))
                    else:
                        temp_vrstica.append(XOR([
                            V('X'+str(i)+str(a)+str(k)),
                            V('X'+str(i)+str(b)+str(k))
                        ]))
    vrstice = And(temp_vrstica)

    temp_stolpec = []
    for i in range(1,10):
        for a in range(1,9):
            for b in range(a+1,10):
                for k in range(1,10):
                    temp_stolpec.append(XOR([
                        V('X'+str(a)+str(i)+str(k)),
                        V('X'+str(b)+str(i)+str(k))
                    ]))
    stolpci = And(temp_stolpec)

    temp_kvadrat = []
    for i in range(1, 10, 3):
        for j in range(1, 10, 3):
            tmp_indeksi = [(a, b) for b in range(j, j+3) for a in range(i, i+3)]
            for ind1 in range(8):
                for ind2 in range(9):
                    prvi_x, prvi_y = tmp_indeksi[ind1][0], tmp_indeksi[ind1][1]
                    drugi_x, drugi_y = tmp_indeksi[ind2][0], tmp_indeksi[ind2][1]
                    for k in range(1,10):
                        temp_kvadrat.append(XOR([
                            V('X'+str(prvi_x)+str(prvi_y)+str(k)),
                            V('X'+str(drugi_x)+str(drugi_y)+str(k))
                        ]))
    kvadranti = And(temp_kvadrat)
    return And([vrstice, stolpci, kvadranti])

# Hadamardova matrika
"""
Xij i,j € {1,2,m...}

Xij = T, če (i,j) = 1
Xij = F, če (i,j) = -1

Formula:
A (1<=i<j<=n ... za u.to in jto vrstico) do
    "skalarni produkt i-te in jte vrstice je enak 0"
    Namig: uporabi kakšne nove spremenljivke za računanje skalarnega produkta
"""

