# -*- coding: utf-8 -*-
"""yucc - Your UpCloud CLI.

Copyright (C) Erik Sørensen, 2017.

Usage:
    yucc ls servers [options] [-t <tags>...]
    yucc ls templates [options]
    yucc ls zones [options]
    yucc ls plans [options]
    yucc server create (--hostname=<hostname>) (--plan=<plan>)
      (--login-user=<user> --ssh-key=<ssh-key>) [--ensure-started]
      [options]
    yucc server start <uuid> [options]
    yucc server stop <uuid> [options]
    yucc server restart <uuid> [options]
    yucc server delete <uuid> [--delete-storages] [options]
    yucc server info <uuid> [options]
    yucc account [options]
    yucc profile [options]
    yucc [options]

Options:
    --hostname=<hostname>      Hostname of a server
    --title=<title>            Title of a server. If not set it will be the same
                               as the hostname.
    --plan=<plan>              Plan to use for the server
    --login-user=<user>        The username to create on the server
    --ssh-key=<ssh-key>        The ssh public key to deploy to the server
    --zone=<zone>              The zone to deploy to. Default might be read from
                               profile.
    --ensure-started           Wait for the server to start when creating the
                               server.
    --delete-storages          Also delete storages when deleting server
    -f, --format=<format>      Program output format. [default: json]
    -p, --profile=<profile>    Settings profile to use. Read from
                               ~/.yaccrc file. [default: default]
    -P, --prompt-credentials   Prompt for credentials rather than reading
                               them from profile
    -t, --tags                 Filter on or set tags
    -q, --quiet                Be silent. Only output essential data
    -h, --help                 Show this helpscreen and exit
    -v, --verbose              Verbose output
    --debug                    Output debugging information
    --version                  Print version and exit

Commands:
    ls                         List resources (servers, templates, zones, plans)
    account                    Show basic account information
    profile                    Dump profile information

"""

from docopt import docopt

from . import __version__, __prog__
from commands import *
from new_commands import ProfileCommand
from new_commands import AccountCommand
from new_commands import ListPlansCommand
from new_commands import ListTemplatesCommand
from new_commands import ListZonesCommand
from new_commands import ListServersCommand
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
        'ls_zones': ListZonesCommand,
        'ls_templates': ListTemplatesCommand,
        'ls_servers': ListServersCommand,
        'ls_plans': ListPlansCommand,
        'server_create': create_server,
        'server_start': start_server,
        'server_stop': stop_server,
        'server_restart': restart_server,
        'server_delete': delete_server,
        'server_info': dump_server,
        'account': AccountCommand,
        'profile': ProfileCommand
    }
    return cmds[cmd]

def is_new_command(cmd):
    import inspect
    return inspect.isclass(cmd)

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

    command = None
    extra_args = {'format': args['--format']}

    if args['ls']:
        if args['zones']:
            command = get_command('ls_zones')
        elif args['templates']:
            command = get_command('ls_templates')
        elif args['servers']:
            command = get_command('ls_servers')
        elif args['plans']:
            command = get_command('ls_plans')
        else:
            logger.critical('Unknown resource type given to ' +
                    'command `ls`')
            exit(1)
    elif args['account']:
        command = get_command('account')
    elif args['profile']:
        command = get_command('profile')
    elif args['server']:
        if args['create']:
            command = get_command('server_create')
            extra_args['hostname'] = args['--hostname']
            extra_args['plan'] = args['--plan']
            if not args.get('zone'):
                zone = config.get('default_zone')
                if not zone:
                    logger.error('No default zone specified. You will have to ' +
                       'provide it.')
                    exit(1)
            else:
                zone = args['zone']
            extra_args['zone'] = zone
            extra_args['login_user'] = args['--login-user']
            extra_args['ssh_key'] = args['--ssh-key']
            extra_args['ensure_started'] = args['--ensure-started']
        elif args['start']:
            command = get_command('server_start')
            extra_args['uuid'] = args['<uuid>']
        elif args['stop']:
            command = get_command('server_stop')
            extra_args['uuid'] = args['<uuid>']
        elif args['restart']:
            command = get_command('server_restart')
            extra_args['uuid'] = args['<uuid>']
        elif args['delete']:
            command = get_command('server_delete')
            if args['--delete-storages']:
                extra_args['delete-storages'] = True
            extra_args['uuid'] = args['<uuid>']
        elif args['info']:
            command = get_command('server_info')
            extra_args['uuid'] = args['<uuid>']
        else:
            logger.critical('Unknown subcommand for server')
            exit(1)
    else:
        logger.critical('Command given is unknown')
        exit(1)

    logger.debug('extra_args: ' + str(extra_args))

    if is_new_command(command):
        cmd = command(logger, config, **extra_args)
        cmd.run()
        if not cmd.has_error():
            logger.normal(cmd.output())
        else:
            errors = cmd.errors()
            for error in errors:
                logger.error(error)
            exit(1)
    else:
        if not command(logger, config, **extra_args):
            exit(1)
