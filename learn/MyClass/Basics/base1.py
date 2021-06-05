import functools
import time

a = 1
b = 2.0
c = 'str1'
d = [x for x in range(5)]
print(f"Data types: {type(a)}, {type(b)}, {type(c)} {type(d)}")

for i, x in enumerate(d):
    print(f"{i}: {x}")


def timer(func):
    """Decorator to find function run time"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Run time: {func.__name__} {run_time:.4f} secs")
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

    def __call__(self, *args, **kwargs):
        self.address = self.address.upper()
        return self

    def __str__(self):
        return f"name: {self.name} city: {self.address}"

    def __len__(self):
        return len(self.name) + len(self.address)

    def __eq__(self, other):
        return self.name == other.name

    def __del__(self):
        print("delete object")


s = Student()
s.create('nikhil', 'pune')
print(f"Student: {str(s)} {len(s)}")
print(f"Student called: {str(s())}")
s1 = Student()
s1.create('nikhil', 'new york')
if s == s1:
    print("Students are the same")
