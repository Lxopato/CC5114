from random import choice


class Node:
    def __init__(self, val, l=None, r=None):
        self.val = val
        self.l = l
        self.r = r

    def eval(self):
        pass


class NumNode(Node):

    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def eval(self):
        return self.val


class OpNode(Node):

    def __init__(self, op, l, r):
        self.op = op
        self.l = l
        self.r = r

    def __str__(self):
        return "(" + str(self.l) + " " + str(self.op) + " " + str(self.r) + ")"

    def eval(self):
        if self.op == '+':
            return self.l.eval() + self.r.eval()
        elif self.op == '-':
            return self.l.eval() - self.r.eval()
        elif self.op == '*':
            return self.l.eval() * self.r.eval()
        elif self.op == '/':
            try:
                return self.l.eval() / self.r.eval()
            except ZeroDivisionError:
                raise


class NullNode(Node):

    def eval(self):
        pass


class Tree:

    def __init__(self, depth, terminals):
        self.depth = depth
        self.terminals = terminals
        self.ops = ['+', '-', '*', '/']

    def create_tree(self):
        def recursion(depth):
            if depth > 0:
                return OpNode(choice(self.ops), recursion(depth-1), recursion(depth-1))
            else:
                return NumNode(choice(self.terminals))

        return recursion(self.depth)

if __name__ == '__main__':
    terminals = [x+1 for x in range(10)]
    depth = 3
    tree = Tree(depth, terminals).create_tree()
    print(tree)
    print(tree.eval())

