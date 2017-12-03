from random import choice
import copy


class Node:
    def __init__(self, val, l=None, r=None):
        self.val = val
        self.l = l
        self.r = r

    def eval(self):
        pass

    def serialize(self):
        pass

    def replace(self, node):
        self.__class__ = node.__class__
        self.l = node.l
        self.r = node.r
        self.val = node.val

    def copy(self):
        return copy.deepcopy(self)


class NumNode(Node):

    def __init__(self, val):
        super().__init__(val)

    def __str__(self):
        return str(self.val)

    def eval(self):
        return self.val

    def serialize(self):
        return [self]


class OpNode(Node):

    def __init__(self, val, l, r):
        super().__init__(val, l, r)

    def __str__(self):
        return "(" + str(self.l) + " " + str(self.val) + " " + str(self.r) + ")"

    def eval(self):
        if self.val == '+':
            return self.l.eval() + self.r.eval()
        elif self.val == '-':
            return self.l.eval() - self.r.eval()
        elif self.val == '*':
            return self.l.eval() * self.r.eval()

    def serialize(self):
        return self.l.serialize() + [self] + self.r.serialize()


class Tree:

    def __init__(self, depth, terminals):
        self.depth = depth
        self.terminals = terminals
        self.ops = ['+', '-', '*']

    def create_tree(self):
        def recursion(depth):
            if depth > 0:
                return OpNode(choice(self.ops), recursion(depth-1), recursion(depth-1))
            else:
                return NumNode(choice(self.terminals))

        return recursion(self.depth)
