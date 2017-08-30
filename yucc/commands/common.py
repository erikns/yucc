import upcloud_api
import requests

ROOT_API_ENDPOINT = 'https://api.upcloud.com/1.2'
DEFAULT_OUTPUT_FORMAT = 'table'

def api_get(resource, config):
    return requests.get(ROOT_API_ENDPOINT + resource,
        auth=(config['username'], config['password']))

# API call decorator
def upcloud_api_call(func):
    def func_wrapper(logger, creds, **kwargs):
        try:
            func(logger, creds, **kwargs)
        except upcloud_api.errors.UpCloudAPIError as error:
            if error.error_code == 'AUTHENTICATION_FAILED':
                logger.error('Authentication failed')
                _report_error_debug(logger, error)
            elif error.error_code == 'SERVER_NOT_FOUND':
                logger.error('The server was not found')
            else:
                logger.error('Unknown error occurred: ' +
                        error.error_message)
                _report_error_debug(logger, error)
            return False
        except ValueError as error:
            logger.error(error.message)
            return False
        except Exception as error:
            logger.debug(error.message)
            logger.error('Unknown error occurred')
            raise error

        return True
    return func_wrapper

def _report_error_debug(logger, err):
    logger.debug('Code: {} Message: {}'.format(err.error_code,
    err.error_message))
