__author__ = 'Jaka & Jani'
#coding: UTF-8

from operands import *
from simplify import simplify, simplify_not


def only_literals(p):
    """
    Vrne True, ce so v formuli p samo literali (in ne dodatni operatorji). Sicer False.
    """
    # Loceno preverimo Not
    if isinstance(p, Not):
        return isinstance(p.formula, V)
    # Sicer preverjamo posamezne clene
    for trm in p.formule:
        if not isinstance(trm, V) and not isinstance(trm, Not):
            return False
        # Preverimo tudi negirane clene
        elif isinstance(trm, Not) and not isinstance(trm.formula, V):
            return False
    return True


def is_CNF_clause(p):
    """
    Vrne True, ce je formula p CNF stavek (disjunkcija literalov). Sicer False.

    Ce imamo disjunkcijo, ki ima notri samo literale ali negirane literale, jo lahko porabimo za CNF.
    Konjukcija takih disjunkcij je CNF.
    """
    return isinstance(p, Or) and only_literals(p)


def is_CNF_formula(p):
    """
    Vrne true ce je formula p v CNF obliki,
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
    Pretvorba formule v CNF.
    p - formula za pretvorbo
    verbose - zastavica za izpis poteka funkcije

    Vrne formulo p v CNF obliki.
    """
    def convert_to_cnf_aux(f):
        """
        Prevede funkcijo v CNF obliko.
        Kot vhod prejme funkcijo. Funkcija mora biti v primerni obliki (negacije
        so lahko le pred spremenljivkami).
        """
        if isinstance(f, (V, Not, Tru, Fls)):
            return f
        if isinstance(f, And):
            combined = []   # Ze v cnf obliki, samo zdruzimo skupaj posamezne konjunkcije.
            for p in f.formule:
                combined.append(convert_to_cnf_aux(p))
            return simplify(And(combined))
        if isinstance(f, Or):
            combined = []   # Moramo pretvoriti v CNF.
            for p in f.formule:
                combined.append(convert_to_cnf_aux(p))
            # Pretvorimo tako, da naredimo vse mozne kombinacije med konjunkcijo in disjunkcijo.
            combined = kombinacije(combined)
            comb2 = []
            for p in combined:
                comb2.append(Or(p))
            return And(comb2)

    def simp_cnf(cs, verbose=False):
        """
        Nadaljnje poenostavljanje.
        """
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
            return splosci(And([simp_cnf(term, verbose) for term in cs.formule]))
        if isinstance(cs, Or):
            if not cs.formule:
                if verbose:
                    print "Or 0", cs
                return And([Or([])])
            elif len(cs.formule) == 1:
                if verbose:
                    print "Or 1", cs
                return splosci(simp_cnf(cs.formule[0]))
            else:
                if verbose:
                    print "Or > 2", cs
                # Kompliciran Or, potrebna distribucija
                konj, ostalo = [], []
                for f in cs.formule:
                    if isinstance(f, And):
                        konj.append(f)
                    else:
                        ostalo.append(f)
                if not konj:
                    return splosci(Or(ostalo))
                else:
                    return splosci(And([simp_cnf(Or(ostalo+[el]+konj[1:]), verbose)
                                        for el in konj[0].formule]))

    # Osnovna pretvorba.
    tmp_cnf = simp_cnf(splosci(simplify(convert_to_cnf_aux(simplify_not((simplify(p)))))))

    # Robni primeri.
    if isinstance(tmp_cnf, V) or isinstance(tmp_cnf, Not) or isinstance(tmp_cnf, Fls):
        return And([Or([tmp_cnf])])
    if isinstance(tmp_cnf, Tru):
        return Tru()

    # Polovimo proste literatle.
    new_formule = []
    for f in tmp_cnf.formule:
        if isinstance(f, V) or isinstance(f, Not):
            new_formule.append(Or([f]))
        else:
            new_formule.append(f)

    return And(new_formule)


def splosci(f):
    """
    Splosci (flatten) dano formulo f, kolikor je mozno.
    """
    a = simplify(f)

    def splosci_aux(p):
        """
        Pomozna funkcija za rekurzivne klice.
        """
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


def kombinacije(f):
    """
    Prejme formulo (logicno) ter nam vrne vse mozne kombinacije na neki visini (ce na formulo gledamo kot drevo).
    """
    comb = []
    for i in f:
        if isinstance(i, V):
            comb = kombinacijeGenerator(comb, [i])
        elif isinstance(i, Not):
            comb = kombinacijeGenerator(comb, [i])
        else:
            comb = kombinacijeGenerator(comb, i.formule)
    return comb


def kombinacijeGenerator(comb, f):
    """
    Tole nam generira kombinacije z posamezno vejo.
    """
    tempComb = []
    for i in f:
        if not comb:
            return f
        for j in comb:
            if isinstance(i, Or):   # S tem preprecimo vgnezdene Or stavke.
                i = i.formule
            # Pozorni moramo biti, v kakem formatu dobimo vrednosti.
            if type(j) == list:
                if type(i) == list:
                    tempComb.append(j+i)
                else:
                    tempComb.append(j+[i])
            else:
                if type(i) == list:
                    tempComb.append([j]+i)
                else:
                    tempComb.append([j, i])
    # Vrnemo seznam kombinacij.
    return tempComb
