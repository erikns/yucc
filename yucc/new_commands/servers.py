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
