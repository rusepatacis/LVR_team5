__author__ = 'Jaka & Jani'
#coding: UTF-8

from operands import *


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
    nobeno_dvakrat = And([And([Not(And([spremenljivke[(v, par_barv[0])], spremenljivke[(v, par_barv[1])]]))
                               for par_barv in pari_barv]) for v in vozlisca])

    # Povezani vozlišči nista iste barve
    povezani_nista_iste = And([[Not(And([spremenljivke[(vi, k)], spremenljivke[(vj, k)]])) for k in barve]
                               for (vi, vj) in G])

    # Prevedba je konjunkcija pogojev
    return And([vsaj_ena_barva, nobeno_dvakrat, povezani_nista_iste])
