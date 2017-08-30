from .command_base import SdkApiBase

class ListServersCommand(SdkApiBase):
    def __init__(self, logger, config, **kwargs):
        super(ListServersCommand, self).__init__(logger, config, **kwargs)

    def do_command(self):
        servers = self._sdk_call(lambda: self._manager.get_servers())
        result = list()

        # seems hacky :/ maybe move this to base class?
        for server in servers:
            result.append(server.to_dict())
        self._output = result


class DumpServerInfoCommand(SdkApiBase):
    def __init__(self, logger, config, **kwargs):
        super(DumpServerInfoCommand, self).__init__(logger, config, **kwargs)
        if not kwargs.get('uuid'):
            raise Exception('UUID not specified')
        self.uuid = kwargs.get('uuid')

    def do_command(self):
        server = self._sdk_call(lambda: self._manager.get_server(self.uuid))
        self._output = server.to_dict()


class StartServerCommand(SdkApiBase):
    def __init__(self, logger, config, **kwargs):
        super(StartServerCommand, self).__init__(logger, config, **kwargs)
        if not kwargs.get('uuid'):
            raise Exception('UUID not specified')
        self.uuid = kwargs.get('uuid')

    def do_command(self):
        server = self._sdk_call(lambda: self._manager.get_server(self.uuid))
        self._sdk_call(lambda: server.start())


class StopServerCommand(SdkApiBase):
    def __init__(self, logger, config, **kwargs):
        super(StopServerCommand, self).__init__(logger, config, **kwargs)
        if not kwargs.get('uuid'):
            raise Exception('UUID not specified')
        self.uuid = kwargs.get('uuid')

    def do_command(self):
        server = self._sdk_call(lambda: self._manager.get_server(self.uuid))
        self._sdk_call(lambda: server.stop())
