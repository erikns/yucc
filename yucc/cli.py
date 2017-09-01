# -*- coding: utf-8 -*-

from docopt import docopt

from . import __version__, __prog__, __doc__ as __maindoc__

from commands import *
from .logger import LogLevel, Logger
from .config import read_config, verify_config_permissions
from .util import credentials_prompt

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
        'server_create': CreateServerCommand,
        'server_start': StartServerCommand,
        'server_stop': StopServerCommand,
        'server_restart': RestartServerCommand,
        'server_delete': DeleteServerCommand,
        'server_info': DumpServerInfoCommand,
        'account': AccountCommand,
        'profile': ProfileCommand
    }
    return cmds[cmd]


def main():
    args = docopt(__maindoc__)
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
            extra_args['os'] = args['--os']
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

    cmd = command(logger, config, **extra_args)
    cmd.run()
    if not cmd.has_error():
        logger.normal(cmd.output())
    else:
        errors = cmd.errors()
        for error in errors:
            logger.error(error)
        exit(1)
