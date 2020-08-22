import os, sys, platform
import json, re

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

