__author__ = 'Jani'
#coding: UTF-8

import unittest

from dpll import dpll
from team5_sat_solver.sat_prevedbe.hadamard import hadamardova_matrika
from operands import *
from simplify import push_not, simplify_not, simplify, simplify_and_same, simplify_or_same
from utils import Stopwatch


class MyTestCase(unittest.TestCase):
    """
    Neumni osnovni testi, ki ne stestirajo prav dosti.
    Preverijo ali spremembe osnovnih operatorjev se vedno podajo pricakovano vrednost.
    """
    def test_basic_operations(self):
        st = Stopwatch("Basic test")
        self.assertEqual(Tru(), "Tru")
        self.assertEqual(Fls(), "Fls")
        self.assertEqual(V("X"), "X")
        self.assertEqual(Not("X"), "[NOT](X)")
        self.assertEqual(And([V("X"), V("Y")]), "(X [AND] Y)")
        self.assertEqual(Or([V("X"), V("Y")]), "(X [OR] Y)")
        self.assertEqual(Imp(V("X"), V("Y")), "X [=>] Y")    # TODO to neki cudno izpise z asci kodo
        st.stop()
        print st

    def test_simplify(self):
        """
        Testira osnovne (lahke) primere krajsanja formule.
        """
        st = Stopwatch("Simplify")

        self.assertEqual(simplify(Not(Tru())), Fls())
        self.assertEqual(simplify(Not(Fls())), Tru())

        self.assertEqual(simplify(And([V("X"), Tru()])), V("X"))
        self.assertEqual(simplify(And([V("X"), Tru(), V("Y")])), And([V("X"), V("Y")]))
        self.assertEqual(simplify(Or([V("X"), Fls()])), V("X"))
        self.assertEqual(simplify(Or([V("X"), Fls(), V("Y")])), Or([V("X"), V("Y")]))

        self.assertEqual(simplify(Not(Not("X"))), V("X"))
        self.assertEqual(simplify(Not(Not(Not(Not("X"))))), V("X"))
        self.assertEqual(simplify(Not("X")), Not("X"))
        self.assertEqual(simplify(Not(Not(Not("X")))), Not("X"))

        self.assertEqual(simplify(V("X")), V("X"))
        self.assertEqual(simplify(Tru()), Tru())
        self.assertEqual(simplify(Fls()), Fls())

        self.assertEqual(simplify(Or([V("X"), Tru()])), Tru())
        self.assertEqual(simplify(And([V("X"), V("Y"), Fls()])), Fls())

        self.assertEqual(simplify(Or([V("X"), Not("X")])), Tru())
        self.assertEqual(simplify(Or([Not("X"), V("Y"), V("X")])), Tru())

        self.assertEqual(simplify(And([V("X"), Not("X")])), Fls())
        self.assertEqual(simplify(And([Not("X"), V("Y"), V("X")])), Fls())

        st.stop()
        print st

    def test_medium(self):
        st = Stopwatch("Medium")
        formula3 = (Or([Or([V("p"), V("q")]), Or([V("q"), V("r")]), Or([V("r"), V("p")])]))  # (p∧q)∧(q∧r)∧(r∧p)
        self.assertEqual((simplify_or_same(formula3)), Or([V("p"), V("q"), V("r")]))
        formula3 = (And([And([V("p"), V("q")]), And([V("q"), V("r")]), And([V("r"), V("p")])]))   # (p∧q)∧(q∧r)∧(r∧p)
        self.assertEqual((simplify_and_same(formula3)), And([V("p"), V("q"), V("r")]))
        st.stop()
        print st

    def test_simplify_same(self):
        """
        Testira delovanje metode simplify_or_same ter simplify_and_same.
        """
        st = Stopwatch("Simplify same")

        formula1 = Or([Or([V("X"), V("Y")]), Or([V("Y"), V("Z")])])
        formula2 = Or([Or([Or([V("X"), V("Y")]), Or([V("Y"), V("Z")])]),
                       Or([Or([V("X"), V("Y")]), Or([V("Y"), V("Z")])])])
        formula3 = (Or([Or([V("p"), V("q")]), Or([V("q"), V("r")]), Or([V("r"), V("p")])]))     # (p∧q)∧(q∧r)∧(r∧p)

        self.assertEqual((simplify_or_same(formula1)), Or([V("X"), V("Y"), V("Z")]))
        self.assertEqual((simplify_or_same(formula2)), Or([V("X"), V("Y"), V("Z")]))
        self.assertEqual((simplify_or_same(formula3)), Or([V("p"), V("q"), V("r")]))

        formula1 = And([And([V("X"), V("Y")]), And([V("Y"), V("Z")])])
        formula2 = And([And([And([V("X"), V("Y")]),
                             And([V("Y"), V("Z")])]), And([And([V("X"), V("Y")]), And([V("Y"), V("Z")])])])
        formula3 = (And([And([V("p"), V("q")]), And([V("q"), V("r")]), And([V("r"), V("p")])]))   # (p∧q)∧(q∧r)∧(r∧p)

        self.assertEqual((simplify_and_same(formula1)), And([V("X"), V("Y"), V("Z")]))
        self.assertEqual((simplify_and_same(formula2)), And([V("X"), V("Y"), V("Z")]))
        self.assertEqual((simplify_and_same(formula3)), And([V("p"), V("q"), V("r")]))

        # (p∧q)∧(q∧r)∧(r∧p) or (p1∧q1)∧(q1∧r1)∧(r1∧p1)
        formula4 = Or([(And([And([V("p"), V("q")]),
                             And([V("q"), V("r")]),
                             And([V("r"), V("p")])])),
                       (And([And([V("p1"), V("q1")]),
                             And([V("q1"), V("r1")]),
                             And([V("r1"), V("p1")])]))])
        self.assertEqual(simplify(formula4), Or([And([V('p'), V('q'), V('r')]), And([V('p1'), V('q1'), V('r1')])]))

        st.stop()
        print st

    def test_jaka_found_bug1(self):
        """
        Testiranje buga, ki ga je nasel Jaka.
        """
        stopwatch = Stopwatch("Jaka bug1")

        t1 = Not(Or([And([Or([V("p"), V("q")]), Or([V("p"), V("r")])]), And([Not(V("a")), V("b"), V('c')])]))
        t2 = And([And([Tru(), V("q"), V("p"), V("r"), Not(V("a")), V("b")]), Or([V("c"), V("x"), V("w")])])
        t3 = And([Or([Tru(), V("q"), V("p"), V("r"), Not(V("a")), V("b")]), Or([V("c"), V("x"), V("w")]),
                  Or([V("a"), V("b"), And([Or([V("c"), V('a'), V('x')]), V('z'), V('w')])])])
        t4 = Or([Or([And([V('A'), V('B')]), And([V('C'), V('D')])]), V('E')])

        simplify(t1)
        simplify(t2)
        simplify(t3)
        stopwatch.intermediate()
        simplify(t4)
        stopwatch.intermediate()

        pr = [t1, t2, t3, t4]
        simplify(pr)
        stopwatch.stop()
        print stopwatch

    def test_hadamardova_matrika(self):
        """
        Testiranje hadamardove matrike.
        """
        st = Stopwatch("Hadamardova")

        print hadamardova_matrika(2)    # Testirano na roke, tale je ok.
        st.intermediate(2)
        print hadamardova_matrika(3)    # Ok.
        st.intermediate(3)
        print hadamardova_matrika(4)
        st.intermediate(4)
        hadamardova_matrika(6)
        st.intermediate(6)
        hadamardova_matrika(8)
        st.intermediate(8)
        hadamardova_matrika(10)
        st.intermediate(10)

        st.stop()
        print st

    def test_dpll(self):
        """
        Testiranje dpll.
        """
        f1 = And([V("X"), V("Y")])
        f2 = Not(Or([And([Or([V("p"), V("q")]), Or([V("p"), V("r")])]), And([Not(V("a")), V("b"), V('c')])]))
        f3 = And([V("X"), Not(V("X"))])
        f4 = Not(XOR(V("X"), V("Y")))
        f5 = Not(And([V("X"), V("Y")]))

        #print dpll(V("X"))#TODO tale ne dela
        self.assertEqual(dpll(f1), {"X": "Tru", "Y": "Tru"})
        print dpll(f2)
        print dpll(f3)
        print dpll(f5)

        had2 = hadamardova_matrika(2)
        hh = Or([And([XOR(V("a1,1"),V("a2,1")),Not(XOR(V("a1,2"),V("a2,2")))]),
                 And([Not(XOR(V("a1,1"),V("a2,1"))),XOR(V("a1,2"),V("a2,2"))])])
        print hh
        print had2
        print "--------------------------"
        print push_not(hh)
        print push_not(had2)
        print "+++++++++++++++++++++++++++", hh == had2,push_not(hh) == push_not(had2)

        had3 = XOR(Not(XOR(V("a1,1"), V("a1,2"))), Not(XOR(V("a2,1"), V("a2,2"))))

        print dpll(push_not(hh))
        print dpll(push_not(hadamardova_matrika(2)))

    def test_push_not(self):
        """
        Testiranje potiskanja negacije navznoter.
        """
        f0 = And([V("X"), V("Y")])
        f1 = Not(And([V("X"), V("Y")]))
        f2 = Not(Or([V("X"), V("Y")]))
        f3 = Imp(V("X"), V("Y"))
        f4 = Equiv(V("X"), V("Y"))
        f5 = XOR(V("X"), V("Y"))

        self.assertEqual(simplify_not(f0), f0)
        self.assertEqual(simplify_not(f1), Or([Not(V("X")), Not(V("Y"))]))
        self.assertEqual(simplify_not(f2), And([Not(V("X")), Not(V("Y"))]))
        self.assertEqual(simplify_not(Not(f3)), And([V("X"), Not(V("Y"))]))
        self.assertEqual(simplify_not(Not(f4)), Or([And([V("X"), Not(V("Y"))]), And([Not(V("X")), V("Y")])]))
        self.assertEqual(simplify_not(Not(f5)), Or([And([V("X"), V("Y")]), And([Not(V("X")), Not(V("Y"))])]))

        h2 = hadamardova_matrika(2)
        print h2
        print push_not(h2)

if __name__ == '__main__':
    unittest.main()
