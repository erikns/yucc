import upcloud_api
from upcloud_api import ZONE
import argparse

from .config import read_credentials
from .logger import Logger, LogLevel
from . import __version__


def parse_arguments():
    parser = argparse.ArgumentParser(description='UpCloud CLI')
    parser.add_argument('-v', '--verbose', action = 'count', 
            dest = 'log_level', default = 0,
            help = 'be more verbose in logging')
    parser.add_argument('--version', action = 'store_true',
            dest = 'show_version', default = False,
            help = 'print version information and exit')

    args = parser.parse_args()
    args.log_level = LogLevel.ERROR + args.log_level
    
    return args

def cli_main():
    args = parse_arguments()
    logger = Logger(args.log_level)
    logger.debug('Arguments: ' + str(args))
    if args.show_version:
        logger.normal('yucc-cli version ' + __version__)
        exit(0)

    logger.debug('Reading credentials from preference file')
    creds = read_credentials()

    logger.debug('Injecting credentials')
    manager = upcloud_api.CloudManager(creds['username'], creds['password'])

    logger.debug('Collecting zones...')
    zones = manager.get_zones()['zones']['zone']
    logger.debug('Zones collected')

    logger.normal()
    for zone in zones:
        logger.normal(zone['id'] + ' ' + zone['description'])


def main():
    logger = Logger()
    try:
        cli_main()
    except:
        logger.critical('Critical unhandled error encountered!')


