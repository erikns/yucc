from .command_base import SdkApiBase, RawApiBase, CommandError


class ListTagsCommand(RawApiBase):
    def __init__(self, logger, config, **kwargs):
        super(ListTagsCommand, self).__init__(logger, config, **kwargs)
        self._expect_output = True

    def do_command(self):
        tags_response = self._http_get('/tag')
        self._output = tags_response.json()['tags']['tag']
