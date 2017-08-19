import upcloud_api
from upcloud_api import ZONE

from .config import read_credentials
from .logger import Logger, LogLevel

def main():
    logger = Logger(LogLevel.DEBUG)

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

