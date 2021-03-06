import datetime
import os, sys, platform, stat
import json, re
import logging
from subprocess import Popen, PIPE, STDOUT
import functools, time


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


def count_calls(func):
    """decorator to count function calls"""
    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper_count_calls.num_calls = 0
    return wrapper_count_calls


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
        return decorator_slow_down
    else:
        '''
        decorator is called without arguments - so function is passed
        wrap it and return it
        '''
        return decorator_slow_down(_func)


def slow_down_by(_func=None, rate=1):
    """
    same as slow_down - but uses a class internally
    :param _func:
    :param rate:
    :return: decorator
    """
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


class CountCalls:
    """
    Decorator class to count function calls
    use:
        @CountCalls
        def some_function():
    """
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__!r}")
        return self.func(*args, **kwargs)


def get_int_timestamp():
    return int(time.mktime(datetime.datetime.now().timetuple()))


def write_json(dict_, json_file):
    import json
    with open(json_file, 'w') as fp:
        json.dump(dict_, fp)


def remove_even_readonly(full):
    os.chmod(full, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    os.unlink(full)


def remove_directory(dirname):
    import errno, os, stat, shutil

    def handle_remove_read_only(func, path, exc):
        exec_value = exc[1]
        if func in (os.rmdir, os.unlink, os.remove) and exec_value.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
            func(path)
        else:
            raise

    shutil.rmtree(dirname, ignore_errors=False, onerror=handle_remove_read_only)


def os_info():
    osinfo = dict()
    osinfo['os.name'] = os.name
    osinfo['platform.system'] = platform.system()
    osinfo['platform.release'] = platform.release()
    osinfo['platform.version'] = platform.version()
    osinfo['platform.machine'] = platform.machine()
    osinfo['platform.node'] = platform.node()
    osinfo['platform.processor'] = platform.processor()
    return osinfo


def print_exception_info(e, applog, raise_again=True):
    import traceback, sys
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    formatted = traceback.format_exception(exc_type, exc_value, exc_traceback)
    file_info = re.sub(r'\n\s*', ' CODE_LINE: ', re.sub(r'\s*\n\s*$', '', re.sub(r'^\s+', '', formatted[-2])))
    applog.error('Exception in predict.py')
    # logger.error('{}'.format(e.__repr__()))
    applog.error('Exception message: {}'.format(re.sub('\n', '', formatted[-1])))
    applog.error('{}'.format(file_info))
    if raise_again:
        raise Exception(exc_value)


DEBUG_LEVELV_NUM = 9


def debugv(self, message, *args, **kws):
    if self.isEnabledFor(DEBUG_LEVELV_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(DEBUG_LEVELV_NUM, message, args, **kws)


logging.Logger.debugv = debugv
logging.addLevelName(DEBUG_LEVELV_NUM, "DEBUGV")


def set_custom_logging(log_level_num: int, log_function_name: str, log_function):
    setattr(logging.Logger, log_function_name, log_function)
    logging.addLevelName(log_level_num, log_function_name.upper)
    return


def exec_shell_realtime_simple(cmd, cwd, applog, separator=' ; ', timeout=-1, shl='/bin/bash'):
    '''
    for windows:
        shl="c:/Windows/system32/cmd.exe"
        separator=" & "
    '''

    def kill_process_with_children(parent_pid):
        import psutil
        # parent_pid = 30437   # my example
        applog.info('Kill process with pid {}'.format(parent_pid))
        parent = psutil.Process(parent_pid)
        for child in parent.children(recursive=True):  # or parent.children() for recursive=False
            applog.info('Kill child process pid {}'.format(child.pid))
            child.kill()
        applog.info('Kill Parent pid {}'.format(parent.pid))
        parent.kill()

    def read_out(p, timeout=-1):
        while True:
            line = p.stdout.readline().rstrip()
            if not line:
                pass
            # yield 'Collected Inputs'
            else:
                yield line
            if p.poll() is not None:
                yield 'Poll break - Process Finished'
                break

    new_env = os.environ.copy()
    applog.info('exec_shell_realtime_simple')
    applog.info('shell {}'.format(shl))
    start_time = datetime.utcnow()

    p = Popen(separator.join(cmd),  # ['echo Nikhil ; cd /mydir ; ls ; pwd'],
              stdout=PIPE, stderr=STDOUT,
              # env=new_env,
              executable=shl,
              shell=True,
              encoding='utf-8',
              cwd=cwd
              )

    outlines = []
    stat = 'failure'
    for line in read_out(p, timeout):
        applog.info('SHELL_CMD_OUTPUT: {}'.format(line))
        time_delta = datetime.utcnow() - start_time
        if 'Process Finished' not in line:
            outlines.append(line)
        if time_delta.total_seconds() >= timeout:
            kill_process_with_children(p.pid)
            stat = 'timeout_reached'
            break

    return p, outlines, stat


def get_directory_size(start_path='.'):
    '''
    Returns directory size in bytes
    '''
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def get_disk_usage(path='/'):
    import shutil
    total, used, free = shutil.disk_usage(path)
    print(f'Total: {total / (1024 * 1024 * 1024)}GB')
    print(f'Used: {used / (1024 * 1024 * 1024)}GB')
    print(f'free: {free / (1024 * 1024 * 1024)}GB')
