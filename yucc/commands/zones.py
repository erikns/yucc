import upcloud_api
from ..logger import Logger
from ..outputter import output
from .common import upcloud_api_call

@upcloud_api_call
def list_zones(logger, creds, **kwargs):
    manager = upcloud_api.CloudManager(creds['username'], creds['password'])

    logger.debug('Collecting zones...')
    zones = manager.get_zones()['zones']['zone']
    logger.debug('Zones collected')

    output('zone', zones)
