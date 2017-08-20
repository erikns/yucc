"""UpCloud CLI.

Usage:
    yucc server ls [options] [-t <tags>...]
    yucc server inspect <id> [options]
    yucc templates [options]
    yucc zones [options]
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
    server          Manage servers
    templates       List available public templates
    zones           List available zones

Server subcommands:
    ls              List all servers
    inspect         Show server details

"""

from docopt import docopt

from . import __version__, __prog__
from commands import Zones
from commands import Templates
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


def run_zones(args):
    zones = Zones(determine_log_level(args), read_credentials())
    zones.run()


def run_templates(args):
    templates = Templates(determine_log_level(args), read_credentials())
    templates.run()


def main():
    args = docopt(__doc__)
    if args['--debug']:
        print args 
        print ''

    if args['--version']:
        print __prog__, 'version', __version__
        exit(0)

    if args['zones']:
        run_zones(args)
    elif args['templates']:
        run_templates(args)
    else:
        Logger(LogLevel.CRIT).critical('Command not implemented')
        exit(1)

