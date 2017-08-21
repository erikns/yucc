import upcloud_api

from .common import upcloud_api_call
from ..logger import Logger
from ..outputter import output

class Servers:
    def __init__(self, log_level, creds):
        self.logger = Logger(log_level)
        self.creds = creds

    @upcloud_api_call
    def run(self):
        manager = upcloud_api.CloudManager(self.creds['username'], self.creds['password'])
        servers = manager.get_servers()
        output('server', servers)

