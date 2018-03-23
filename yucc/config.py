import configparser
import os

config_path = os.path.join(os.path.expanduser('~'), '.yuccrc')


def _map_section(config, section):
    res = {}
    options = config.options(section)
    for option in options:
        try:
            res[option] = config.get(section, option)
        except:
            print("Error!")
    return res


def verify_config_permissions(logger):
    if not os.path.isfile(config_path):
        raise ValueError("No .yuccrc file found")
    logger.debug("Verifying '{}' permissions...".format(config_path))
    file_mode = str(oct(os.stat(config_path).st_mode)[-3:])
    if file_mode != '600':
        logger.warning("Config file has unsafe file permissions '{}'".format(file_mode))
    else:
        logger.info("Config file permissions are OK '{}'".format(file_mode))


def read_config(**kwargs):
    read_creds = kwargs.get('read_creds', True)
    profile_name = kwargs.get('profile', 'default')

    if not os.path.isfile(config_path):
        raise ValueError("No .yuccrc file found")
    config = configparser.RawConfigParser()
    config.read(config_path)
    try:
        profile = _map_section(config, profile_name)
    except configparser.NoSectionError:
        raise ValueError("No profile named '{}'. Choices are {}".format(profile_name,
                         config.sections()))

    if profile.get('default_zone'):
        default_zone = profile['default_zone']
    else:
        default_zone = None

    if read_creds:
        return {'username': profile['username'],
                'password': profile['password'],
                'default_zone': default_zone}
    else:
        return {'default_zone': default_zone}
