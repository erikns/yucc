import json
import requests
import upcloud_api


class AuthenticationError:
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


class CommandError:
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


class NotFoundError:
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
        self._output = None
        self._expect_output = True

    def run(self):
        try:
            self.do_command()
        except AuthenticationError as e:
            self._report_error('Authentication failed')
            self.logger.debug('Exception: {}'.format(e))
        except CommandError as e:
            self._report_error(str(e))
        except NotFoundError as e:
            self._report_error(str(e))
        except Exception as e:
            if str(e).startswith('Invalid OS'):
                self._report_error('{}'.format(e))
            else:
                self._report_error('Exception: {}'.format(e))

    def do_command(self):
        raise Exception('CommandBase cannot be used by itself!')

    def has_error(self):
        return len(self._errors) > 0

    def errors(self):
        return self._errors

    def _report_error(self, error):
        self._errors.append(error)

    def output(self):
        if self._output:
            return json.dumps(self._output, sort_keys=True,
                              indent=4, separators=(',', ': '))
        elif self._expect_output:
            return json.dumps([])


class RawApiBase(CommandBase):
    ROOT_API_ENDPOINT = 'https://api.upcloud.com/1.2'

    def __init__(self, logger, config, **kwargs):
        super(RawApiBase, self).__init__(logger, config, **kwargs)
        self._http_auth = (self.username, self.password)

    def _http_get(self, resource):
        response = requests.get(RawApiBase.ROOT_API_ENDPOINT + resource,
                                auth=self._http_auth)
        if response.ok:
            return response
        elif response.status_code == 401:
            raise AuthenticationError('Authentication failed with username {}'.format(self.username))
        elif response.status_code == 404:
            raise NotFoundError('Resource not found')
        else:
            raise CommandError('Generic error executing HTTP request. Response code: {}'.format(
                               response.status_code))

    def _http_post(self, resource, data):
        response = requests.post(RawApiBase.ROOT_API_ENDPOINT + resource, json=data, auth=self._http_auth)

        if response.ok:
            return response
        elif response.status_code == 401:
            raise AuthenticationError('Authentication failed with username {}'.format(self.username))
        elif response.status_code == 404:
            raise NotFoundError('Resource not found')
        else:
            raise CommandError('Generic error executing HTTP request. Response code: {}'.format(
                response.status_code))


class SdkApiBase(CommandBase):
    def __init__(self, logger, config, **kwargs):
        super(SdkApiBase, self).__init__(logger, config, **kwargs)
        self._manager = upcloud_api.CloudManager(self.username, self.password)

    def _sdk_call(self, func):
        try:
            return func()
        except upcloud_api.errors.UpCloudAPIError as e:
            if e.error_code == 'AUTHENTICATION_FAILED':
                raise AuthenticationError(e.error_message)
            elif e.error_code == 'SERVER_NOT_FOUND':
                raise CommandError('The server does not exist')
            elif e.error_code in ['ZONE_NOT_FOUND', 'SERVER_INVALID']:
                raise CommandError(e.error_message)
            elif e.error_code == 'UNAUTHORIZED_ADDRESS':
                raise CommandError('Your account cannot access the API on this ip address')
            else:
                self.logger.debug('{}: {}'.format(e.error_code, e.error_message))
                raise CommandError('Unknown error {} {}'.format(e.error_code, e.error_message))
