
class Handler:
    def __init__(self, successor=None):
        self._successor = successor

    def set_next(self, successor):
        self._successor = successor
        # return successor to set_next(obj1).set_next(obj2) can be chained
        return successor

    def handle(self, req):
        handled = self._handle(req)
        if not handled and self._successor:
            self._successor.handle(req)
        return None

    def _handle(self, req):
        raise NotImplementedError('Handler not implemented')


class Dog(Handler):
    def _handle(self, req):
        if req == 'Meatball':
            print(f'{self.__class__.__name__} Eating {req}')
            return True
        print(f'{self.__class__.__name__} passing forward: {req}')
        return False


class Monkey(Handler):
    def _handle(self, req):
        if req == 'Banana':
            print(f'{self.__class__.__name__} Eating {req}')
            return True
        print(f'{self.__class__.__name__} passing forward: {req}')
        return False


class DefaultHandler(Handler):
    def _handle(self, req):
        print(f'{self.__class__.__name__}: NO handler for {req}')
        return True


class Client:
    def __init__(self):
        self.chain = None

    def delegate(self, requests_):
        for req in requests_:
            self.chain.handle(req)


cl = Client()
d = Dog()
m = Monkey()
dh = DefaultHandler()
d.set_next(m).set_next(dh)

cl.chain = d
# cl.chain = Dog(Monkey(DefaultHandler()))

cl.delegate(['Banana', 'Meatball'])
