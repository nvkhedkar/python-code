import math

class AvlTree:
    class Node:
        def __init__(self, v=None):
            self.value = v
            self.left = None
            self.right = None
            self.height = 0

    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self.insertr(self.root, value)

    def insertr(self, current, value):
        if not current:
            return AvlTree.Node(value)

        if value <= current.value:
            current.left = self.insertr(current.left, value)
        else:
            current.right = self.insertr(current.right, value)

        self.height(current)
        return current

    def balance(self, current):
        return

    def height(self):
        self.height(self.root)

    def height(self, current):
        lh = self.get_height(current.left)
        rh = self.get_height(current.right)
        current.height = max(lh, rh) + 1

    def get_height(self, current):
        return -1 if not current else current.height

    def is_leaf(self, current):
        return not current.left and not current.right

    def to_string_r(self, current):
        strepr = f' | {current.value} ({current.height})'
        strepr += f' L: ' if not current.left else f' L: {current.left.value} '
        strepr += f' R: ' if not current.right else f' R: {current.right.value} '
        print(strepr)
        if current.left:
            self.to_string_r(current.left)
        if current.right:
            self.to_string_r(current.right)

    def to_string(self):
        strepr = ''
        self.to_string_r(self.root)

    @staticmethod
    def test_avl_tree():
        avt = AvlTree()
        avt.insert(20)
        avt.to_string()
        avt.insert(30)
        avt.insert(10)
        avt.to_string()
        avt.insert(5)
        avt.insert(15)
        avt.to_string()
        print('done')


AvlTree.test_avl_tree()
