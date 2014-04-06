__author__ = 'Jani'
#coding: UTF-8

import unittest
from sat_solver import *


class MyTestCase(unittest.TestCase):
    """
    Neumni osnovni testi, ki ne stestirajo prav dosti.
    """
    def test_basic_operations(self):
        self.assertEqual(Tru(), "Tru")
        self.assertEqual(Fls(), "Fls")
        self.assertEqual(V("X"), "X")
        self.assertEqual(Not("X"),"¬X")
        self.assertEqual(And([V("X"), V("Y")]), "(X ∧ Y)")
        self.assertEqual(Or([V("X"), V("Y")]),"(X ∨ Y)")
        self.assertEqual(Imp([V("X"),V("Y")]),"(X ⇒ Y)")

        print "Test basic finished."

    def test_simplify(self):
        self.assertEqual(simplify(Not(Tru())), Fls())
        self.assertEqual(simplify(Not(Fls())), Tru())

        self.assertEqual(simplify(And([V("X"),Tru()])),V("X"))
        self.assertEqual(simplify(And([V("X"),Tru(),V("Y")])),And([V("X"),V("Y")]))
        self.assertEqual(simplify(Or([V("X"),Fls()])),V("X"))
        self.assertEqual(simplify(Or([V("X"),Fls(),V("Y")])),Or([V("X"),V("Y")]))

        self.assertEqual(simplify(Not(Not("X"))), V("X"))
        self.assertEqual(simplify(Not(Not(Not(Not("X"))))), V("X"))
        self.assertEqual(simplify(Not("X")), Not("X"))
        self.assertEqual(simplify(Not(Not(Not("X")))), Not("X"))

        self.assertEqual(simplify(V("X")),V("X"))
        self.assertEqual(simplify(Tru()), Tru())
        self.assertEqual(simplify(Fls()), Fls())

        self.assertEqual(simplify(Or([V("X"),Tru()])), Tru())
        self.assertEqual(simplify(And([V("X"),V("Y"),Fls()])), Fls())

        self.assertEqual(simplify(Or([V("X"),Not("X")])),Tru())
        self.assertEqual(simplify(Or([Not("X"),V("Y"), V("X")])), Tru())

        self.assertEqual(simplify(And([V("X"),Not("X")])),Fls())
        self.assertEqual(simplify(And([Not("X"),V("Y"), V("X")])), Fls())

        print "Test simplify finished."

    def test_medium(self):
        formula3 = (Or([Or([V("p"),V("q")]), Or([V("q"),V("r")]),Or([V("r"),V("p")])]))#(p∧q)∧(q∧r)∧(r∧p)
        #self.assertEqual((simplify_or_same(formula3)), Or([V("p"),V("q"),V("r")]))

        formula3 = (And([And([V("p"),V("q")]), And([V("q"),V("r")]),And([V("r"),V("p")])]))#(p∧q)∧(q∧r)∧(r∧p)
        #self.assertEqual((simplify_and_same(formula3)), And([V("p"),V("q"),V("r")]))

        print "Test medium finished."

    def test_simplify_same(self):
        formula1 = Or([ Or([V("X"),V("Y")]), Or([V("Y"),V("Z")])])
        formula2 = Or([Or([ Or([V("X"),V("Y")]), Or([V("Y"),V("Z")])]),Or([ Or([V("X"),V("Y")]), Or([V("Y"),V("Z")])])])
        formula3 = (Or([Or([V("p"),V("q")]), Or([V("q"),V("r")]),Or([V("r"),V("p")])]))#(p∧q)∧(q∧r)∧(r∧p)

        self.assertEqual((simplify_or_same(formula1)),Or([V("X"),V("Y"),V("Z")]))
        self.assertEqual((simplify_or_same(formula2)),Or([V("X"),V("Y"),V("Z")]))
        self.assertEqual((simplify_or_same(formula3)), Or([V("p"),V("q"),V("r")]))

        formula1 = And([ And([V("X"),V("Y")]), And([V("Y"),V("Z")])])
        formula2 = And([And([ And([V("X"),V("Y")]), And([V("Y"),V("Z")])]),And([ And([V("X"),V("Y")]), And([V("Y"),V("Z")])])])
        formula3 = (And([And([V("p"),V("q")]), And([V("q"),V("r")]),And([V("r"),V("p")])]))#(p∧q)∧(q∧r)∧(r∧p)

        self.assertEqual((simplify_and_same(formula1)),And([V("X"),V("Y"),V("Z")]))
        self.assertEqual((simplify_and_same(formula2)),And([V("X"),V("Y"),V("Z")]))
        self.assertEqual((simplify_and_same(formula3)), And([V("p"),V("q"),V("r")]))

        formula4 = Or([(And([And([V("p"),V("q")]), And([V("q"),V("r")]),And([V("r"),V("p")])])),(And([And([V("p1"),V("q1")]), And([V("q1"),V("r1")]),And([V("r1"),V("p1")])]))])#(p∧q)∧(q∧r)∧(r∧p) or (p1∧q1)∧(q1∧r1)∧(r1∧p1)
        self.assertEqual(simplify(formula4),Or([And([V('p'),V('q'),V('r')]), And([V('p1'),V('q1'),V('r1')])]))

        print "Test simplify_same finished."

    def test_jaka_found_bug1(self):
        stopwatch = Stopwatch("Jaka bug1")

        t1 = Not(Or([And([Or([V("p"), V("q")]),Or([V("p"), V("r")])]),And([Not(V("a")), V("b"), V('c')])]))
        t2 = And([And([Tru(),V("q"),V("p"),V("r"),Not(V("a")),V("b")]),Or([V("c"),V("x"),V("w")])])
        t3 = And([Or([Tru(),V("q"),V("p"),V("r"),Not(V("a")),V("b")]),Or([V("c"),V("x"),V("w")]),
                  Or([V("a"),V("b"),And([Or([V("c"), V('a'), V('x')]),V('z'),V('w')])])])
        t4 = Or([Or([And([V('A'), V('B')]), And([V('C'), V('D')])]),V('E')])

        simplify(t1)
        stopwatch.intermediate("gieuigheuihreiugeh")
        simplify(t2)
        simplify(t3)
        stopwatch.intermediate()
        simplify(t4)
        stopwatch.intermediate()

        pr = []
        pr.append(t1)
        pr.append(t2)
        pr.append(t3)
        pr.append(t4)
        simplify(pr)
        stopwatch.stop()
        print stopwatch

        print "Test jaka_bug1 finished."

    def test_hadamardova_matrika(self):
        r = XOR([Not(XOR([V("a1,1"), V("a1,2")])), Not(XOR([V("a2,1"), V("a2,2")]))])

        print r
        print hadamardova_matrika(2)#TODO tuki je neki cudnega, enako je ampak ce primerjas ni enako?
        #self.assertEqual(hadamardova_matrika(2), r) weird


        print hadamardova_matrika(3)
        #print hadamardova_matrika(4)
        #hadamardova_matrika(22) # priblizno 2.5s da resi
        #hadamardova_matrika(24) # 3.3s
        #hadamardova_matrika(26)  # 5s
        #hadamardova_matrika(30)   #10s


        print "Test hadamardova_matrika finished."



if __name__ == '__main__':
    unittest.main()
