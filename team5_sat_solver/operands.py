__author__ = 'Jaka & Jani'
#coding: UTF-8

""" Osnovni logicni operandi, ki jih uporabljamo za konstrukcijo formul. """

"""
Razred, ki predstavlja logicni FALSE (0).
Uporaba: Fls()
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


"""
Razred, ki predstavlja logicni TRUE (1).
Uporaba: Tru()
"""


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

"""
Razred, ki predstavlja spremenljivko v logicnem izrazu.
Uporaba: V('X'); X := spremenljivka
"""


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

"""
Logicna negacija.
Uporaba: Not(formula); Formula je lahko logicen izraz, ali spremenljivka.
"""


class Not:
    def __init__(self, p):
        self.formula = p

    def __repr__(self):
        return "[NOT](" + str(self.formula)+')'

    def vrednost(self, v):
        return not(self.formula.vrednost(v))

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(repr(self))

"""
Logicen konjunkcija (in).
Uporaba: And([formula,formula]); Konjunkciji znotraj seznama podamo izraze/spremenljivke, ki jih povezuje.
Opomba: Lahko dodamo, več kot 2 izraza. Npr: And([x,y,z]) -> (x in y in z)
"""


class And:
    def __init__(self, ps):
        self.formule = ps

    def __repr__(self):
        return "(%s)" % (" [AND] ".join(str(f) for f in self.formule))

    def vrednost(self, v):
        b = True
        for p in self.formule:
            b = b and p.vrednost(v)
            if not b:
                break
        return b

    def __eq__(self, other):
        return str(self) == str(other)


"""
Logicen disjunkcija (ali).
Uporaba: Or([formula,formula]); Disjunkcija znotraj seznama podamo izraze/spremenljivke, ki jih povezuje.
Opomba: Lahko dodamo več kot 2 izraza. Npr: Or([x,y,z]) -> (x ali y ali z)
"""


class Or:
    def __init__(self, ps):
        self.formule = ps

    def __repr__(self):
        return "(%s)" % (" [OR] ".join(str(f) for f in self.formule))

    def vrednost(self, v):
        b = False
        for p in self.formule:
            b = b or p.vrednost(v)
            if b:
                break
        return b

    def __eq__(self, other):
        return str(self) == str(other)


"""
Logicna implikacija.
Implementirana je z uporabo negacije.

Uporaba: Imp(p,q); kjer sta p in q formuli ali spremenljivki.
"""


class Imp(Or):
    """
    Implcation
    """
    def __init__(self, p, q):
        self.p = p
        self.q = q
        Or.__init__(self, [Not(p), q])

    def __repr__(self):
        return str(self.p) + " [=>] " + str(self.q)

"""
Logicna ekvivalenca.
Implementirana je z uporabo negacije, konjunkcije in disjunkcije.

Uporaba: Equiv(p,q); p in q sta lahko formuli ali spremenljivki.
"""


class Equiv(And):
    """
    Logical equivalence
    """
    def __init__(self, p, q):
        self.p = p
        self.q = q
        And.__init__(self, [Or([Not(p), q]), Or([p, Not(q)])])

    def __repr__(self):
        return str(self.p) + " [<=>] " + str(self.q)


"""
Ekskluzivni ali.
Implementiran z uporabo negacije, disjunkcije in konjunkcije.

Uporaba: XOR(p,q); p in q sta lahko spremenljivki ali formuli.
"""


class XOR(And):

    def __init__(self, p, q):
        self.p = p
        self.q = q
        And.__init__(self, [Or([Not(p), Not(q)]), Or([p, q])])

    def __repr__(self):
        return str(self.p) + " [XOR] " + str(self.q)