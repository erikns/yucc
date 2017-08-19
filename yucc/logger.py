from colorama import Style, Fore

class LogLevel:
    NORMAL = 0
    CRIT = 1
    ERROR = 2
    WARN = 3
    INFO = 4
    DEBUG = 5


class Logger:
    def __init__(self, log_level):
        self.log_level = log_level

    def debug(self, msg):
        if self.log_level >= LogLevel.DEBUG:
            print Style.DIM + '==> ' + msg + Style.RESET_ALL

    def info(self, msg):
        if self.log_level >= LogLevel.INFO:
            print '==> '+ msg

    def warning(self, msg):
        if self.log_level >= LogLevel.WARN:
            print Fore.YELLOW + '==> ' + msg + Fore.RESET

    def error(self, msg):
        if self.log_level >= LogLevel.ERROR:
            print Fore.RED + '==> ' + msg + Fore.RESET

    def critical(self, msg):
        if self.log_level >= LogLevel.CRIT:
            print Style.BRIGHT + Fore.RED + '==> ' + msg + Fore.RESET + Style.RESET_ALL

    def normal(self, msg = ''): # for normal output information
        print msg


