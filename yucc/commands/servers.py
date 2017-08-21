import upcloud_api

from .common import upcloud_api_call
from ..logger import Logger

class Servers:
    def __init__(self, log_level, creds):
        self.logger = Logger(log_level)

    def run(self):
        self.logger.critical('Command to list servers is not implemented yet')
        return False

