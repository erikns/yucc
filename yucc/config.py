import ConfigParser
import os

def _map_section(config, section):
    res = {}
    options = config.options(section)
    for option in options:
        try:
            res[option] = config.get(section, option)
        except:
            print "Error!"
    return res

def read_config():
    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(os.path.expanduser('~'), '.yuccrc'))
    creds = _map_section(config, 'default')
    return {'username': creds['username'],
            'password': creds['password']}
