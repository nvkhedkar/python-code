from abc import ABC


class Component:
    def component_function(self):
        pass


class Leaf1(Component):
    def __init__(self, n):
        Component.__init__(n)
        self.name = n

    def component_function(self):
        print(f'Leaf1: {self.name}')


class Leaf2(Component):
    def __init__(self, n):
        Component.__init__(n)
        self.name = n

    def component_function(self):
        print(f'Leaf2: {self.name}')


class Composite(Component):
    def __init__(self, n):
        Component.__init__(n)
        self.name = n
        self.children = []

    def component_function(self):
        print(f'Composite: {self.name}')
        for child in self.children:
            child.component_function()

    def add_child(self, c):
        self.children.append(c)

    def remove_child(self, c):
        self.children.remove(c)


sub1 = Composite('SubMenu 1')
sub_sub_11 = Leaf1('sub_submenu_11')
sub_sub_12 = Leaf2('sub_submenu_12')

sub1.add_child(sub_sub_11)
sub1.add_child(sub_sub_12)

top = Composite('Top Menu')
sub2 = Composite('SubMenu 2')
top.add_child(sub1)
top.add_child(sub2)

top.component_function()
