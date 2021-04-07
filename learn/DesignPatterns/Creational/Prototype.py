import copy


class Prototype:
    def __init__(self):
        self._objects = {}

    def register(self, name, obj):
        self._objects[name] = obj

    def unregister(self, name):
        del self._objects[name]

    def clone(self, name, **attr):
        obj = copy.deepcopy(self._objects[name])
        obj.__dict__.update(attr)
        return obj


class Car:
    def __init__(self):
        self.name = 'Skylark'
        self.color = 'Red'
        self.variant = 'Ex'

    def __str__(self):
        return f'{self.__class__.__name__}: {self.name}, {self.color}, {self.variant}'


c = Car()
p = Prototype()
p.register('skylark', c)
c1 = p.clone('skylark', variant='Zx')
print(str(c))
print(str(c1))