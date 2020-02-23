import os
import lark
import discord
from .evaluator import EvaluateExpression
from .output import ParseTreeToString
from .latex import ParseTreeToLaTeX
from graphics.latex import GeneratePNGFromLaTeX
from graphics.plot import Plot2D
from .transformers import Simplify

bot_parser = lark.Lark(
    open(os.path.join(os.path.dirname(__file__), 'grammar.lark')),
    lexer = 'standard',
    start = 'bot_command')

class BotCommand(lark.Visitor):
    def __init__(self):
        self.result = '???'
        self.assignments = {}
        self.ranges = {}

    def range(self, node):
        self.ranges[node.children[0].value] = (
            EvaluateExpression(node.children[1], self.assignments),
            EvaluateExpression(node.children[2], self.assignments)
        )

    def assignment(self, node):
        self.assignments[node.children[0].value] = EvaluateExpression(
            node.children[1],
            self.assignments)

    def cmd_graph(self, node):
        expression = node.children[1]
        if len(self.ranges) != 1:
            self.result = "Can only plot 2D graphs."
            return
        range_var = list(self.ranges.keys())[0]
        range_low = self.ranges[range_var][0]
        range_high = self.ranges[range_var][1]
        points = []
        num_points = 1000
        step = (range_high - range_low) / num_points

        assignments = dict(self.assignments)
        for i in range(0, num_points + 1):
            x = range_low + i * step
            assignments[range_var] = x
            try:
                y = EvaluateExpression(expression, assignments)
                points.append((x,y)) 
            except:
                pass

        png = Plot2D(
            points, 
            '$%s$' % (range_var,), 
            '$f(%s)$' % (range_var,), 
            '$f(x) = %s$' % (ParseTreeToLaTeX(expression),))
        if png is not None:
            self.result = discord.File(png,"graph.png")
        else: 
            self.result = "Failed."

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
    
    def cmd_latex(self, node):
        self.result = self.ExprToPNG(node.children[1])
    
    def ExprToPNG(self, node):
        latex_expression = ParseTreeToLaTeX(node)
        png = GeneratePNGFromLaTeX(latex_expression)
        if png is not None:
            return discord.File(png,"input.png")
        else: 
            raise RuntimeError("Failed")        
    
    def cmd_simplify(self, node):
        simplified_expression = Simplify(node.children[1])
        self.result = self.ExprToPNG(simplified_expression)

def RunBotCommand(command):
    try:
        tree = bot_parser.parse(command)
        evaluator = BotCommand()
        evaluator.visit(tree)
        return evaluator.result
    except lark.exceptions.UnexpectedInput as e:
        return str(e)
    except RuntimeError as e:
        return str(e)
    return 'Done'

__all__ = [
    'RunBotCommand',
]