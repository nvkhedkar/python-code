"""
We need to keep few important principles in mind while implementing Chain of Responsibility:

1.Each processor in the chain will have its implementation for processing a command
    In our example above, all processors have their implementation of isAuthorized
2. Every processor in the chain should have reference to the next processor
    Above, UsernamePasswordProcessor delegates to OAuthProcessor
3. Each processor is responsible for delegating to the next processor so beware of dropped commands
    Again in our example, if the command is an instance of SamlProvider then the request may not get processed and will be unauthorized
4. Processors should not form a recursive cycle
    In our example, we don't have a cycle in our chain: UsernamePasswordProcessor -> OAuthProcessor. But, if we explicitly set UsernamePasswordProcessor as next processor of OAuthProcessor, then we end up with a cycle in our chain: UsernamePasswordProcessor -> OAuthProcessor -> UsernamePasswordProcessor. Taking the next processor in the constructor can help with this
5. Only one processor in the chain handles a given command

Disadvantages:
1. Mostly, it can get broken easily:
    if a processor fails to call the next processor, the command gets dropped
    if a processor calls the wrong processor, it can lead to a cycle
2. It can create deep stack traces, which can affect performance
3. It can lead to duplicate code across processors, increasing maintenance
"""


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
