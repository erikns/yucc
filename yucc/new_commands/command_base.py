import json
import requests
import upcloud_api

class AuthenticationError:
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message

class CommandBase(object):
    def __init__(self, logger, config, **kwargs):
        self.logger = logger
        self.username = config['username']
        self.password = config['password']
        self.default_zone = config['default_zone']
        self.format = kwargs.get('format', 'json')

        self._errors = []
        self._output = dict()

    def run(self):
        try:
            self.do_command()
        except Exception as e:
            self._report_error('Exception: {}'.format(e))
            raise e

    def do_command(self):
        raise Exception('CommandBase cannot be used by itself!')

    def has_error(self):
        return len(self._errors) > 0

    def errors(self):
        return self._errors

    def _report_error(self, error):
        self._errors.append(error)

    def output(self):
        return json.dumps(self._output, sort_keys=True,
                indent=4, separators=(',', ': '))


class RawApiBase(CommandBase):
    ROOT_API_ENDPOINT = 'https://api.upcloud.com/1.2'

    def __init__(self, logger, config, **kwargs):
        super(RawApiBase, self).__init__(logger, config, **kwargs)
        self._http_auth = (self.username, self.password)

    def run(self):
        try:
            self.do_command()
        except AuthenticationError as e:
            self._report_error('Authentication failed')
            self.logger.debug('AuthenticationError: {}'.format(e))
        except Exception as e:
            self._report_error('Exception: {}'.format(e))
            raise e

    def _http_get(self, resource):
        response = requests.get(RawApiBase.ROOT_API_ENDPOINT + resource,
            auth=self._http_auth)
        if response.ok:
            return response
        elif response.status_code == 401:
            raise AuthenticationError('Authentication failed with username {}'.format(self.username))
        else:
            raise Exception('Generic error executing HTTP request. Response code: {}'.format(response.status_code))


class SdkApiBase(CommandBase):
    def __init__(self, logger, config, **kwargs):
        super(SdkApiBase, self).__init__(logger, config, **kwargs)
        self._manager = upcloud_api.CloudManager(self.username, self.password)

    def run(self):
        try:
            self.do_command()
        except upcloud_api.errors.UpCloudAPIError as e:
            self._report_error(e.error_message)
            self.logger.debug('Exception: {}'.format(e))
        except Exception as e:
            self._report_error('Exception: {}'.format(e))
            raise e
