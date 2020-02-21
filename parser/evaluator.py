import lark
import math

@lark.v_args(inline=True)
class Evaluator(lark.Transformer):
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

class VariableCollector(lark.Visitor):
    def __init__(self):
        self.vars = set()

    def variable(self, node):
        self.vars.add(node.children[0].value)
    
def GetVariables(parse_tree):
    collector = VariableCollector()
    collector.visit(parse_tree)
    return collector.vars

__all__ = [
    'EvaluateExpression',
    'GetVariables',
]