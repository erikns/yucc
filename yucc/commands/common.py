import upcloud_api

# API call decorator
def upcloud_api_call(func):
    def func_wrapper(self):
        try:
            func(self)
        except upcloud_api.errors.UpCloudAPIError as error:
            if error.error_code == 'AUTHENTICATION_FAILED':
                self.logger.error('Authentication failed')
            else:
                self.logger.error('Unknown error occurred: ' +
                        error.error_message)
            return False

        return True
    return func_wrapper

