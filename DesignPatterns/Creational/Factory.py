
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


class Cat(Pet):
    def __init__(self, n='tom'):
        Pet.__init__(self, n)

    def speak(self):
        return 'meow! meow!'


def pet_factory(pet_type='dog'):
    if pet_type == 'dog':
        return Dog()
    elif pet_type == 'cat':
        return Cat()


c = pet_factory('cat')
print(f'{c.name} says {c.speak()}')

d = pet_factory('dog')
print(f'{d.name} says {d.speak()}')


