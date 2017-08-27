import upcloud_api
from ..logger import Logger
from ..outputter import output
from .common import upcloud_api_call_func

@upcloud_api_call_func
def list_zones(logger, creds):
    manager = upcloud_api.CloudManager(creds['username'], creds['password'])

    logger.debug('Collecting zones...')
    zones = manager.get_zones()['zones']['zone']
    logger.debug('Zones collected')

    output('zone', zones)
