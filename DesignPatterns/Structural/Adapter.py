class Hindi:
    def __init__(self):
        self.name = 'hindi'

    def greet_hindi(self):
        return f'{self.name} says Namaste!'


class English:
    def __init__(self):
        self.name = 'english'

    def greet_english(self):
        return f'{self.name} says Hello!'


class Adapter:
    def __init__(self, o, **adapted_method):
        self._object = o
        self.__dict__.update(adapted_method)

    def __getattr__(self, item):
        return getattr(self._object, item)


hindi = Hindi()
english = English()
objects = list()
objects.append(Adapter(hindi, greet=hindi.greet_hindi))
objects.append(Adapter(english, greet=english.greet_english))

for o in objects:
    print(f'Greet {o.name}: {o.greet()}')


