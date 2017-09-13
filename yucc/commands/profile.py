from .command_base import CommandBase


class ProfileCommand(CommandBase):
    def __init__(self, logger, config, **kwargs):
        super(ProfileCommand, self).__init__(logger, config, **kwargs)

    def do_command(self):
        self._output = {
            'default_zone': self.default_zone
        }
