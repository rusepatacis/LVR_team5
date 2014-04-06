__author__ = 'jaka'
#coding:utf-8

from lvr_vaje1 import And
from time import time

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
        return v[self.ime].vrednost(v)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(repr(self))


class Not:
    def __init__(self, p):
        self.formula = p

    def __repr__(self):
        return "¬" + str(self.formula)

    def vrednost(self, v):
        return not(self.formula.vrednost(v))

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(repr(self))


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


class Imp(Or):
    """
    Implcation
    """
    def __init__(self, p, q):
        self.p = p
        self.q = q
        Or.__init__(self, [Not(p), q])

    def __repr__(self):
        return str(self.p) + " ⇒ " + str(self.q)


class Equiv(And):
    """
    Logical equivalence
    """
    def __init__(self, p, q):
        self.p = p
        self.q = q
        And.__init__(self, [Or([Not(p), q]), Or([p, Not(q)])])

    def __repr__(self):
        return str(self.p) + " ⇔ " + str(self.q)


class XOR(And):

    def __init__(self, p, q):
        self.p = p
        self.q = q
        And.__init__(self, [Or([Not(p), Not(q)]), Or([p, q])])

    def __repr__(self):
        return str(self.p) + " ⊕ " + str(self.q)


class Stopwatch():
    def __init__(self):
        self.timestamps = [time()]
        self.tags = ["Start"]

    def intermediate(self,tag=""):
        if len(self.timestamps) == 0:
            print "Error. Stopwatch not running. Starting it now."
            self.timestamps.append(time())

            if len(tag) == 0:
                self.tags = ["Start"]
            else:
                self.tags = [tag]
        else:
            self.timestamps.append(time())
            if len(tag) == 0:
                self.tags.append("Inter" + str(len(self.timestamps)-1))
            else:
                self.tags.append(tag)

    def start(self,tag=""):
        if len(self.timestamps > 1):
            print "Error. Stopwatch already running."
        else:
            self.timestamps.append(time())
            if len(tag) == 0:
                self.tags.append("Inter" + str(len(self.timestamps)-1))
            else:
                self.tags.append(tag)

    def restart(self,tag=""):
        self.timestamps = [time()]
        if len(tag) == 0:
            self.tags = ["Start"]
        else:
            self.tags = [tag]

    def clear(self):
        self.timestamps = []
        self.tags = []

    def stop(self,tag=""):
        self.timestamps.append(time())
        if len(tag) == 0:
            self.tags.append("Inter" + str(len(self.timestamps)-1))
        else:
            self.tags.append(tag)

    def __repr__(self):
        x = "Time: "
        y = "      "
        if len(self.timestamps) > 0:
            for t in range(0,len(self.timestamps)-2):
                #x += str(self.timestamps[t+1] - self.timestamps[t])+" "

                tmp = '%.3f ' % (self.timestamps[t+1] - self.timestamps[t])
                x += tmp+" "*(abs(8-len(tmp)))
                y += self.tags[t+1] + " "*abs(8-len(self.tags[t+1]))

            x += "\n"
            x += "Total: %.3f" % (self.timestamps[len(self.timestamps)-1] - self.timestamps[0]) + " s"
        else:
            x += "Stopwatch not started."
        y += "\n"
        return y+x




def simplify(formula, verbose=False):
    if verbose:
        print "\t\t", formula, formula.__class__
    if formula.__class__.__name__ in ('V', 'Fls', 'Tru'):
        if verbose:
            print "Tukaj sem", formula
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

        """if formula.__class__.__name__ == 'Or':
            formula = simplify_or_same(formula)
        elif formula.__class__.__name__ == 'And':
            formula = simplify_and_same(formula)
        """

        temp = []
        for p in formula.formule:
            p = simplify_and_same(p)
            p = simplify_or_same(p)

            if p not in temp:
                temp.append(p)
        new = temp
        formula.formule = new
        if len(formula.formule) == 1:
            return formula.formule[0]
        else:
            return formula
    else:
        return formula

def simplify_or_same(formula):
    if formula.__class__.__name__ in ('V','Not'):
        return formula

    same = True
    for form in formula.formule:
        if form.__class__.__name__ != 'V':
            same = False
            break

    if same:
        simp = []
        for form in formula.formule:
            if form not in simp:
                simp.append(form)

        formula.formule = simp
        return formula

    if formula.__class__.__name__ == 'Or':
        onlyOr = True
        for form in formula.formule:
            if form.__class__.__name__ not in ('Or', 'V'):
                onlyOr = False
                break

        temp = []
        if onlyOr:
            for form in formula.formule:
                tmpFormula = simplify_or_same(form)

                if tmpFormula.__class__.__name__ == 'V':
                    temp.append(tmpFormula)
                    continue
                for form2 in tmpFormula.formule:
                    if form2 not in temp:
                        temp.append(form2)

            formula.formule = temp
        return formula
    return formula

def simplify_and_same(formula):
    if formula.__class__.__name__ in ('V','Not'):
        return formula

    same = True
    for form in formula.formule:
        if form.__class__.__name__ != 'V':
            same = False
            break

    if same:
        simp = []
        for form in formula.formule:
            if form not in simp:
                simp.append(form)

        formula.formule = simp
        return formula

    if formula.__class__.__name__ == 'And':
        onlyOr = True
        for form in formula.formule:
            if form.__class__.__name__ not in ('And', 'V'):
                onlyOr = False
                break

        temp = []
        if onlyOr:
            for form in formula.formule:
                tmpFormula = simplify_and_same(form)

                for form2 in tmpFormula.formule:
                    if form2 not in temp:
                        temp.append(form2)

            formula.formule = temp
        return formula
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

def hadamardova_matrika(n):
    n = n+1 #ker stejemo indekse matrike od 1 naprej
    matrika = {}

    for i in range(1,n):
        for j in range(1,n):
            matrika[(i,j)] = V("a"+str(i)+","+str(j))

    formula = []

    for i in range(1,n-1):#stolpci
        temp = []
        for j in range(1,n):#vrstice
            for k in range(j+1,n):#vrstice
                t1 = Not(XOR([matrika[(j, i)], matrika[(j, i+1)]]))
                t2 = Not(XOR([matrika[(k, i)], matrika[(k, i+1)]]))
                temp.append(XOR([t1,t2]))

        while len(temp) > 2:
            temp2 = []
            for i1 in range(len(temp)-1):
                temp2.append(XOR([temp[i1],temp[i1+1]]))
            temp = temp2

        if len(temp) == 1:
            f = temp[0]
        else:
            f = And([temp[0],temp[1]])

        formula.append(f)

    if len(formula) == 1:
        return formula[0]

    return And(formula)




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
    def convert_nnf_to_CNF(cs, verbose=False):
        if isinstance(cs, Tru):
            if verbose:
                print "Tru", cs
            return splosci(cs)
        if isinstance(cs, Fls):
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
            return splosci(And([convert_nnf_to_CNF(term, verbose)
                        for term in cs.formule]))
        if isinstance(cs, Or):
            if not cs.formule:
                if verbose:
                    print "Or 0", cs
                return And([Or([])])
            elif len(cs.formule) == 1:
                if verbose:
                    print "Or 1", cs
                return splosci(convert_nnf_to_CNF(cs.formule[0]), verbose)
            else:
                if verbose:
                    print "Or > 2", cs
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
                    return splosci(And([convert_nnf_to_CNF(Or(ostalo+[el]+konj[1:]), verbose) for el in konj[0].formule]))
    tmp_cnf = convert_nnf_to_CNF(splosci(simplify(p)), verbose=verbose)
    # Polovimo proste literatle
    new_formule = []
    for f in tmp_cnf.formule:
        if isinstance(f, V) or isinstance(f, Not):
            new_formule.append(Or([f]))
        else:
            new_formule.append(f)
    return And(new_formule)


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


def dpll(f, verbose=False):
    """
    DPLL algorithm

    formula.vrednost(dpll(formula)) will return True (if the problem is solvable)
    """
    if verbose:
        print "Formula", f

    # Primer prazne formule
    if not f:
        return False

    # Pretvori v CNF
    cnf_f = convert_to_CNF(f)
    if verbose:
        print "CNF____", cnf_f

    # Primer prazne formule
    if not cnf_f.formule:
        return False

    # Slovar spremenljivk, katerih vrednosti poznamo
    v = {}

    # Seznam stavkov, ki jih se moramo obdelati
    cs = cnf_f.formule
    if verbose:
        print "CS_____", cs
        print "CSitemC", len(cs)


    def dpll_aux(v, cs, verbose=False):

        # Slovar spremenljivk, katerih vrednosti še ne poznamo
        neznane_vrednosti = set(v for stavek in cs for v in stavek.formule)
        if verbose:
            print "Nezanane vrednosti", sorted(list(neznane_vrednosti))


        # Optimiziramo z sortiranjem seznama stavkov po velikosti (krajse stavke obdelamo prej)
        cs = sorted(cs, key=lambda x: len(x.formule))

        # Gremo cez stavke in obravnavmo primere
        ocisceni_cs=[]
        for i, stavek in enumerate(cs):
            # Naletimo na prazen stavek --> false (ni resitve)
            if not stavek.formule:
                return False
            # Naletimo na seznam z enim elemetom [xi] (spremenljivka ali negacija)
            # znamo nastaviti xi
            if len(stavek.formule) == 1:
                lit = stavek.formule[0]
                if isinstance(lit, V) or isinstance(lit, Not):
                    v[lit] = Tru()
                else:
                    raise TypeError
                # Take stavke odstranimo
            else:
                ocisceni_cs.append(stavek)

        # Dobimo posodobljen v in skrcen seznam cs
        cs = ocisceni_cs

        if verbose:
            print "Updated v", v
            print "Updated CS", cs

        # Poenostavimo cs tako, da upostevamo razsirjeni v
        upostevamo_v_cs = []
        for stavek in cs:
            nov_stavek = []
            true_spremenljivka = False
            for variable in stavek.formule:
                if variable in v:
                    if v[variable] == Tru():
                        true_spremenljivka = True
                        break
                    # Literale, ki so Fls izpustimo iz novega izraza
                else:
                    nov_stavek.append(variable)

            if not true_spremenljivka:
                # Ce nismo naleteli na Tru, dodamo izraz oziroma njegov del
                upostevamo_v_cs.append(Or(nov_stavek))

        cs = upostevamo_v_cs
        if verbose:
            print "CS upostevsi v", cs

        # ce cs sedaj prazen -> odgovor je v
        if not cs:
            return v


        # cs sedaj ni prazen
        # se vedno imamo stavke za obdelavo, a trenutno nimamo dodatnega znanja
        # zato izberemo xi in preizkusimo xi = Fls in xi = Tru
        if not neznane_vrednosti:
            return False
        else:
            xi = neznane_vrednosti.pop()
            v[xi] = Tru()
            v1 = dpll_aux(v, cs, verbose)
            if not v1:
                v[xi] = Fls()
                return dpll_aux(v, cs, verbose)
            else:
                return v1


    v = dpll_aux(v, cs, verbose)
    if v:
        # Imamo resitev
        # Nezanke, ki v resitvi niso omenjene, nastavimo na Fls
        for var in set(v for stavek in cs for v in stavek.formule):
            if var not in v:
                v[var] = Fls()

        # Pocistimo negacije, pretvorimo v slovar stringov (ki so imena spremenljivk).
        v_final = {}
        for var in v:
            if isinstance(var, V):
                v_final[var.ime] = v[var]
            elif isinstance(var, Not):
                if v[var] == Fls():
                    v_final[var.formula.ime] = Tru()
                elif v[var] == Tru():
                    v_final[var.formula.ime] = Fls()
                else:
                    raise ValueError
            else:
                raise TypeError
        return v_final
    else:
        return False
