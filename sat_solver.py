__author__ = 'jaka'
#coding:utf-8

class Fls:
    def __init__(self):
        pass

    def __repr__(self):
        return 'Fls'

    def vrednost(self, v):
        return False

    def __eq__(self, other):
        return str(self) == str(other)



class Tru:
    def __init__(self):
        pass

    def __repr__(self):
        return 'Tru'

    def vrednost(self, v):
        return True

    def simplify(self):
        pass

    def __eq__(self, other):
        return str(self) == str(other)


class V:
    def __init__(self, ime):
        self.ime = ime

    def __repr__(self):
        return str(self.ime)

    def vrednost(self, v):
        return v[self.ime]

    def __eq__(self, other):
        return str(self) == str(other)


class Not:
    def __init__(self, p):
        self.formula = p

    def __repr__(self):
        return "¬" + str(self.formula)

    def vrednost(self, v):
        return not(self.formula.vrednost(v))

    def __eq__(self, other):
        return str(self) == str(other)


class And:
    def __init__(self, ps):
        self.formule = ps

    def __repr__(self):
        return "(%s)" % (" ∧ ".join(str(f) for f in self.formule))


    def vrednost(self, v):
        b = True
        for p in self.formule:
            b = b and p.vrednost(v)
            if not b: break
        return b

    def __eq__(self, other):
        return str(self) == str(other)


class Or:
    def __init__(self, ps):
        self.formule = ps

    def __repr__(self):
        return "(%s)" % (" ∨ ".join(str(f) for f in self.formule))


    def vrednost(self, v):
        b = False
        for p in self.formule:
            b = b or p.vrednost(v)
            if b: break
        return b

    def __eq__(self, other):
        return str(self) == str(other)


class Imp:
    def __init__(self, formule):
        self.formule = formule

    def __repr__(self):
        return  "(%s)" % (" ⇒ ".join(str(f) for f in self.formule))

    def vrednost(self, v):
        # p ---> q = NOTp or q
        b = self.formule[0].vrednost(v)
        for p in self.formule[1:]:
            b = (not b) or p.vrednost(v)
        return b

    def __eq__(self, other):
        return str(self) == str(other)


class XOR():
    def __init__(self, formule):
        self.formule = formule

    def __repr__(self):
        return "(%s)" % (" XOR ".join(str(f) for f in self.formule))

    def vrednost(self, v):
        p, q = self.formule[0], self.formule[1]
        return And([
            Or([p, q]),
            Not(And([p, q]))
        ]).vrednost(v)


def simplify(formula, verbose=False):
    if verbose:
        print formula
    if formula.__class__.__name__ in ('V', 'Fls', 'Tru'):
        if verbose:
            print "Tukaj sem"
        return formula
    elif formula.__class__.__name__ == 'Not':
        if formula.formula.__class__.__name__ == 'And':
            return Or([simplify(Not(p)) for p in formula.formula.formule])
        if formula.formula.__class__.__name__ == 'Or':
            return And([simplify(Not(p)) for p in formula.formula.formule])
        if formula.formula.__class__.__name__ == 'Not':
            return simplify(formula.formula.formula)
        if formula.formula.__class__.__name__ == 'Fls':
            return Tru()
        if formula.formula.__class__.__name__ == 'Tru':
            return Fls()
        if formula.formula.__class__.__name__ == 'V':
            return Not(formula.formula)
        return formula
    elif formula.__class__.__name__  in ('And', 'Or'):
        if formula.__class__.__name__ == 'And':
            for b in formula.formule:
                if b == "Fls":
                    return Fls()
            tmp = []
            for b in formula.formule:
                if b == Tru():
                    pass
                else:
                    tmp.append(b)
            if len(tmp) == 1:
                return tmp[0]
            else:
                formula.formule = tmp
            formula.formule = tmp
            for a in range(len(formula.formule)):
                for b in range(a+1,len(formula.formule)):
                    if simplify(formula.formule[a]) == simplify(Not(formula.formule[b])):
                        return Fls()

        if formula.__class__.__name__ == 'Or':
            for b in formula.formule:
                if b == "Tru":
                    return Tru()
            tmp = []
            for b in formula.formule:
                if b == Fls():
                    pass
                else:
                    tmp.append(b)
            if len(tmp) == 1:
                return tmp[0]
            else:
                formula.formule = tmp
            formula.formule = tmp
            for a in range(len(formula.formule)):
                for b in range(a+1,len(formula.formule)):
                    if simplify(formula.formule[a]) == simplify(Not(formula.formule[b])):
                        return Tru()

        temp = []
        for p in formula.formule:
            if p not in temp:
                temp.append(p)
        new = temp
        formula.formule = new
        if len(formula.formule) == 1:
            return V(formula.formule[0])
        else:
            return formula
    else:
        return formula

"""
    Vaje 2 - prevedbe problemov
"""





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



"""
    Vaje 3 - prevedbe problemov
"""


def barvanje(G, b):
    """
        Prevedba problema barvanja grafov na SAT

        G - neusmerjen graf, podan s seznamom povezav (dvojk, vozlišča so nizi),
        torej G = [(v1,v2), (v2,v5), (v2,v3), ...]
        b - želeno število barv
    """
    if not G or b <= 0:
        raise Exception("Preveri obliko vhodnega grafa in predznak števila barv!")

    # Za lažje razumevanje barve shranimo v seznam
    barve = range(1, b+1)
    # Definicija spremenljivk oblike Cik ... vozlisce i je barve k
    vozlisca = list(set([u for (u, v) in G] + [v for (u, v) in G]))

    # Za lazje delo vozlisca shranimo v slovar oblike (ime_vozlisca, barva) -> pripadajoca spremenljivka
    spremenljivke = dict(((v, k), V('C%s%d' % (v, k))) for v in vozlisca for k in barve)

    # Vsako vozlišče je pobarvano z vsaj eno barvno
    vsaj_ena_barva = And([[Or([spremenljivke[(v, k)]]) for k in barve] for v in vozlisca])

    # Nobeno vozlišče ni hkrati pobarvnano z dvema barvama
    pari_barv = [(barve[j], barve[i]) for i in range(len(barve)) for j in range(i)]
    nobeno_dvakrat = And([And([Not(And([spremenljivke[(v, par_barv[0])], spremenljivke[(v, par_barv[1])]])) for par_barv in pari_barv]) for v in vozlisca])

    # Povezani vozlišči nista iste barve
    povezani_nista_iste = And([[Not(And([spremenljivke[(vi, k)], spremenljivke[(vj, k)]])) for k in barve] for (vi, vj) in G])

    # Prevedba je konjunkcija pogojev
    return And([vsaj_ena_barva, nobeno_dvakrat, povezani_nista_iste])



"""
Vaje 4,5 - DLSS
"""

"""
Pretvorba v CNF obliko
"""


def only_literals(p):
    """
    Vrne True, če so v formuli p samo spremenljivke (in ne dodatni operatorji)
    """
    # Ločeno preverimo Not
    if isinstance(p, Not):
        return isinstance(p.formula, V)
    # Sicer preverjamo posamezne člene
    for trm in p.formule:
        if not isinstance(trm, V) and not isinstance(trm, Not):
            return False
        # Preverimo tudi negirane člene
        elif isinstance(trm, Not) and not isinstance(trm.formula, V):
            return False
    return True


def is_CNF_clause(p):
    """
    Če imamo disjunkcijo, ki ima notri samo literale ali negirane literale, jo lahko porabimo za CNF
    (konjukcija takih disjunkcij je CNF).
    """
    return isinstance(p, Or) and only_literals(p)


def is_CNF_formula(p):
    """
    Vrne true če je formula p v CNF obliki
    """
    # Imeti moramo konjunkcijo...
    if isinstance(p, And):
        # ... samih disjunkctnih stavkov
        for trm in p.formule:
            if not (is_CNF_clause(trm)):
                return False
    else:
        return False
    return True


def convert_to_CNF(p, verbose=False):
    """
    Pretvorba formule v CNF
    """
    def convert_nnf_to_CNF(cs, verbose=verbose, i=0):
        print cs, isinstance(cs, V)
        i += 1
        if isinstance(cs, Tru):
            if verbose:
                print "Tru", cs
            return splosci(cs)
        if isinstance(cs, Fls):
            print "FALSH"
            if verbose:
                print "Fls", cs
            return And([Or([])])
        if isinstance(cs, V):
            if verbose:
                print "Variabla", cs
            return splosci(Or([cs]))
        if isinstance(cs, Not):
            if verbose:
                print "Not", cs
            return splosci(Or([cs]))
        if isinstance(cs, And):
            if verbose:
                print "And", cs
            return splosci(And([convert_nnf_to_CNF(term, i=i)
                        for term in cs.formule]))
        if isinstance(cs, Or):
            if not cs.formule:
                if verbose:
                    print "Or 0", cs
                return And([Or([])])
            elif len(cs.formule) == 1:
                if verbose:
                    print "Or 1", cs
                return splosci(convert_nnf_to_CNF(cs.formule[0], i=i))
            else:
                # Kompliciran or, potrebna distribucija
                konj, ostalo = [], []
                for f in cs.formule:
                    if isinstance(f, And):
                        konj.append(f)
                    else:
                        ostalo.append(f)
                if not konj:
                    return splosci(Or(ostalo))
                else:
                    return splosci(And([convert_nnf_to_CNF(Or(ostalo+[el]+konj[1:])) for el in konj[0].formule]))
    return convert_nnf_to_CNF(splosci(simplify(p)))


def splosci(f):
    """
    Splosci (flatten) dani izraz, kolikor je mozno.
    """
    a = simplify(f)
    def splosci_aux(p):
        if isinstance(p, And):
            nove = []
            for fr in p.formule:
                if isinstance(fr, And):
                    nove += [splosci_aux(x) for x in fr.formule]
                else:
                    nove.append(splosci_aux(fr))
            p.formule = nove
        elif isinstance(p, Or):
            nove = []
            for fr in p.formule:
                if isinstance(fr, Or):
                    nove += [splosci_aux(x) for x in fr.formule]
                else:
                    nove.append(splosci_aux(fr))
            p.formule = nove
        else:
            return p
        return p
    return splosci_aux(a)