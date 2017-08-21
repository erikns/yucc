import upcloud_api
from ..logger import Logger
from ..outputter import output

class Zones:
    def __init__(self, log_level, creds):
        self.logger = Logger(log_level)
        self.creds = creds

    def run(self):
        try:
            manager = upcloud_api.CloudManager(self.creds['username'], self.creds['password'])

            self.logger.debug('Collecting zones...')
            zones = manager.get_zones()['zones']['zone']
            self.logger.debug('Zones collected')

            output('zone', zones)
        except upcloud_api.errors.UpCloudAPIError as error:
            if error.error_code == 'AUTHENTICATION_FAILED':
                self.logger.error('Authentication failed')
            else:
                self.logger.error('Unknown error occurred: ' +
                        error.error_message)
            return False

        return True

