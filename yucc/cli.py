import upcloud_api
from upcloud_api import ZONE

from .config import read_credentials

def main():
    creds = read_credentials()
    manager = upcloud_api.CloudManager(creds['username'], creds['password'])
    zones = manager.get_zones()['zones']['zone']
    for zone in zones:
        print zone['id'], zone['description']

