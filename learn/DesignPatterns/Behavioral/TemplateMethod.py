"""
Template method
It makes it easier to implement complex algorithms by encapsulating logic in a single method.

the algorithm's structure will be defined in a base class that defines the template template_method() method
the template_method() method is the template method, which defines steps of the algorithm

It should not be overridden
"""
import sys
from abc import ABC, abstractmethod


class AbstractClass(ABC):
    def template_method(self):
        self.__always_do_this()
        self.step_1()
        self.step_2()
        self.do_this_or()
        pass

    def __always_do_this(self):
        # Methods starting with __ cannot be overriden
        name_of_this_function = sys._getframe().f_code.co_name
        name_of_concrete_child_class = self.__class__.__name__
        print(f'{name_of_concrete_child_class}, {name_of_this_function}')

    @abstractmethod
    def step_1(self):
        pass

    @abstractmethod
    def step_2(self):
        pass

    def do_this_or(self):
        print('Default implementation. Overriding this is optional')


class ClassA(AbstractClass):
    def step_1(self):
        print(f'{self.__class__.__name__}: Doing step 1')

    def step_2(self):
        print(f'{self.__class__.__name__}: Doing step 2')


class ClassB(AbstractClass):
    def step_1(self):
        print(f'{self.__class__.__name__}: Doing step 1')

    def step_2(self):
        print(f'{self.__class__.__name__}: Doing step 2')

    def do_this_or(self):
        print(f'{self.__class__.__name__}: specific implementation')


ca = ClassA()
ca.template_method()

cb = ClassB()
cb.template_method()
