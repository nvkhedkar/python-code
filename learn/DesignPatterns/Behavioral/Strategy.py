import types


class Strategy:
    def __init__(self, strategy_function=None):
        self.name = 'Default Strategy'

        # if strategy_function is passed replace execute with the strategy_function
        # Call to Strategy.execute will not execute strategy_function
        # This allows modification of behavior externally without changing current implementation
        if strategy_function:
            self.execute = types.MethodType(strategy_function, self)

    def execute(self):
        print(f'default_execute {self.name}')


class ConcreteStrategy1(Strategy):
    def __init__(self, strategy_function):
        Strategy.__init__(self, strategy_function)
        self.name = ''


class ConcreteStrategy2(Strategy):
    def __init__(self, strategy_function):
        Strategy.__init__(self, strategy_function)
        self.name = ''


# Can encapsulate inside a class
def strategy_one(class_object):
    print(f'strategy_one: {class_object.name}')


def strategy_two(class_object):
    print(f'strategy_two: {class_object.name}')


s0 = Strategy()
s0.execute()

s1 = ConcreteStrategy1(strategy_one)
s1.execute()

s2 = ConcreteStrategy2(strategy_two)
s2.execute()
