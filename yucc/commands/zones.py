import upcloud_api
from ..logger import Logger

class Zones:
    def __init__(self, log_level, creds):
        self.logger = Logger(log_level)
        self.creds = creds

    def run(self):
        manager = upcloud_api.CloudManager(self.creds['username'], self.creds['password'])

        self.logger.debug('Collecting zones...')
        zones = manager.get_zones()['zones']['zone']
        self.logger.debug('Zones collected')

        self.logger.normal()
        for zone in zones:
            self.logger.normal(zone['id'] + '  ' + zone['description'])

