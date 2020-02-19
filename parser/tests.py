import unittest
from . import parser

class TestParser(unittest.TestCase):
    def check_parses(self, string):
        tree = parser.parse(string)
        # print(tree.pretty())

    def test_expressions(self):
        self.check_parses('2')
        self.check_parses('2.0')
        self.check_parses('x')
        self.check_parses("-x")
        self.check_parses('sin(x)')
        self.check_parses('pi')
        self.check_parses('x^2')
        self.check_parses('2a')
        self.check_parses('2ax')
        self.check_parses('2a^2')
        self.check_parses('2a^2x')
        self.check_parses('2sin(x)cos(y)')
        self.check_parses('sinh(x)')
        self.check_parses('((x))')
        self.check_parses('(y(x))')
        self.check_parses('2-3')
        self.check_parses('a-b-c')
        self.check_parses('a-(b-c)')
        self.check_parses('2--3')
        self.check_parses('x-y')
        self.check_parses('x^(-y)')
        self.check_parses('x^(5-y)')
        self.check_parses('a/b/c')
        self.check_parses('1*2*3')
        self.check_parses('2+3/4')
        self.check_parses('2/xy')
        self.check_parses('2/x*y')
        self.check_parses('ln(abs(x))')