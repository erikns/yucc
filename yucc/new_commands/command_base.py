import json

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
