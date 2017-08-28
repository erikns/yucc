import upcloud_api
import requests

ROOT_API_ENDPOINT = 'https://api.upcloud.com/1.2'

def api_get(resource, config):
    return requests.get(ROOT_API_ENDPOINT + resource,
        auth=(config['username'], config['password']))

# API call decorator
def upcloud_api_call(func):
    def func_wrapper(logger, creds):
        try:
            func(logger, creds)
        except upcloud_api.errors.UpCloudAPIError as error:
            if error.error_code == 'AUTHENTICATION_FAILED':
                logger.error('Authentication failed')
            else:
                logger.error('Unknown error occurred: ' +
                        error.error_message)
            return False

        return True
    return func_wrapper
