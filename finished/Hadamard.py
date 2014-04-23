__author__ = 'Jaka & Jani'
#coding: UTF-8


from operands import *
import itertools

"""
Iskanje hadamardove matrike stopnje n.
Vrne logicno funkcijo, katere resitev (ce obstaja) je hadamardova matrika.
"""
def hadamardova_matrika(n):
    if n % 2 == 1:
        return Fls

    n = n+1 #ker stejemo indekse matrike od 1 naprej
    matrika = {}

    for i in range(1,n):#stolpec
        for j in range(1,n):#vrstica
            matrika[(i,j)] = V("a"+str(i)+","+str(j))

    formula = []

    for i in range(1,n-1):#stolpci
        xorParov = []
        for j in range(1,n):#vrstice
            #dobimo XOR pare elementov v stolpcu i in i+1 v vrstici j
            xorParov.append(XOR(matrika[(i,j)],matrika[(i+1,j)]))

        stolpecFormula = []
        """
        #tole bi se dalo se izbolsati, tako da izlocimo "simetricne" permutacije (1,2) == (2,1)
        for perm in itertools.permutations(xorParov):
            andFormula = list(perm[:len(perm)/2]) #pol jih mora biti pravilnih (1)
            NandFormula = list(perm[len(perm)/2:]) #pol jih mora biti napacnih
            NandFormula = Not(Or(NandFormula)) #drugi del morajo bit vsi 0, če postavimo vse v OR in OR negiramo dobimo to

            andFormula.append(NandFormula) #zdruzimo
            stolpecFormula.append(andFormula)
        """

        #optimizirano, ne podvajamo po nepotrebnem
        #izberemo pol vrstic, pol jih mora biti pravilnih, pol napačnih
        for perm in itertools.combinations(xorParov,len(xorParov)/2):
            andFormula = []
            NandFormula = []
            for x in xorParov:
                if x in perm:
                    andFormula.append(x)#prva polovica
                else:
                    andFormula.append(Not(x))#druga polovica

            #NandFormula = Not(Or(NandFormula))#negiran XOR

            #andFormula.append(NandFormula) #zdruzimo
            stolpecFormula.append(And(andFormula))

        formula.append(Or(stolpecFormula)) #ena od verzij za stolpec mora biti pravilna

    return And(formula) #za vsak stolpec mora biti vsaj 1 resitev


"""
Iskanje hadamardove matrike stopnje n.
Vrne logicno funkcijo, katere resitev (ce obstaja) je hadamardova matrika.
"""
def hadamardova_matrikaOLD(n):
    if n % 2 == 1:
        return Fls

    n = n+1 #ker stejemo indekse matrike od 1 naprej
    matrika = {}

    for i in range(1,n):#stolpec
        for j in range(1,n):#vrstica
            matrika[(i,j)] = V("a"+str(i)+","+str(j))

    formula = []

    for i in range(1,n-1):#stolpci
        xorParov = []
        for j in range(1,n):#vrstice
            #dobimo XOR pare elementov v stolpcu i in i+1 v vrstici j
            xorParov.append(XOR(matrika[(i,j)],matrika[(i+1,j)]))

        stolpecFormula = []

        #tole bi se dalo se izbolsati, tako da izlocimo "simetricne" permutacije (1,2) == (2,1)
        for perm in itertools.permutations(xorParov):
            andFormula = list(perm[:len(perm)/2]) #pol jih mora biti pravilnih (1)
            NandFormula = list(perm[len(perm)/2:]) #pol jih mora biti napacnih
            NandFormula = Not(Or(NandFormula)) #drugi del morajo bit vsi 0, če postavimo vse v OR in OR negiramo dobimo to

            andFormula.append(NandFormula) #zdruzimo
            stolpecFormula.append(andFormula)#TODO preglej ce dole deluje pravilno

        """
        #optimizirano, ne podvajamo po nepotrebnem
        #izberemo pol vrstic, pol jih mora biti pravilnih, pol napačnih
        for perm in itertools.combinations(xorParov,len(xorParov)/2):
            andFormula = []
            NandFormula = []
            for x in xorParov:
                if x in perm:
                    andFormula.append(x)#prva polovica
                else:
                    NandFormula.append(x)#druga polovica

            NandFormula = Not(Or(NandFormula))

            andFormula.append(NandFormula) #zdruzimo
            stolpecFormula.append(andFormula)
        """
        formula.append(Or(stolpecFormula)) #ena od verzij za stolpec mora biti pravilna

    return And(formula) #za vsak stolpec mora biti vsaj 1 resitev