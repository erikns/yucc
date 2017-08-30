class CommandBase(object):
    def __init__(self, logger, config, **kwargs):
        self.logger = logger
        self.username = config['username']
        self.password = config['password']
        self.default_zone = config['default_zone']
        self.format = kwargs.get('format', 'json')

        self._has_error = False
        self._output = dict()

    def run(self):
        self.do_command()

    def do_command(self):
        raise Exception('CommandBase cannot be used by itself!')

    def error(self):
        return self._has_error

    def output(self):
        return self._output
