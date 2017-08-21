import upcloud_api
from ..logger import Logger
from ..outputter import output
from .common import upcloud_api_call

class Zones:
    def __init__(self, log_level, creds):
        self.logger = Logger(log_level)
        self.creds = creds

    @upcloud_api_call
    def run(self):
        manager = upcloud_api.CloudManager(self.creds['username'], self.creds['password'])

        self.logger.debug('Collecting zones...')
        zones = manager.get_zones()['zones']['zone']
        self.logger.debug('Zones collected')

        output('zone', zones)

