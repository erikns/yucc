import upcloud_api
from upcloud_api import ZONE
import argparse

from .config import read_credentials
from .logger import Logger, LogLevel
from . import __version__
from commands import Zones

class Cli:
    def __init__(self):
        parser = argparse.ArgumentParser(description='UpCloud CLI')
        parser.add_argument('-v', '--verbose', action = 'count', 
                dest = 'log_level', default = 0,
                help = 'be more verbose in logging')
        parser.add_argument('--version', action = 'store_true',
                dest = 'show_version', default = False,
                help = 'print version information and exit')

        parser.add_argument('command', 
                help = 'Subcommand to run',
                choices = ['server', 'zones'])

        self.args = parser.parse_args()
        self.args.log_level = LogLevel.ERROR + self.args.log_level
        Logger(self.args.log_level).debug(str(self.args))
        self.creds = read_credentials()

        if self.args.show_version:
            Logger().normal('yucc-cli version ' + __version__)
            exit(0)

        getattr(self, self.args.command)()

    def server(self):
        logger = Logger(self.args.log_level)
        logger.critical('Command not implemented')
        exit(1)

    def zones(self):
        zones = Zones(self.args, self.creds)
        zones.run()


def main():
    Cli()


