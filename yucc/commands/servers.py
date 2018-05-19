import upcloud_api
from .command_base import SdkApiBase, RawApiBase, CommandError


class ListServersCommand(SdkApiBase):
    def __init__(self, logger, config, **kwargs):
        super(ListServersCommand, self).__init__(logger, config, **kwargs)
        self.tags = kwargs.get('tags')
        self.tags_op = kwargs.get('tags_operator', 'one')

    def do_command(self):
        servers = self._sdk_call(lambda: self._manager.get_servers())
        result = list()

        # seems hacky :/ maybe move this to base class?
        for server in servers:
            if self._satisfies_tags(server):
                result.append(server.to_dict())
        self._output = result

    def _satisfies_tags(self, server, **kwargs):
        operator = self.tags_op
        self.logger.debug('operator: ' + operator)

        tags_list = self.tags.split(',')
        search_tags = set(tags_list)
        self.logger.debug(search_tags)

        server_tags = set(server.tags)
        self.logger.debug(server_tags)

        matching_tags = 0
        for tag in search_tags:
            if tag in server_tags:
                matching_tags = matching_tags + 1

        if operator == 'one':
            return matching_tags >= 1
        elif operator == 'all':
            return matching_tags == len(search_tags)
        else:
            self.logger.warning('Unsupported operator ' + operator + '. Ignoring tags!')
            return True


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
            username=self.login_user,
            ssh_keys=[loaded_ssh_key],
            create_password=False
        )

        server = upcloud_api.Server(
            plan=self.plan,
            hostname=self.hostname,
            zone=self.zone,
            storage_devices=[
                upcloud_api.Storage(os=self.os, size=10)
            ],
            login_user=user_block
        )
        created_server = self._sdk_call(lambda: self._manager.create_server(server))
        if self.ensure_started:
            self._sdk_call(lambda: created_server.ensure_started())

        self._output = {'uuid': created_server.uuid}

    def _load_ssh_keyfile(self, keyfile):
        with open(keyfile) as f:
            loaded_key = f.read().strip()
        return loaded_key


class TagServerCommand(RawApiBase):
    def __init__(self, logger, config, **kwargs):
        super(TagServerCommand, self).__init__(logger, config, **kwargs)
        self._expect_output = False
        if not kwargs.get('uuid'):
            raise ValueError('UUID needs to be supplied')
        self.uuid = kwargs.get('uuid')
        if not kwargs.get('tag_name'):
            raise ValueError('Tag name needs to be supplied')
        self.tag_name = kwargs.get('tag_name')

    def do_command(self):
        # make sure the server to tag exists first
        self._http_get('/server/' + self.uuid)

        needs_creation = False
        if self.__tag_exists():
            self.logger.debug('Tag ' + self.tag_name + ' exists')
        else:
            self.logger.debug('TAG ' + self.tag_name + ' DOES NOT EXIST!')
            needs_creation = True

        if needs_creation:
            newtag_data = {
                'tag': {
                    'name': self.tag_name
                }
            }
            self._http_post('/tag', newtag_data)
            self.logger.debug('TAG created')

        self._http_post('/server/' + self.uuid + '/tag/' + self.tag_name, None)

    def __tag_exists(self):
        tags_response = self._http_get('/tag')
        existing_tags = tags_response.json()['tags']['tag']

        requested_tag = [tag for tag in existing_tags if tag['name'] == self.tag_name]
        if len(requested_tag) == 1:
            return True
        else:
            return False


class UntagServerCommand(RawApiBase):
    def __init__(self, logger, config, **kwargs):
        super(UntagServerCommand, self).__init__(logger, config, **kwargs)
        self._expect_output = False
        if not kwargs.get('uuid'):
            raise ValueError('UUID needs to be supplied')
        self.uuid = kwargs.get('uuid')
        if not kwargs.get('tag_name'):
            raise ValueError('Tag name needs to be supplied')
        self.tag_name = kwargs.get('tag_name')

    def do_command(self):
        # make sure the server to untag exists first
        self._http_get('/server/' + self.uuid)
        self._http_post('/server/' + self.uuid + '/untag/' + self.tag_name, None)
