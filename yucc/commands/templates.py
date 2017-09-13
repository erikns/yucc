from .command_base import RawApiBase


class ListTemplatesCommand(RawApiBase):
    def __init__(self, logger, config, **kwargs):
        super(ListTemplatesCommand, self).__init__(logger, config, **kwargs)

    def do_command(self):
        templates_response = self._http_get('/storage/template')

        templates = templates_response.json()['storages']['storage']
        self._output = templates
