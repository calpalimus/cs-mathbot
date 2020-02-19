import unittest
from . import parser, ParseTreeToString

class TestParser(unittest.TestCase):
    def check_parses(self, string, expected = None):
        tree = parser.parse(string)
        print(ParseTreeToString(tree))
        self.assertEquals(ParseTreeToString(tree), expected)

    def test_expressions(self):
        self.check_parses('2.0',           '2.0')
        self.check_parses('2',             '2')
        self.check_parses('x',             'x')
        self.check_parses('-x',            '(- x)')
        self.check_parses('sin(x)',        '(sin x)')
        self.check_parses('pi',            '(pi)')
        self.check_parses('x^2',           '(^ x 2)')
        self.check_parses('2a',            '(* 2 a)')
        self.check_parses('2ax',           '(* 2 a x)')
        self.check_parses('2a^2',          '(* 2 (^ a 2))')
        self.check_parses('2a^2x',         '(* 2 (^ a 2) x)')
        self.check_parses('2sin(x)cos(y)', '(* 2 (sin x) (cos y))')
        self.check_parses('sinh(x)',       '(sinh x)')
        self.check_parses('((x))',         'x')
        self.check_parses('(y(x))',        '(* y x)')
        self.check_parses('2-3',           '(- 2 3)')
        self.check_parses('a-b-c',         '(- (- a b) c)')
        self.check_parses('a-(b-c)',       '(- a (- b c))')
        self.check_parses('2--3',          '(- 2 (- 3))')
        self.check_parses('x-y',           '(- x y)')
        self.check_parses('x^(-y)',        '(^ x (- y))')
        self.check_parses('x^(5-y)',       '(^ x (- 5 y))')
        self.check_parses('a/b/c',         '(/ (/ a b) c)')
        self.check_parses('1*2*3',         '(* (* 1 2) 3)')
        self.check_parses('2+3/4',         '(+ 2 (/ 3 4))')
        self.check_parses('2/xy',          '(/ 2 (* x y))')
        self.check_parses('2/x*y',         '(* (/ 2 x) y)')
        self.check_parses('ln(abs(x))',    '(ln (abs x))')