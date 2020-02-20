from lark import Lark, Transformer, Visitor, v_args, exceptions
import lark.exceptions
import os
import math
import sys

bot_parser = Lark(
    open(os.path.join(os.path.dirname(__file__), 'grammar.lark')),
    lexer = 'standard',
    start = 'bot_command')

parser = Lark(
    open(os.path.join(os.path.dirname(__file__), 'grammar.lark')),
    lexer = 'standard',
    start = 'expression')

@v_args(inline=True)
class StringTransformer(Transformer):
    def add(self, lhs, rhs):
        return '(+ %s %s)' % (lhs, rhs)

    def sub(self, lhs, rhs):
        return '(- %s %s)' % (lhs, rhs)

    def div(self, lhs, rhs):
        return '(/ %s %s)' % (lhs, rhs)

    def mul(self, *arguments):
        return '(* ' + ' '.join(arguments) + ')'

    def constant(self, CONSTANT):
        return '(%s)' % (CONSTANT.value,)

    def neg(self, arg):
        return '(- %s)' % (arg,)

    def exp(self, lhs, rhs):
        return '(^ %s %s)' % (lhs, rhs)

    def function(self, FUNCTION, argument):
        return '(%s %s)' % (FUNCTION.value, argument)

    def number(self, NUMBER):
        return NUMBER.value

    def variable(self, VARIABLE):
        return VARIABLE.value

def ParseTreeToString(parse_tree):
    return StringTransformer().transform(parse_tree)

class VariableCollector(Visitor):
    def __init__(self):
        self.vars = set()

    def variable(self, node):
        self.vars.add(node.children[0].value)
    
def GetVariables(parse_tree):
    collector = VariableCollector()
    collector.visit(parse_tree)
    return collector.vars

@v_args(inline=True)
class Evaluator(Transformer):
    def __init__(self, values):
        self.values = values

    def add(self, lhs, rhs):
        return lhs + rhs

    def sub(self, lhs, rhs):
        return lhs - rhs

    def div(self, lhs, rhs):
        return lhs / rhs

    def mul(self, *arguments):
        return_mul = 1.0
        for arg in arguments:
            return_mul = return_mul * arg
        return return_mul

    def constant(self, CONSTANT):
        if CONSTANT.value == "pi":
            return math.pi
        elif CONSTANT.value == "e":
            return math.e
        else:
            raise RuntimeError("Unknown constant " + CONSTANT.value)

    def neg(self, arg):
        return -arg

    def exp(self, lhs, rhs):
        return math.pow(lhs, rhs)

    def function(self, FUNCTION, argument):
        if FUNCTION.value == 'sin':
            return math.sin(argument)

        elif FUNCTION.value == 'cos':
            return math.cos(argument)

        elif FUNCTION.value == 'tan':
            return math.tan(argument)

        elif FUNCTION.value == 'sinh':
            return math.sinh(argument)

        elif FUNCTION.value == 'cosh':
            return math.cosh(argument)

        elif FUNCTION.value == 'tanh':
            return math.tanh(argument)
        
        elif FUNCTION.value == 'ln':
            return math.log(argument)

        elif FUNCTION.value == 'abs':
            return abs(argument)

        else:
            raise RuntimeError("Unknown function " + FUNCTION.value)

    def number(self, NUMBER):
        return float(NUMBER.value)

    def variable(self, VARIABLE):
        try:
            return self.values[VARIABLE.value]
        except KeyError:
            raise RuntimeError("Unknown variable " + VARIABLE.value)
   
def EvaluateExpression(parse_tree, values={}):
    evaluator = Evaluator(values)
    try:
        return evaluator.transform(parse_tree)
    except lark.exceptions.VisitError as e:
        raise e.orig_exc

class BotCommand(Visitor):
    def __init__(self):
        self.result = '???'
        self.assignments = {}
    
    def assignment(self, node):
        self.assignments[node.children[0].value] = EvaluateExpression(node.children[1], self.assignments)

    def cmd_evaluate(self, node):
        expression = node.children[1]

        try:
            self.result = str(EvaluateExpression(expression, self.assignments))
        except RuntimeError as e:
            self.result = 'Error: ' + str(e)

    def cmd_show(self, node):
        self.result = ParseTreeToString(node.children[1])

def RunBotCommand(command):
    try:
        tree = bot_parser.parse(command)
        evaluator = BotCommand()
        evaluator.visit(tree)
        return evaluator.result
    except lark.exceptions.UnexpectedInput as e:
        return str(e)
    return 'Done'

__all__ = [
    'parser',
    'bot_parser',
    'ParseTreeToString',
    'GetVariables',
    'EvaluateExpression',
    'RunBotCommand',
]