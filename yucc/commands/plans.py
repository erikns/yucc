import requests

from .common import upcloud_api_call
from ..outputter import output

API_ENDPOINT = 'https://api.upcloud.com/1.2/plan'

@upcloud_api_call
def list_plans(logger, creds):
    plans_response = requests.get(API_ENDPOINT, auth=(creds['username'],
        creds['password']))
    if not plans_response.ok:
        raise upcloud_api.errors.UpCloudAPIError('AUTHENTICATION_FAILED',
            'Authentication failed')
    plans = plans_response.json()['plans']['plan']
    logger.debug(str(plans))
    output('plan', plans)
