__author__ = 'Jaka & Jani'
#coding UTF-8

from operands import *
from CNF import *

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