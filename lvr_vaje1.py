#coding:utf-8

__author__ = 'jaka'
"""
Naloga 1

Sestavite podatkovno strukturo ali razrede za predstavitev Boolovih formul (ki lahko vsebujejo spremenljivke).
Za osnovne logične veznike vzemite ⊥, ⊤, ¬, ∧, ∨. Sam se odločite, ali boste ⇒ predstavili kot osnovni veznik, ali ga prevedli na ostale.
Premisli: ali je bolje, da sprejmeta disjunkcija in konjunkcija dva parametra, ali poljuben seznam parametrov?
Če sprejmeta poljuben seznam parametrov, kaj pomeni konjukcija in disjunkcija praznega seznama?

Naloga 2
Sestavite funkcijo ali metodo, ki vrne vrednost Boolove formule pri danih vrednostih spremenljivk.
Na primer, formula (¬¬x∧y)∨¬x ima vrednost ⊤, če je x=⊥ in y=⊤.

Naloga 3
Sestavite funkcijo ali metodo za poenstavljanje Boolovih izrazov.
Na primer, izraz (x∧⊤)∨⊤ lahko poenostavimo v x. En način za poenostavljanje je naslednji:

    vse negacije "potisnemo" navznoter do spremenljivk in konstant
    dvojne negacije se izničijo
    rekurzivno poenostavimo podizraze, nato poenostavimo izraz

Pri tej nalogi je možnih precej različnih Viant. Sami premislite, kaj vse boste naredili.
"""

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
        return self.ime

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
        return "∧" + str(self.formule)

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
        return "∨" + str(self.formule)

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
        return "⇒" + str(self.formule)

    def vrednost(self, v):
        # p ---> q = NOTp or q
        b = self.formule[0]
        for p in self.formule[1:]:
            b = (not b) or p.vrednost(v)
        return b

    def __eq__(self, other):
        return str(self) == str(other)


def simplify(formula):
    print formula
    if formula.__class__.__name__ in ('V', 'Fls', 'Tru'):
        print "Tukaj sem"
        return formula
    elif formula.__class__.__name__ == 'Not':
        if formula.formula.__class__.__name__ == 'And':
            return Or([simplify(Not(p)) for p in formula.formula.formule])
        if formula.formula.__class__.__name__ == 'Or':
            return And([simplify(Not(p)) for p in formula.formula.formule])
        if formula.formula.__class__.__name__ == 'Not':
            return (simplify(formula.formula.formula))
        if formula.formula.__class__.__name__ in ('V', 'Fls', 'Tru'):
            return Not(formula.formula)
    elif formula.__class__.__name__  in ('And', 'Or'):
        temp = []
        for p in formula.formule:
            if p not in temp:
                temp.append(p)
        new = temp
        formula.formule = new
        return formula
    else:
        return formula

#Primer (naloga 2)
"""
moja_formula = And([V("p"), Not(V("p"))])

jani_formula = And([Imp([V("p"), V("q")]),
                    Imp([V("r"), V("q")])
                ])
print jani_formula
# Valuacija - implementiraj s pomočjo sloVja
v = {"p": True, "q": False, "r": True}

print "Vrednost za v:", jani_formula.vrednost(v)
"""

def v1():
    tabla = (And([Or([V("p"), V("q")]), Or([V("p"), V("r")])]))
    tabla = Or([Imp([V("p"), V("q")]), V("p"), Imp([V("p"), V("q")])])
    print tabla
    print simplify(tabla)


""" Naloga 3 - poenostavljanje"""
# Najprej potrebujemo funkcijo, ki vse negacije potisne navznoter - negation normal form -- nnf
# Sproti tudi poenostavimo dvojne negacije
# Tretja točka težja


"""
namig - sortiraj seznam spremenljivk -- na ta način lahko hitro pomečeš ven duplikate... v pythonu preprosto narediš množico


simplify

and [] -> True
and [q] -> simplfy(q)

"""

