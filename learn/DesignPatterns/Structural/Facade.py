"""
Facade:
1. Facade encapsulates a complex subsystem behind a simple interface.
   It hides much of the complexity and makes the subsystem easy to use.
2. It decouples a client implementation from the complex subsystem.
   Thanks to this, we can make changes to the existing subsystem and don't affect a client.

Issues:
The facade pattern doesn't force us to unwanted tradeoffs, because it only adds additional layers of abstraction.

Sometimes the pattern can be overused in simple scenarios, which will lead to redundant implementations.
"""


class SubsystemA:
    def method1(self):
        print(f'{self.__class__.__name__} method 1')

    def method2(self):
        print(f'{self.__class__.__name__} method 2')


class SubsystemB:
    def method1(self):
        print(f'{self.__class__.__name__} method 1')

    def method2(self):
        print(f'{self.__class__.__name__} method 2')


class Facade:
    def __init__(self):
        self.subsystem_a = SubsystemA()
        self.subsystem_b = SubsystemB()

    def operate_system(self):
        self.subsystem_a.method1()
        self.subsystem_a.method2()

        self.subsystem_b.method1()
        self.subsystem_b.method2()


f = Facade()
f.operate_system()


