import requests
import upcloud_api

from ..logger import Logger
from ..outputter import output
from .common import upcloud_api_call, api_get

# This is hacked in as the python SDK didn't have this feature
API_RESOURCE = '/storage/template'

@upcloud_api_call
def list_templates(logger, creds):
    storages_response = api_get(API_RESOURCE, creds)
    if not storages_response.ok:
        raise upcloud_api.errors.UpCloudAPIError('AUTHENTICATION_FAILED',
                'Authentication failed')
    storages = storages_response.json()['storages']['storage']
    output('template', storages)
