"""
When to Use Adapter Pattern
1. When an outside component provides captivating functionality that we'd like to reuse,
   but it's incompatible with our current application. A suitable Adapter can be developed
   to make them compatible with each other
2. When our application is not compatible with the interface that our client is expecting
3. When we want to reuse legacy code in our application without making any modification in the original code
"""


class Movable:
    def get_speed_mph(self):
        return 0.0


class Bugatti(Movable):
    def get_speed_mph(self):
        return 265.0


class MovableAdapter:
    def __init__(self, o):
        self._object = o

    def get_speed(self):
        return self.convert_to_kph()

    def convert_to_kph(self):
        return self._object.get_speed_mph() * 1.63


bg = Bugatti()
bga = MovableAdapter(bg)

print(f'Mph: {bg.get_speed_mph()}, Kph: {bga.get_speed()}')
