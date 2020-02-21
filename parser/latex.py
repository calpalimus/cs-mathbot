import lark
from collections import namedtuple

@lark.v_args(inline=True)
class StringTransformer(lark.Transformer):
    Result = namedtuple('Result', ['op', 'expr'])

    def add(self, lhs, rhs):
        return self.Result('add', '%s + %s' % (lhs.expr, rhs.expr))

    def sub(self, lhs, rhs):
        if rhs.op in ('add', 'sub'):
            return self.Result('sub', '%s - (%s)' % (lhs.expr, rhs.expr))
        else:
            return self.Result('sub', '%s - %s' % (lhs.expr, rhs.expr))

    def div(self, lhs, rhs):
        return self.Result('div', '\\frac{%s}{%s}' % (lhs.expr, rhs.expr))

    def mul(self, *arguments):
        exprs = []
        for i, arg in enumerate(arguments):
            if arg.op in ('add', 'sub') or (i > 0 and arg.op == 'neg'):
                exprs.append('(%s)' % (arg.expr,))
            else:
                exprs.append(arg.expr)
        return self.Result('mul', ' '.join(exprs))

    def constant(self, CONSTANT):
        if CONSTANT.value == 'e':
            return self.Result('constant', 'e')
        else:
            return self.Result('constant', '\\%s' % (CONSTANT.value,))

    def neg(self, arg):
        return self.Result('neg', '-%s' % (arg.expr,))

    def exp(self, lhs, rhs):
        return self.Result('exp', '{%s}^{%s}' % (lhs.expr, rhs.expr))

    def function(self, FUNCTION, argument):
        if FUNCTION.value == 'abs':
            return self.Result('function', '\\lvert %s \\rvert' % (argument.expr))
        else:
            return self.Result('function', '\\%s(%s)' % (FUNCTION.value, argument.expr))

    def number(self, NUMBER):
        return self.Result('number', NUMBER.value)

    def variable(self, VARIABLE):
        return self.Result('variable', VARIABLE.value)

def ParseTreeToLaTeX(parse_tree):
    return StringTransformer().transform(parse_tree).expr

__all__ = [
    'ParseTreeToLaTeX',
]