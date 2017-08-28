# -*- coding: utf-8 -*-
"""yucc - Your UpCloud CLI.

Copyright (C) Erik Sørensen, 2017.

Usage:
    yucc ls servers [options] [-t <tags>...]
    yucc ls templates [options]
    yucc ls zones [options]
    yucc account [options]
    yucc profile [options]
    yucc [options]

Options:
    -p, --profile=<profile>   Settings profile to use. Read from
                              ~/.yaccrc file. [default: default]
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
    profile                   Dump profile information

"""

from docopt import docopt

from . import __version__, __prog__
from commands import *
from .logger import LogLevel, Logger
from .config import read_config, verify_config_permissions

def determine_log_level(args):
    level = LogLevel.WARN
    if args['--quiet']:
        level = LogLevel.ERROR
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
        'account': show_account_info,
        'profile': dump_profile_info
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

    try:
        logger = Logger(determine_log_level(args))
        verify_config_permissions(logger)
        if args['--prompt-credentials']:
            config = read_config(profile=args['--profile'])
            creds = credentials_prompt()
            config['username'] = creds['username']
            config['password'] = creds['password']
        else:
            config = read_config(profile=args['--profile'], read_creds=True)
    except ValueError as e:
        logger.error(e.message)
        exit(1)

    if not config.get('default_zone'):
        logger.warning('You have not set a default deployment zone. It will' +
            ' need to be provided.')

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
    elif args['profile']:
        command = get_command('profile')
    else:
        logger.critical('Command given is unknown')
        exit(1)

    logger = Logger(determine_log_level(args))
    if not command(logger, config):
        exit(1)
