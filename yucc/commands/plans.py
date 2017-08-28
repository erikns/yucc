from .common import upcloud_api_call, api_get
from ..outputter import output

API_RESOURCE = '/plan'

@upcloud_api_call
def list_plans(logger, creds):
    plans_response = api_get(API_RESOURCE, creds)
    if not plans_response.ok:
        raise upcloud_api.errors.UpCloudAPIError('AUTHENTICATION_FAILED',
            'Authentication failed')
    plans = plans_response.json()['plans']['plan']
    logger.debug(str(plans))
    output('plan', plans)
