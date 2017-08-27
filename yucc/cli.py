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
    ls                        List resources (servers, templates, zones)
    account                   Show basic account information

"""

from docopt import docopt

from . import __version__, __prog__
from commands import list_zones, list_templates, show_account_info, list_servers
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

def get_command(cmd):
    cmds = {
        'ls_zones': list_zones,
        'ls_templates': list_templates,
        'ls_servers': list_servers,
        'account': show_account_info
    }
    return cmds[cmd]

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
    if args['--prompt-credentials']:
        config = read_config()
        creds = credentials_prompt()
        config['username'] = creds['username']
        config['password'] = creds['password']
    else:
        config = read_config(read_creds=True)

    if args['--profile'] != '~/.yaccrc':
        logger.critical('yucc does not yet support changing the profile file')
        exit(1)

    if args['ls']:
        if args['zones']:
            command = get_command('ls_zones')
        elif args['templates']:
            command = get_command('ls_templates')
        elif args['servers']:
            command = get_command('ls_servers')
        else:
            logger.critical('Unknown resource type given to ' +
                    'command `ls`')
            exit(1)
    elif args['account']:
        command = get_command('account')
    else:
        logger.critical('Command given is unknown')
        exit(1)

    logger = Logger(determine_log_level(args))
    if not command(logger, config):
        exit(1)
