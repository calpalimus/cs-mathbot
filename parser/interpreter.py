import os
import lark
from .evaluator import EvaluateExpression
from .output import ParseTreeToString

bot_parser = lark.Lark(
    open(os.path.join(os.path.dirname(__file__), 'grammar.lark')),
    lexer = 'standard',
    start = 'bot_command')

class BotCommand(lark.Visitor):
    def __init__(self):
        self.result = '???'
        self.assignments = {}
    
    def assignment(self, node):
        self.assignments[node.children[0].value] = EvaluateExpression(
            node.children[1],
            self.assignments)

    def cmd_evaluate(self, node):
        expression = node.children[1]

        try:
            self.result = str(EvaluateExpression(
                expression,
                self.assignments))
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
    'RunBotCommand',
]