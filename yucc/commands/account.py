import requests
import upcloud_api

from ..logger import Logger
from .common import upcloud_api_call, api_get

API_RESOURCE = '/account'

@upcloud_api_call
def show_account_info(logger, creds, **kwargs):
    account_response = api_get(API_RESOURCE, creds)
    if not account_response.ok:
        raise upcloud_api.errors.UpCloudAPIError('AUTHENTICATION_FAILED',
                'Authentication error')
    account = account_response.json()['account']
    logger.normal('Username: ' + account['username'])
    if 'credits' in account:
        logger.normal("Credits:  ${0:.2f}".format(account['credits'] /
            100))
    else:
        logger.info("No credits information in output." +
            " Do you have billing access?")
