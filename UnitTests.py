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
        self.assertEqual(And([V("X"), V("Y")]), "∧[X, Y]")
        self.assertEqual(Or([V("X"), V("Y")]),"∨[X, Y]")
        self.assertEqual(Imp([V("X"),V("Y")]),"⇒[X, Y]")

    def test_simplify(self):
        self.assertEqual(simplify(Not(Tru())), "Fls")
        self.assertEqual(simplify(Not(Fls())), "Tru")

        self.assertEqual(simplify(Not(Not("X"))), "X")
        self.assertEqual(simplify(Not(Not(Not(Not("X"))))), "X")
        self.assertEqual(simplify(Not("X")), "¬X")
        self.assertEqual(simplify(Not(Not(Not("X")))), "¬X")

        self.assertEqual(simplify(V("X")),"X")
        self.assertEqual(simplify(Tru()),"Tru")
        self.assertEqual(simplify(Fls()), "Fls")

        self.assertEqual(simplify(Or([V("X",Tru())])), Tru())





if __name__ == '__main__':
    unittest.main()
