__author__ = 'Jaka & Jani'
#coding UTF-8

from operands import *
from Simplify import *

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

