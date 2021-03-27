"""
Let's talk about when to use the Proxy pattern:

1. When we want a simplified version of a complex or heavy object.
   In this case, we may represent it with a skeleton object which loads the original object on demand,
   also called as lazy initialization. This is known as the Virtual Proxy.
2. When the original object is present in different address space, and we want to represent it locally.
   We can create a proxy which does all the necessary boilerplate stuff like creating and maintaining
   the connection, encoding, decoding, etc., while the client accesses it as it was present in their
   local address space. This is called the Remote Proxy.
3. When we want to add a layer of security to the original underlying object to provide controlled access
   based on access rights of the client. This is called Protection Proxy
"""


class ExpensiveObject:
    def __init__(self):
        self.heavy_initial_config()

    def process(self):
        print(f"{self.__class__.__name__}: processing complete.")

    def heavy_initial_config(self):
        print(f"{self.__class__.__name__}: Loading initial configuration...")


class VirtualProxy:
    def __init__(self):
        self.object = None

    def process(self):
        if not self.object:
            self.object = ExpensiveObject()
        self.object.process()


class ProtectionProxy:
    def __init__(self):
        self.is_free = True
        self.object = None

    def process(self):
        if self.is_free:
            if not self.object:
                self.object = ExpensiveObject()
            self.object.process()
        else:
            print('Object is not free...')


sp = VirtualProxy()
sp.process()

pp = ProtectionProxy()
pp.process()
pp.process()
pp.is_free = False
pp.process()
