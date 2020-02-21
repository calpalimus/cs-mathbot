import lark

@lark.v_args(inline=True)
class StringTransformer(lark.Transformer):
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

__all__ = [
    'ParseTreeToString',
]