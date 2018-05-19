# -*- coding: utf-8 -*-

from docopt import docopt

from . import __version__, __prog__, __doc__ as __maindoc__

from .commands import *
from .logger import LogLevel, Logger
from .config import read_config, verify_config_permissions
from .util import *


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
    if cmd.startswith('-'):
        # if the "command" given to this function starts with --, it
        # means there has been no known command given on program invocation
        return None
    else:
        cmds = {
            'ls_zones': ListZonesCommand,
            'ls_templates': ListTemplatesCommand,
            'ls_servers': ListServersCommand,
            'ls_plans': ListPlansCommand,
            'ls_tags': ListTagsCommand,
            'server_create': CreateServerCommand,
            'server_start': StartServerCommand,
            'server_stop': StopServerCommand,
            'server_restart': RestartServerCommand,
            'server_delete': DeleteServerCommand,
            'server_info': DumpServerInfoCommand,
            'server_tag': TagServerCommand,
            'server_untag': UntagServerCommand,
            'account': AccountCommand,
            'profile': ProfileCommand
        }
        return cmds[cmd]


def build_command(args):
    root_cmds = ['ls', 'server', 'account', 'profile']
    sub_cmds = ['zones', 'templates', 'servers', 'plans',
                'create', 'start', 'stop', 'restart', 'delete', 'info', 'tag', 'untag', 'tags']
    root_args = ['--debug', '--verbose', '--quiet', '--profile',
                 '--prompt-credentials', '--version']

    root_command = first_in(args, root_cmds + root_args)
    subcommand = first_in(args, sub_cmds)

    extras = exclude_keys(args, root_cmds + sub_cmds)
    extras = strip_keys(extras, '-')
    extras = strip_keys(extras, '<')
    extras = replace_in_keys(extras, '<', '')
    extras = replace_in_keys(extras, '>', '')
    extras = strip_none(extras)
    extras = replace_in_keys(extras, '-', '_')

    cmd_string = root_command + ('_' + subcommand if subcommand else '')
    return get_command(cmd_string), extras


def main():
    args = docopt(__maindoc__)
    if args['--debug']:
        print(args)
        print('')

    if args['--version']:
        print('v' + __version__)
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
        logger.error(e)
        exit(1)

    command, extra_args = build_command(args)
    logger.debug('extra_args: ' + str(extra_args))
    if not command:
        logger.error('No command given')
        exit(1)

    default_zone = config.get('default_zone')
    if not default_zone:
        logger.warning('You have not set a default deployment zone. It will' +
                       ' need to be provided.')
    extra_args['zone'] = default_zone

    try:
        cmd = command(logger, config, **extra_args)
        cmd.run()
        if not cmd.has_error():
            output = cmd.output()
            if output:
                logger.normal(output)
        else:
            errors = cmd.errors()
            for error in errors:
                logger.error(error)
            exit(1)
    except ValueError as e:
        logger.error(str(e))
        exit(1)
    except Exception as e:
        logger.critical('Unknown exception thrown')
        raise e
