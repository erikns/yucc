import requests
import upcloud_api

from ..logger import Logger
from ..outputter import output
from .common import upcloud_api_call

# This is hacked in as the python SDK didn't have this feature
class Templates:
    API_ENDPOINT = 'https://api.upcloud.com/1.2/storage/template'

    def __init__(self, log_level, creds):
        self.logger = Logger(log_level)
        self.creds = creds

    @upcloud_api_call
    def run(self):
        storages_response = requests.get(self.API_ENDPOINT, auth=(self.creds['username'], 
            self.creds['password']))
        if not storages_response.ok:
            raise upcloud_api.errors.UpCloudAPIError('AUTHENTICATION_FAILED',
                    'Authentication failed')
        storages = storages_response.json()['storages']['storage']
        output('template', storages)

