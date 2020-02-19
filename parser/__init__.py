from lark import lark
import os

parser = lark.Lark(
    open(os.path.join(os.path.dirname(__file__), 'grammar.lark')),
    lexer = "standard")


__all__ = [
    'parser'
]