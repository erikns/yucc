from colorama import Style, Fore

class LogLevel:
    CRIT = -2
    ERROR = -1
    NORMAL = 0
    WARN = 2
    INFO = 3
    DEBUG = 4


class Logger:
    def __init__(self, log_level = LogLevel.NORMAL):
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

    def critical(self, msg, bright = True):
        if self.log_level >= LogLevel.CRIT:
            if bright:
                print Style.BRIGHT + Fore.RED + '==> ' + msg + Fore.RESET + Style.RESET_ALL
            else:
                print Fore.RED + '==> ' + msg + Fore.RESET

    def normal(self, msg = ''): # for normal output information
        print msg


