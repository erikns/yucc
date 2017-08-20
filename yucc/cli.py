import upcloud_api
from upcloud_api import ZONE
import argparse

from .config import read_credentials
from .logger import Logger, LogLevel


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action = 'count', 
            dest = 'log_level', default = 0,
            help = 'be more verbose in logging')

    args = parser.parse_args()
    args.log_level = LogLevel.ERROR + args.log_level
    
    return args


def main():
    args = parse_arguments()

    logger = Logger(args.log_level)
    logger.debug('Arguments: ' + str(args))

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

