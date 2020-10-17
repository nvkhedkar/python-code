import datetime
import os, sys, platform, stat
import json, re
import logging
from subprocess import Popen, PIPE, STDOUT


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


def set_custom_logging(log_level_num:int, log_function_name:str, log_function):
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
    
    p = Popen(separator.join(cmd),  # ['echo Nikhil ; cd /trusolid ; ls ; pwd'],
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


def get_directory_size(start_path = '.'):
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
