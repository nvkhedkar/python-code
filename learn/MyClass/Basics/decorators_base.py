import functools, time


def SlowDown(_func=None, rate=1):
    # class as decorator
    class _SlowDown:
        def __init__(self, func, rate=0.25):
            self.func = func
            self.rate = rate
            print(f"__init__: {self.func}, {self.rate}")

        def __call__(self, *args, **kwargs):
            print(f"__call__ {self.rate}")
            time.sleep(self.rate)
            return self.func(*args, **kwargs)

    if _func:
        print(f"func {_func} {rate}")
        return _SlowDown(_func)
    else:
        print(f"No func {_func} {rate}")

        def wrapper(_func):
            print(f'wrapper {_func}')
            return _SlowDown(_func, rate)
        return wrapper


def slow_down(_func=None, *, rate=1):
    """Sleep given amount of seconds before calling the function
    *, : means all floowing parameters are keyword only
    function to decorate is only passed in directly if the decorator
    is called without arguments
    """
    def decorator_slow_down(func):
        @functools.wraps(func)
        def wrapper_slow_down(*args, **kwargs):
            time.sleep(rate)
            return func(*args, **kwargs)
        return wrapper_slow_down

    if _func is None:
        '''
        decorator called with arguments - so function is not passed
        return inner decorator
        this will wrap the function later
        '''
        print(f"No func {_func} {rate}")
        return decorator_slow_down
    else:
        '''
        decorator is called without arguments - so function is passed
        wrap it and return it
        '''
        print(f"func {_func} {rate}")
        return decorator_slow_down(_func)


def timer(func):
    """Decorator to find function run time"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Run time: {func.__name__!r} {run_time:.4f} secs")
        return value

    return wrapper_timer


@timer
def sleepy(secs):
    time.sleep(secs)
    return secs + 1


print(sleepy(2))




