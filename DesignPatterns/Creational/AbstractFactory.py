"""
When to Use Abstract Factory Pattern:
1. The client is independent of how we create and compose the objects in the system
2. The system consists of multiple families of objects, and these families are designed to be used together
3. We need a run-time value to construct a particular dependency

Issues:
While the pattern is great when creating predefined objects, adding the new ones might be challenging.
To support the new type of objects will require changing the AbstractFactory class and all of its subclasses.
"""


class Pet:
    def __init__(self, n):
        self.name = n

    def speak(self):
        return 'sound!'


class Dog(Pet):
    def __init__(self, n='fluffy'):
        Pet.__init__(self, n)

    def speak(self):
        return 'woof! woof!'

    def __repr__(self):
        return f'Name: {self.name} Sound: {self.speak()}'


class Cat(Pet):
    def __init__(self, n='tom'):
        Pet.__init__(self, n)

    def speak(self):
        return 'meow! meow!'

    def __repr__(self):
        return f'Name: {self.name} Sound: {self.speak()}'


class Color:
    def color(self):
        return 'no color'


class White(Color):
    def color(self):
        return 'white'


class Brown(Color):
    def color(self):
        return 'brown'


def pet_factory(pet_type='dog'):
    if pet_type == 'dog':
        return Dog()
    elif pet_type == 'cat':
        return Cat()


def color_factory(color_type='white'):
    if color_type == 'white':
        return White()
    elif color_type == 'brown':
        return Brown()


def abstract_factory(fac_type='pet'):
    if fac_type == 'pet':
        return pet_factory
    elif fac_type == 'color':
        return color_factory


pf = abstract_factory('pet')
d = pf('dog')
print(repr(d))
cf = abstract_factory('color')
col = cf('brown')
print(col.color())

