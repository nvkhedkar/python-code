
class Subject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer):
        try:
            self.observers.remove(observer)
        except Exception as e:
            print('Found exception')

    def notify(self, modifier=None):
        for observer in self.observers:
            observer.update(self)


class Core(Subject):
    def __init__(self, n=''):
        Subject.__init__(self)
        self.name = n
        self._temp = 0

    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, temp):
        self._temp = temp
        self.notify()


class TempObserver:
    def __init__(self, n=''):
        self.name = n

    def update(self, subject):
        print(f'{self.name} Temperature: {subject.name} {subject.temp}')


def check_observer():
    c1 = Core('c1')
    c2 = Core('c2')
    o1 = TempObserver('o1')
    o2 = TempObserver('o2')
    c1.attach(o1)
    c1.attach(o2)
    c1.temp = 80
    c1.temp = 90


check_observer()

