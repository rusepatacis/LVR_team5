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

        #self.assertEqual(simplify(And([V("X"),Tru()])),V("X"))
        #self.assertEqual(simplify(Or([V("X"),Fls()])),V("X"))

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
        #self.assertEqual(simplify(Or([And([V("X"), Tru()]), Fls()])), V("X")) #(X in Tru) v Fls => X

        #self.assertEqual(simplify(And([Or([Not("P"),V("Q")], V("P"))])), And([V("Q",V("P"))]))
        print "Test medium finished."


if __name__ == '__main__':
    unittest.main()
