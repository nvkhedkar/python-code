import functools
import time
import decorator


a = 1                   # int
b = 2.0                 # float
c = 'simple string'     # string
ls = [a, b, c]          # list
dt = {
    str(a): a,
    str(b): b,
    str(c): c}          # dictionary


def show_type_and_value(aa):
    print(f"type: {type(aa)}, value:{aa}")


def demo_func():
    print('Hello demo')
    for i in range(4):
        if i % 2 == 0:
            print("even")
        else:
            print("odd")
    print('Bye demo')


def i_do_nothing():
    pass


uc = 'str1 \u2602 \u0041'
u = u'strunicode'
d = [x for x in range(5)]

show_type_and_value(a)
show_type_and_value(b)
show_type_and_value(c)
show_type_and_value(ls)
show_type_and_value(dt)

for i, x in enumerate(d):
    print(f"{i}: {x}")


def timer(func):
    """Decorator to find function run time"""
    @functools.wraps(func)  # copies func attributes: __name__ __doc__ etc
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        # Call the function
        value = func(*args, **kwargs)
        run_time = time.perf_counter() - start_time
        print(f"Run time for {func.__name__!r} is {run_time:.4f} seconds")
        return value
    return wrapper_timer


@timer
def sleepy(secs):
    time.sleep(secs)
    return secs + 1


ans = sleepy(0.5)
print(ans, type(ans))


class Student:
    def __init__(self):
        print("init object")
        self.name = ''
        self.address = ''

    def create(self, n, a):
        self.name = n
        self. address = a

    def __del__(self):
        print("delete object")

    def __call__(self, *args, **kwargs):
        self.address = self.address.upper()
        return self

    def __str__(self):
        return f"name: {self.name} city: {self.address}"

    def __len__(self):
        return len(self.name) + len(self.address)

    def __eq__(self, other):
        return self.name == other.name



s = Student()
s.create('nikhil', 'pune')
print(f"Student: {str(s)} {len(s)}")
print(f"Student called: {str(s())}")
s1 = Student()
s1.create('nikhil', 'new york')
if s == s1:
    print("Students are the same")
