import datetime
import os, sys, platform
import json, re
import logging
from subprocess import Popen, PIPE, STDOUT


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


def exec_shell_realtime_simple(cmd, cwd, applog, timeout=-1, shl='/bin/bash'):
    '''
    for windows shl="c:/Windows/system32/cmd.exe"
    '''
    def kill_process_with_childs(parent_pid):
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
    p = Popen(';'.join(cmd),  # ['echo Nikhil ; cd /trusolid ; ls ; pwd'],
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
            kill_process_with_childs(p.pid)
            stat = 'timeout_reached'
            break

    return p, outlines, stat
