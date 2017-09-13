
import requests
from .command_base import RawApiBase


class AccountCommand(RawApiBase):
    RESOURCE = '/account'

    def __init__(self, logger, config, **kwargs):
        super(AccountCommand, self).__init__(logger, config, **kwargs)

    def do_command(self):
        account_response = self._http_get(AccountCommand.RESOURCE)
        account = account_response.json()['account']

        self._output = {
            'username': account['username']
        }
        if 'credits' in account:
            self._output['credits'] = account['credits']
        else:
            self.logger.info('No credits information in output. Do you have billing access?')
