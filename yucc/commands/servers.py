import upcloud_api

from .common import upcloud_api_call
from ..logger import Logger
from ..outputter import output, raw_output

@upcloud_api_call
def list_servers(logger, creds, **kwargs):
    manager = upcloud_api.CloudManager(creds['username'], creds['password'])
    servers = manager.get_servers()
    logger.debug(str(servers))
    if len(servers) > 0:
        for server in servers:
            raw_output('server', server.to_dict())
    else:
        logger.info('There are no servers')

@upcloud_api_call
def create_server(logger, creds, **kwargs):
    logger.debug('kwargs: ' + str(kwargs))
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

    hostname = kwargs.get('hostname')
    plan = kwargs.get('plan')
    title = kwargs.get('title', hostname)
    zone = kwargs.get('zone')
    ssh_key = kwargs.get('ssh_key')
    login_user = kwargs.get('login_user')
    logger.debug('Hostname: {}, Plan: {}, Title: {}, Zone: {} User: {}'.format(hostname,
        plan, title, zone, login_user))

    try:
        with open(ssh_key) as f:
            loaded_ssh_key = f.read().strip()
    except IOError as e:
        raise ValueError('SSH key file `{}` not found'.format(ssh_key))
    logger.debug('SSH key: ' + loaded_ssh_key)

    manager = upcloud_api.CloudManager(creds['username'], creds['password'])

    user_block = upcloud_api.login_user_block(
            username=login_user,
            ssh_keys=[loaded_ssh_key],
            create_password=False)
    server = upcloud_api.Server(
        plan=plan,
        hostname=hostname,
        zone=zone,
        storage_devices=[
            upcloud_api.Storage(os='CentOS 7.0', size=10)
        ],
        login_user=user_block
    )
    created_server = manager.create_server(server)
    if kwargs.get('ensure_started', False):
        created_server.ensure_started()
    logger.normal(str(created_server))

@upcloud_api_call
def start_server(logger, creds, **kwargs):
    manager = upcloud_api.CloudManager(creds['username'], creds['password'])
    uuid = kwargs.get('uuid')
    if not uuid:
        raise ValueError('No identifier for server provided')

    server = manager.get_server(uuid)
    server.start()

    logger.info('Server {} started'.format(uuid))

@upcloud_api_call
def stop_server(logger, creds, **kwargs):
    manager = upcloud_api.CloudManager(creds['username'], creds['password'])
    uuid = kwargs.get('uuid')
    if not uuid:
        raise ValueError('No identifier for server provided')

    server = manager.get_server(uuid)
    server.shutdown()

    logger.info('Server {} stopped'.format(uuid))

@upcloud_api_call
def restart_server(logger, creds, **kwargs):
    manager = upcloud_api.CloudManager(creds['username'], creds['password'])
    uuid = kwargs.get('uuid')
    if not uuid:
        raise ValueError('No identifier for server provided')

    server = manager.get_server(uuid)
    server.restart()

    logger.info('Server {} restarted'.format(uuid))

@upcloud_api_call
def delete_server(logger, creds, **kwargs):
    manager = upcloud_api.CloudManager(creds['username'], creds['password'])
    uuid = kwargs.get('uuid')
    delete_storages = kwargs.get('delete-storages', False)
    if not uuid:
        raise ValueError('No identifier for server provided')

    server = manager.get_server(uuid)
    server.destroy()
    if delete_storages:
        for storage in server.storage_devices:
            storage.destroy()
            logger.info('Storage device {} deleted'.format(str(storage)))

    logger.info('Server {} deleted'.format(uuid))

@upcloud_api_call
def dump_server(logger, creds, **kwargs):
    manager = upcloud_api.CloudManager(creds['username'], creds['password'])
    uuid = kwargs.get('uuid')
    if not uuid:
        raise ValueError('No identifier for server provided')

    server = manager.get_server(uuid)

    raw_output('server', server.to_dict())
