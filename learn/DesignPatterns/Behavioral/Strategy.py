import types


class Strategy:
    def __init__(self, strategy_function=None):
        self.name = 'Default Strategy'

        # if strategy_function is passed replace execute with the strategy_function
        if strategy_function:
            self.execute = types.MethodType(strategy_function, self)

    def execute(self):
        print(f'default_execute {self.name}')


def strategy_one(class_object):
    print(f'strategy_one: {class_object.name}')


def strategy_two(class_object):
    print(f'strategy_two: {class_object.name}')


s0 = Strategy()
s0.execute()

s1 = Strategy(strategy_one)
s1.execute()

s2 = Strategy(strategy_two)
s2.execute()
