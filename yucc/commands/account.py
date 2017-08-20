import requests
from ..logger import Logger

class Account:
    API_ENDPOINT = 'https://api.upcloud.com/1.2/account'

    def __init__(self, log_level, creds):
        self.logger = Logger(log_level)
        self.creds = creds

    def run(self):
        account_response = requests.get(self.API_ENDPOINT,
                auth=(self.creds['username'], self.creds['password']))
        account = account_response.json()['account']
        self.logger.normal('Username: ' + account['username'])
        if 'credits' in account:
            self.logger.normal("Credits:  ${0:.2f}".format(account['credits'] /
                100))

