import requests
from ..logger import Logger

# This is hacked in as the python SDK didn't have this feature
class Templates:
    API_ENDPOINT = 'https://api.upcloud.com/1.2/storage/template'

    def __init__(self, log_level, creds):
        self.logger = Logger(log_level)
        self.creds = creds

    def run(self):
        storages_response = requests.get(self.API_ENDPOINT, auth=(self.creds['username'], 
            self.creds['password']))
        storages = storages_response.json()['storages']['storage']
        for storage in storages:
            self.logger.normal(storage['uuid'] + ' ' + storage['title'])

