
from __future__ import print_function
import sys
from colorama import Style, Fore


class LogLevel:
    CRIT = -2
    ERROR = -1
    NORMAL = 0
    WARN = 1
    INFO = 2
    DEBUG = 3


class Logger:
    def __init__(self, log_level=LogLevel.NORMAL):
        self.log_level = log_level

    def debug(self, msg):
        if self.log_level >= LogLevel.DEBUG:
            _print_stderr(Style.DIM + '==> ' + str(msg) + Style.RESET_ALL)

    def info(self, msg):
        if self.log_level >= LogLevel.INFO:
            _print_stderr(Fore.BLUE + '==> ' + str(msg) + Fore.RESET)

    def warning(self, msg):
        if self.log_level >= LogLevel.WARN:
            _print_stderr(Fore.YELLOW + '==> ' + str(msg) + Fore.RESET)

    def error(self, msg):
        if self.log_level >= LogLevel.ERROR:
            _print_stderr(Fore.RED + '==> ' + str(msg) + Fore.RESET)

    def critical(self, msg, bright=True):
        if self.log_level >= LogLevel.CRIT:
            if bright:
                _print_stderr(Style.BRIGHT + Fore.RED + '==> ' +
                              str(msg) + Fore.RESET + Style.RESET_ALL)
            else:
                _print_stderr(Fore.RED + '==> ' + str(msg) + Fore.RESET)

    def normal(self, msg=''):  # for normal output information
        _print_stdout(msg)


def _print_stdout(*args, **kwargs):
    print(*args, **kwargs)


def _print_stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
