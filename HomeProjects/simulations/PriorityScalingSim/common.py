import argparse
import os, re, sys, logging
from datetime import datetime

LOG_FORMAT = '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s: %(message)s'

logger = logging.getLogger(__name__)


def set_logger_filehandler(log_full):
    from logging.handlers import RotatingFileHandler
    now = datetime.now()
    timestamp = datetime.strftime(now, "%Y%b%d_%Hh%Mm%Ss%f")

    # log_file = f'{os.path.splitext(os.path.basename(__file__))[0]}_{args.cmd}_{timestamp}.log'
    log_file_short = f'{os.path.splitext(os.path.basename(__file__))[0]}.log'
    formatter = logging.Formatter(LOG_FORMAT)
    fh = RotatingFileHandler(log_full, maxBytes=1024 * 1024 * 5, backupCount=5)
    fh.setLevel(logger.level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def set_logging_config(level, log_full=''):
    logger.setLevel(level)
    formatter = logging.Formatter(LOG_FORMAT)
    if log_full:
        set_logger_filehandler(log_full)
    # create console handler with a higher log level
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


class LogArgumentParser(argparse.ArgumentParser):
    def error(self, msg):
        logger.error(msg)
        sys.exit(1)
        # raise Exception(msg)


parser = LogArgumentParser()


def check_validity_3_32(arg_value, pat='[\w\d-]{3,32}'):
    recomp = re.compile(pat)
    if not recomp.match(arg_value):
        raise argparse.ArgumentError(f"Argument {arg_value} not in correct format")
    return arg_value


def check_validity_2_10(arg_value, pat='[\w\d-]{2,10}'):
    recomp = re.compile(pat)
    if not recomp.match(arg_value):
        raise argparse.ArgumentError(f"Argument {arg_value} not in correct format")
    return arg_value


def check_validity_url(arg_value, pat='[\w\d\-/\:\.\?\=]+'):
    recomp = re.compile(pat)
    if not recomp.match(arg_value):
        raise Exception('Invalid arg')  # argparse.ArgumentError
    return arg_value
