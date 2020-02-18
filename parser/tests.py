import unittest
from . import parser

class TestParser(unittest.TestCase):
    def test_parser(self):
        tree = parser.parse('Hello, World!')
        print(tree)