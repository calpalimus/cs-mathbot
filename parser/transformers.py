import lark
import math

def IsNumberNode(node):
    if node.data == 'neg':
        return IsNumberNode(node.children[0])
    if node.data == 'number':
        return True
    return False

def GetNumberValue(node):
    if node.data == 'neg':
        return -GetNumberValue(node.children[0])
    if node.data == 'number':
        value = node.children[0].value
        try:
            value = int(value)
        except:
            value = float(value)
        return value
    raise RuntimeError('Not a constant node')

def MakeNumberNode(value):
    return lark.Tree('number', [ lark.Token('NUMBER', str(value)) ])

@lark.v_args(tree=True)
class RemoveSub(lark.Transformer):
    def sub(self, node):
        l,r = node.children
        return lark.Tree('add', [l, lark.Tree('neg', [r])])

@lark.v_args(tree=True)
class MoveNumbersLeft(lark.Transformer):
    def sub(self, node):
        l,r = node.children
        if not IsNumberNode(l) and IsNumberNode(r):
            return lark.Tree(
                'add',
                [ lark.Tree('neg', [r]), l ]
            )
        return node

    def add(self, node):
        l,r = node.children
        if not IsNumberNode(l) and IsNumberNode(r):
            node.children = [r, l]
        return node

    def mul(self, node):
        constant_children = [ child for child in node.children if IsNumberNode(child) ]
        variable_children = [ child for child in node.children if not IsNumberNode(child) ]
        node.children = constant_children + variable_children
        return node

@lark.v_args(tree=True)
class LowerNeg(lark.Transformer):
    def negateNode(self, node):
        if node.data == 'neg':
            return node.children[0]
        elif node.data in ('add', 'sub'):
            node.children = [ self.negateNode(c) for c in node.children ]
            return node
        elif node.data in ('mul', 'div'):
            node.children[0] = self.negateNode(node.children[0])
            return node
        else:
            return lark.Tree('neg', [ node ])

    def neg(self, node):
        c = node.children[0]
        if c.data in ('add', 'sub', 'mul', 'div', 'neg'):
            return self.negateNode(c)
        else:
            return node

@lark.v_args(tree=True)
class AdditionSimplification(lark.Transformer):
    def add(self, node):
        l,r = node.children

        children_to_add = []
        if l.data == 'add':
            children_to_add.extend(l.children)
        else:
            children_to_add.append(l)

        if r.data == 'add':
            children_to_add.extend(r.children)
        else:
            children_to_add.append(r)

        constant_children = [ child for child in children_to_add if IsNumberNode(child) ]
        variable_children = [ child for child in children_to_add if not IsNumberNode(child) ]

        if len(constant_children) > 1:
            values = [ GetNumberValue(child) for child in constant_children ]
            if sum(values) == 0:
                constant_children = []
            else:
            constant_children = [ MakeNumberNode(sum(values)) ]

        children_to_add = constant_children + variable_children

        while len(children_to_add) > 1:
            new_node = lark.Tree('add', children_to_add[-2:])
            children_to_add = children_to_add[:-2] + [ new_node ]

        return children_to_add[0]


def Simplify(parse_tree):
    parse_tree = RemoveSub().transform(parse_tree)
    parse_tree = LowerNeg().transform(parse_tree)
    parse_tree = MoveNumbersLeft().transform(parse_tree)
    parse_tree = AdditionSimplification().transform(parse_tree)
        #simplifier = AdditionSimplification()
    #return simplifier.transform(parse_tree)
    return parse_tree


__all__ = [
    'Simplify',
]