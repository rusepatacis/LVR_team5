__author__ = 'jaka.demsar0@gmail.com'
# coding: utf-8

"""
    Mešani primeri za preizkušanje.
"""

from sat_solver import V, And, Or, Not, XOR, Imp, Tru, Fls

pr = []

t1 = Not(
        Or([
            And([
            Or([V("p"), V("q")]),
            Or([V("p"), V("r")])]),
                And([Not(V("a")), V("b")])
        ])
     )

pr.append(t1)

t2 = And([
        Or([
            Tru(),
            V("q"),
            V("p"),
            V("r"),
        Not(V("a")),
            V("b")
        ]),

        Or([
            V("c"),
            V("x"),
            V("w")
        ])
        ]
     )

pr.append(t2)

t3 = And([
        Or([
            Tru(),
            V("q"),
            V("p"),
            V("r"),
        Not(V("a")),
            V("b")
        ]),

        Or([
            V("c"),
            V("x"),
            V("w")
        ]),
        Or([
            V("a"),
            V("b"),
            And([
                Or([V("c"), V('a'), V('x')]),
                V('z'),
                V('w')
            ])
        ])
        ]
     )

pr.append(t3)
