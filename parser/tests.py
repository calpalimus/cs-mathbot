import unittest
from . import *

class TestParser(unittest.TestCase):
    def check_parses(self, string, expected = None):
        tree = parser.parse(string)
        self.assertEqual(output.ParseTreeToString(tree), expected)
    
    def test_simplify(self):
        self.assertEqual(
            output.ParseTreeToString(transformers.Simplify(parser.parse('3+4'))),
            '7')
        self.assertEqual(
            output.ParseTreeToString(transformers.Simplify(parser.parse('x+1'))),
            '(+ 1 x)'
            )
        self.assertEqual(
            output.ParseTreeToString(transformers.Simplify(parser.parse('(2-1)+(3+x)-(1-2)'))),
            '(+ 5 x)')
        self.assertEqual(
            output.ParseTreeToString(transformers.Simplify(parser.parse('(2-1)+(3+x)-(1-pi)'))),
            '(+ 3 (+ x (pi)))')

    def test_asLaTeX(self):
        self.assertEqual(
            latex.ParseTreeToLaTeX(parser.parse('abs(y) + (cos(x)+x^2)/2')),
            r'\lvert y \rvert + \frac{\cos(x) + {x}^{2}}{2}')

    def test_getVariables(self):
        self.assertEqual(evaluator.GetVariables(parser.parse('2x^2+5y')), {'x','y'})
    
    def test_evaluateExpression(self):
        self.assertEqual(
            evaluator.EvaluateExpression(parser.parse('sin(1/2*pi)')),
            1)
        self.assertEqual(
            evaluator.EvaluateExpression(parser.parse('x^2-y'), {'x':5, 'y':2}),
            23)

    def test_runBotCommand(self):
        self.assertEqual(interpreter.RunBotCommand('$evaluate x^y: x=2, y=x+1'), '8.0')

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