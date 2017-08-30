
import requests
from .command_base import CommandBase

class AccountCommand(CommandBase):
    ROOT_API_ENDPOINT = 'https://api.upcloud.com/1.2'
    RESOURCE = '/account'

    def __init__(self, logger, config, **kwargs):
        super(AccountCommand, self).__init__(logger, config, **kwargs)

    def do_command(self):
        account_response = requests.get(AccountCommand.ROOT_API_ENDPOINT +
            AccountCommand.RESOURCE, auth=(self.username, self.password))
        if not account_response.ok:
            self._report_error('Authentication failed')
            return
        account = account_response.json()['account']

        self._output = {
            'username': account['username']
        }
        if 'credits' in account:
            self._output['credits'] = account['credits']
        else:
            self.logger.info('No credits information in output. Do you have billing access?')
