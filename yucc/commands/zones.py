from .command_base import SdkApiBase


class ListZonesCommand(SdkApiBase):
    def __init__(self, logger, config, **kwargs):
        super(ListZonesCommand, self).__init__(logger, config, **kwargs)

    def do_command(self):
        zones = self._sdk_call(lambda: self._manager.get_zones()['zones']['zone'])
        self._output = zones
