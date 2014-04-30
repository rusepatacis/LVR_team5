__author__ = 'Jaka & Jani'
#coding: UTF-8

""" Modul, ki vsebuje algoritem DPLL. """

from cnf2 import convertToCNF
from cnf import convert_to_CNF
from simplify import *
from operands import *


def dpll(f, verbose=False):
    """
    Algoritem DPLL za resevanje SAT.
    f - formula (objekt operandov)
    verbose - zastavica za izpis poteka funkcije

    Ce je formula izpolnjiva, vrne slovar t vnosi oblike ('ime_spremenljvke' -> resnicnost [Tru/Fls])
    sicer vrne False.
    V primeru tavtologije brez prostih spremenljivk vrne True.

    Klic
        f.vrednost(dpll(f)) bo vrnil True (ce je problem resljiv).
    """""
    if verbose:
        print "Formula", f

    # Primer prazne formule
    if not f:
        return False

    # Pretvori v CNF
    f = convertToCNF(simplify_not(simplify(f))) #spremeni formulo v CNF obliko
    cnf_f = convert_to_CNF(f) #tole nam se dodatno pokrajsa formule (x in ne x), najbol poglavitno pa
                            #nastavi formulo v tako obliko da jo dpll prebavi.

    if verbose:
        print "CNF____", cnf_f

    # Primer tavtologije
    if isinstance(cnf_f, Tru):
        return True
    if isinstance(cnf_f,Fls):
        return False

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
        #neznane_vrednosti = set(v for stavek in cs for v in stavek.formule)
        neznane_vrednosti = set()
        for stavek in cs:
            for i in stavek.formule:
                if i not in v:
                    neznane_vrednosti.add(i)


        if verbose:
            print "Nezanane vrednosti", sorted(list(neznane_vrednosti))

        # Optimiziramo z sortiranjem seznama stavkov po velikosti (krajse stavke obdelamo prej)
        cs = sorted(cs, key=lambda x: len(x.formule))

        # Gremo cez stavke in obravnavmo primere
        ocisceni_cs = []
        for i, stavek in enumerate(cs):
            # Naletimo na prazen stavek --> false (ni resitve)
            if not stavek.formule:
                return False
            # Naletimo na seznam z enim elemetom [xi] (spremenljivka ali negacija)
            # znamo nastaviti xi
            if len(stavek.formule) == 1:
                lit = stavek.formule[0]
                if lit in v and v[lit] == Fls():
                    return False
                elif isinstance(lit, V) or isinstance(lit, Not):
                    v[lit] = Tru()
                    v[simplify_not(Not(lit))] = Fls()
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
        neznane_vrednosti = set()
        for stavek in cs:
            for i in stavek.formule:
                if i not in v:
                    neznane_vrednosti.add(i)
        if not neznane_vrednosti:
            return False
        else:
            xi = neznane_vrednosti.pop()
            xiN = simplify_not(Not(xi))
            if xiN in neznane_vrednosti:
                neznane_vrednosti.remove(xiN)
            v[xi] = Fls()
            v[xiN] = Tru()
            v1 = dpll_aux(v, cs, verbose)
            if not v1:
                v[xi] = Tru()
                v[xiN] = Fls()
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
                v[simplify_not(Not(var))] = Tru()

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
