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

def read_config(**kwargs):
    read_creds = kwargs.get('read_creds', True)

    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(os.path.expanduser('~'), '.yuccrc'))
    default_profile = _map_section(config, 'default')

    if read_creds:
        return {'username': default_profile['username'],
                'password': default_profile['password']}
    else:
        return {}
