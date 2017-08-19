import upcloud_api
from upcloud_api import ZONE
import ConfigParser
import os

def map_section(config, section):
    res = {}
    options = config.options(section)
    for option in options:
        try:
            res[option] = config.get(section, option)
        except:
            print "Error!"
    return res

def read_credentials():
    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(os.path.expanduser('~'), '.yuccrc'))
    creds = map_section(config, 'default')
    return {'username': creds['username'],
            'password': creds['password']}

def main():
    creds = read_credentials()
    manager = upcloud_api.CloudManager(creds['username'], creds['password'])
    zones = manager.get_zones()['zones']['zone']
    for zone in zones:
        print zone['id'], zone['description']

