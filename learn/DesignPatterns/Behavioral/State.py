"""
The main idea of State pattern is to allow the object for changing its behavior without changing its class.
Each state is handled by a separate class.

extract the logic to separate classes and let our context object delegate the behavior to the methods implemented in
 the state class. Besides, we can leverage the transitions between the states, where one state can alter the state of
 the context.

State vs Strategy:
Both design patterns are very similar, but their UML diagram is the same, with the idea behind them slightly different.
 First, the strategy pattern defines a family of interchangeable algorithms. Generally, they achieve the same goal,
 but with a different implementation, for example, sorting or rendering algorithms.
 In state pattern, the behavior might change completely, based on actual state.

Next, in strategy, the client has to be aware of the possible strategies to use and change them explicitly.
 Whereas in state pattern, each state is linked to another and create the flow as in Finite State Machine.
"""


class AtmState:
    name = 'state'
    allowed = []

    def next_state(self, state):
        if state.name in self.allowed:
            print(f'Current state {self}, changed to {state.name}')
            self.__class__ = state
        else:
            print(f'Cannot change to {state.name}')

    def __str__(self):
        return self.name


class AtmStateOff(AtmState):
    name = 'off'
    allowed = ['on']


class AtmStateOn(AtmState):
    name = 'on'
    allowed = ['off']


class ATM:
    def __init__(self):
        self.current_state = AtmStateOff()

    def next_state(self, state):
        self.current_state.next_state(state)


atm = ATM()
atm.next_state(AtmStateOn)
atm.next_state(AtmStateOff)
atm.next_state(AtmStateOn)
