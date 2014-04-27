__author__ = 'Jaka & Jani'
#coding: UTF-8

from operands import *


def simplify(formula, verbose=False):
    """"
    Metoda namenjena poenostavljanju logicnih izrazov.
    Kot parameter sprejme logicno formulo (izraz) ter ga poskusa poenostaviti. Deluje na rekurziven nacin.
    Zastavica verbose doloca izpis sledi funkcije.
    Vrne poenostavljeno fomrulo.
    """""
    if verbose:
        print "\t\t", formula, formula.__class__
    if formula.__class__.__name__ in ('V', 'Fls', 'Tru'):
        if verbose:
            print "Spremenljivka/Fls/Tru", formula
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
        return simplify_not(formula)
    elif formula.__class__.__name__ in ('And', 'Or'):
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
                for b in range(a+1, len(formula.formule)):
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
                for b in range(a+1, len(formula.formule)):
                    if simplify(formula.formule[a]) == simplify(Not(formula.formule[b])):
                        return Tru()

        formula = simplify_and_same(formula)
        formula = simplify_or_same(formula)

        temp = []
        for p in formula.formule:#vsako notranjo formulo je tudi potrebno preveriti
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
    """"
    Podmetoda metode simplify.
    Pokrajsa vgnezdene disjunkcije (Or).
    Npr: (X ali Y) ali (X ali Z) -> (X ali Y ali Z)

    Lahko resi tudi mesane izraze (konjunkcije in disjunkcije)
    """""
    if formula.__class__.__name__ in ('V', 'Not'):
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
    """"
    Podmetoda metode simplify.
    Pokrajsa vgnezdene konjunkcije (And).

    Npr: (X in Y) in (X in Z) -> (X in Y in Z)

    Lahko resi tudi mesane izraze (konjunkcije in disjunkcije)
    """""
    if formula.__class__.__name__ in ('V', 'Not'):
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

                if tmpFormula.__class__.__name__ == 'V':
                    temp.append(tmpFormula)
                    continue
                for form2 in tmpFormula.formule:
                    if form2 not in temp:
                        temp.append(form2)

            formula.formule = temp
        return formula
    return formula


def simplify_not(formula):
    """"
    Porine negacije navznoter do spremenljivk.
    Ta del metode dobi dobi celoten izraz (formulo), katero nato rekurzivno razcleni.
    Ce naleti na negacijo, porine ta del formule metodi "push not".
    """""
    if formula.__class__.__name__ == 'Not':
        return push_not(formula.formula)
    elif formula.__class__.__name__ == 'V':
        return formula
    elif formula.__class__.__name__ == 'And':
        tmpFormula = []
        for f in formula.formule:
            tmpFormula.append(simplify_not(f))
        return And(tmpFormula)
    elif formula.__class__.__name__ == 'Or':
        tmpFormula = []
        for f in formula.formule:
            tmpFormula.append(simplify_not(f))
        return Or(tmpFormula)
    elif formula.__class__.__name__ == 'Imp':
        return Imp(simplify_not(formula.p), simplify_not(formula.q))
    elif formula.__class__.__name__ == 'Equiv':
        return Equiv(simplify_not(formula.p), simplify_not(formula.q))
    elif formula.__class__.__name__ == 'XOR':
        return XOR(simplify_not(formula.p), simplify_not(formula.q))

    print "Unknown operator"
    return formula


def push_not(formula):
    """"
    Porine negacije navznoter do spremenljivk.
    Ta del metode predpostavi, da je prejsnji operand negacija. Glede na naslednji operand nato
    ustrezno porine negacijo navznoter, ter se rekurzivno klice naprej.
    Ce naleti na dvojno negacijo jo iznici (pokrajsa).
    """""
    if formula.__class__.__name__ == 'V':
        return Not(formula)
    elif formula.__class__.__name__ == 'And':
        tempFormula = []
        for form in formula.formule:
            tempFormula.append(push_not(form))
        return Or(tempFormula)
    elif formula.__class__.__name__ == 'Or':
        tempFormula = []
        for form in formula.formule:
            tempFormula.append(push_not(form))
        return And(tempFormula)
    elif formula.__class__.__name__ == 'Not':
        return simplify_not(formula.formula)
    elif formula.__class__.__name__ == 'Imp':
        tmp = And([formula.p, Not(formula.q)])
        return simplify_not(tmp)
    elif formula.__class__.__name__ == 'Equiv':
        tmp = Or([And([formula.p, Not(formula.q)]), And([Not(formula.p), formula.q])])
        return simplify_not(tmp)
    elif formula.__class__.__name__ == 'XOR':
        tmp = Or([And([formula.p, formula.q]), And([Not(formula.p), Not(formula.q)])])
        return simplify_not(tmp)
