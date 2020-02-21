import lark
import os

from . import evaluator, interpreter, output, latex

parser = lark.Lark(
    open(os.path.join(os.path.dirname(__file__), 'grammar.lark')),
    lexer = 'standard',
    start = 'expression')

__all__ = [
    'parser',
    'evaluator',
    'interpreter',
    'output',
    'latex',
]