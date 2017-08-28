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
    profile_name = kwargs.get('profile', 'default')

    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(os.path.expanduser('~'), '.yuccrc'))
    try:
        profile = _map_section(config, profile_name)
    except ConfigParser.NoSectionError:
        raise ValueError("No profile named '{}'".format(profile_name))

    if profile.get('default_zone'):
        default_zone = profile['default_zone']
    else:
        default_zone = None

    if read_creds:
        return {'username': profile['username'],
                'password': profile['password'],
                'default_zone' : default_zone}
    else:
        return {'default_zone': default_zone}
