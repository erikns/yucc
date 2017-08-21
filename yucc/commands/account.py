import requests
import upcloud_api

from ..logger import Logger
from .common import upcloud_api_call

class Account:
    API_ENDPOINT = 'https://api.upcloud.com/1.2/account'

    def __init__(self, log_level, creds):
        self.logger = Logger(log_level)
        self.creds = creds

    @upcloud_api_call
    def run(self):
        account_response = requests.get(self.API_ENDPOINT,
                auth=(self.creds['username'], self.creds['password']))
        if not account_response.ok:
            raise upcloud_api.errors.UpCloudAPIError('AUTHENTICATION_FAILED',
                    'Authentication error')
        account = account_response.json()['account']
        self.logger.normal('Username: ' + account['username'])
        if 'credits' in account:
            self.logger.normal("Credits:  ${0:.2f}".format(account['credits'] /
                100))

