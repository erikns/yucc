import upcloud_api
from .command_base import SdkApiBase, CommandError

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
            raise ValueError('UUID not specified')
        self.uuid = kwargs.get('uuid')

    def do_command(self):
        server = self._sdk_call(lambda: self._manager.get_server(self.uuid))
        self._output = server.to_dict()


class StartServerCommand(SdkApiBase):
    def __init__(self, logger, config, **kwargs):
        super(StartServerCommand, self).__init__(logger, config, **kwargs)
        if not kwargs.get('uuid'):
            raise ValueError('UUID not specified')
        self.uuid = kwargs.get('uuid')

    def do_command(self):
        server = self._sdk_call(lambda: self._manager.get_server(self.uuid))
        self._sdk_call(lambda: server.start())


class StopServerCommand(SdkApiBase):
    def __init__(self, logger, config, **kwargs):
        super(StopServerCommand, self).__init__(logger, config, **kwargs)
        if not kwargs.get('uuid'):
            raise ValueError('UUID not specified')
        self.uuid = kwargs.get('uuid')

    def do_command(self):
        server = self._sdk_call(lambda: self._manager.get_server(self.uuid))
        self._sdk_call(lambda: server.stop())

        self._output = {'uuid': server.uuid}


class RestartServerCommand(SdkApiBase):
    def __init__(self, logger, config, **kwargs):
        super(RestartServerCommand, self).__init__(logger, config, **kwargs)
        if not kwargs.get('uuid'):
            raise ValueError('UUID not specified')
        self.uuid = kwargs.get('uuid')

    def do_command(self):
        server = self._sdk_call(lambda: self._manager.get_server(self.uuid))
        self._sdk_call(lambda: server.restart())


class DeleteServerCommand(SdkApiBase):
    def __init__(self, logger, config, **kwargs):
        super(DeleteServerCommand, self).__init__(logger, config, **kwargs)
        if not kwargs.get('uuid'):
            raise ValueError('UUID not specified')
        self.uuid = kwargs.get('uuid')
        self.delete_storages = kwargs.get('delete_storages', False)

    def do_command(self):
        server = self._sdk_call(lambda: self._manager.get_server(self.uuid))
        self._sdk_call(lambda: server.destroy())

        if self.delete_storages:
            for storage in server.storage_devices:
                self._sdk_call(lambda: storage.destroy())


class CreateServerCommand(SdkApiBase):
    def __init__(self, logger, config, **kwargs):
        super(CreateServerCommand, self).__init__(logger, config, **kwargs)
        if not kwargs.get('hostname'):
            raise ValueError('Hostname is required')
        if not kwargs.get('plan'):
            raise ValueError('Plan is required')
        if not kwargs.get('zone'):
            raise ValueError('Zone is required')
        if not kwargs.get('ssh_key'):
            raise ValueError('SSH key is required')
        if not kwargs.get('login_user'):
            raise ValueError('Login user is required')
        if not kwargs.get('os'):
            raise ValueError('OS is required')

        self.hostname = kwargs.get('hostname')
        self.plan = kwargs.get('plan')
        self.zone = kwargs.get('zone')
        self.ssh_key = kwargs.get('ssh_key')
        self.login_user = kwargs.get('login_user')
        self.ensure_started = kwargs.get('ensure_started', False)
        self.os = kwargs.get('os')

    def do_command(self):
        loaded_ssh_key = self._load_ssh_keyfile(self.ssh_key)
        user_block = upcloud_api.login_user_block(
            username = self.login_user,
            ssh_keys = [loaded_ssh_key],
            create_password = False
        )

        server = upcloud_api.Server(
            plan = self.plan,
            hostname = self.hostname,
            zone = self.zone,
            storage_devices = [
                upcloud_api.Storage(os=self.os, size=10)
            ],
            login_user = user_block
        )
        created_server = self._sdk_call(lambda: self._manager.create_server(server))
        if self.ensure_started:
            self._sdk_call(lambda: created_server.ensure_started())

        self._output = {'uuid': created_server.uuid}

    def _load_ssh_keyfile(self, keyfile):
        with open(keyfile) as f:
            loaded_key = f.read().strip()
        return loaded_key
