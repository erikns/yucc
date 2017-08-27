"""UpCloud CLI.

Usage:
    yucc ls servers [options] [-t <tags>...]
    yucc ls templates [options]
    yucc ls zones [options]
    yucc account [options]
    yucc [options]

Options:
    -p, --profile=<profile>   Settings profile to use. Read from
                              ~/.yaccrc file. [default: ~/.yaccrc]
    -P, --prompt-credentials  Prompt for credentials rather than reading
                              them from profile
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
from commands import Zones, Templates, Account, Servers
from .logger import LogLevel, Logger
from .config import read_config

def determine_log_level(args):
    level = LogLevel.ERROR
    if args['--quiet']:
        level = LogLevel.NORMAL
    if args['--verbose']:
        level = LogLevel.INFO
    if args['--debug']:
        level = LogLevel.DEBUG
    return level


def run_ls_zones(args, creds):
    zones = Zones(determine_log_level(args), creds)
    if zones.run():
        exit(0)
    else:
        exit(1)


def run_ls_templates(args, creds):
    templates = Templates(determine_log_level(args), creds)
    if templates.run():
        exit(0)
    else:
        exit(1)


def run_ls_servers(args, creds):
    servers = Servers(determine_log_level(args), creds)
    if servers.run():
        exit(0)
    else:
        exit(1)


def run_account(args, creds):
    account = Account(determine_log_level(args), creds)
    if account.run():
        exit(0)
    else:
        exit(1)


def credentials_prompt():
    import getpass
    username = raw_input('Username: ')
    password = getpass.getpass('Password: ')
    return {'username': username, 'password': password}


def main():
    args = docopt(__doc__)
    if args['--debug']:
        print args
        print ''

    if args['--version']:
        print __prog__, 'version', __version__
        exit(0)

    logger = Logger(LogLevel.ERROR)
    creds = {}
    if args['--prompt-credentials']:
        creds = credentials_prompt()
    else:
        creds = read_config()

    if args['ls']:
        if args['zones']:
            run_ls_zones(args, creds)
        elif args['templates']:
            run_ls_templates(args, creds)
        elif args['servers']:
            run_ls_servers(args, creds)
        else:
            logger.critical('Unknown resource type given to ' +
                    'command `ls`')
            exit(1)
    elif args['account']:
        run_account(args, creds)
    else:
        logger.critical('Command given is unknown')
        exit(1)
