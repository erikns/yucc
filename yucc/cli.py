"""UpCloud CLI.

Usage:
    yucc ls servers [options] [-t <tags>...]
    yucc ls templates [options]
    yucc ls zones [options]
    yucc account
    yucc [options]

Options:
    -p, --profile=<profile>   Settings profile to use. Read from
                              ~/.yaccrc file. [default: ~/.yaccrc]
    -t, --tags                Filter on or set tags
    -q, --quiet               Be silent. Only output essential data
    -h, --help                Show this helpscreen and exit
    -v, --verbose             Verbose output
    --debug                   Output debugging information
    --version                 Print version and exit

Commands:
    ls                        List resources
    account                   Show basic account information

"""

from docopt import docopt

from . import __version__, __prog__
from commands import Zones
from commands import Templates
from commands import Account
from .logger import LogLevel, Logger
from .config import read_credentials

def determine_log_level(args):
    level = LogLevel.ERROR
    if args['--quiet']:
        level = LogLevel.NORMAL
    if args['--verbose']:
        level = LogLevel.INFO
    if args['--debug']:
        level = LogLevel.DEBUG
    return level


def run_ls_zones(args):
    zones = Zones(determine_log_level(args), read_credentials())
    zones.run()


def run_ls_templates(args):
    templates = Templates(determine_log_level(args), read_credentials())
    templates.run()


def run_account(args):
    account = Account(determine_log_level(args), read_credentials())
    account.run()


def main():
    args = docopt(__doc__)
    if args['--debug']:
        print args 
        print ''

    if args['--version']:
        print __prog__, 'version', __version__
        exit(0)

    logger = Logger(LogLevel.ERROR)
    if args['ls']:
        if args['zones']:
            run_ls_zones(args)
        elif args['templates']:
            run_ls_templates(args)
        elif args['servers']:
            logger.critical('Command for listing servers is not yet implemented')
            exit(1)
        else:
            logger.critical('Unknown resource type given to ' +
                    'command `ls`')
            exit(1)
    elif args['account']:
        run_account(args)
    else:
        logger.critical('Command given is unknown')
        exit(1)

