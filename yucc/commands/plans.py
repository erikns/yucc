import requests
from .command_base import RawApiBase


class ListPlansCommand(RawApiBase):
    RESOURCE = '/plan'

    def __init__(self, logger, config, **kwargs):
        super(ListPlansCommand, self).__init__(logger, config, **kwargs)

    def do_command(self):
        plans_response = self._http_get(ListPlansCommand.RESOURCE)

        plans = plans_response.json()['plans']['plan']
        self._output = plans
