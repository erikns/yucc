# YUCC - Your UpCloud CLI

A CLI for the UpCloud API. Still a work in progress.

## Installation and configuration

### Install from source

Clone the repository and run `pip install .`, either globally or in a virtual
environment.

### Install from PyPI

Run `pip install yucc`. You may need to prepend the command with `sudo`

### Configuration

The CLI makes use of a hidden `.yuccrc`-file in your home directory. This is an
example of what it looks like:
```
[default]
username = user
password = passw0rd
default_zone = de-fra1

[profile2]
username = other_user
password = passw0rd
```
This file defines profiles for the CLI to use. If none is specified, it uses
`default` (by default). Make shure this file is accessible only by your user
(600 permissions), as it does contain sensitive information.

Run `yucc --help` or `yucc -h` to get a glimpse of what the tool offers.

## Usage

To list the plans that are available, type: `yucc ls plans`

To list the zones that are available, type: `yucc ls zones`

To create a server, do something like this:
```bash
yucc server create --hostname server1 --plan 1xCPU-1GB \
    --os "CentOS 7.0" \
    --login-user user --ssh-key ssh_public_key_file.pub \
    --ensure-started
```
The tool returns the UUID of the created server. The server is created in the
default zone specified in the default profile. To override the zone, add the
`--zone <zone>` parameter.

To restart an existing server, type: `yucc server restart <uuid>`

To stop an existing server, type: `yucc server stop <uuid>`

To remove an existing server, type: `yucc server delete <uuid>`. To also delete
storage devices associated with the server, add the `--delete-storages` flag.

To list all servers, run: `yucc ls servers`.

## Todo

- Add tags on server creation
- IP address management, including listing IPs, assigning, etc...
- Storage management, attaching, detaching, etc...

## Contributing

If you feel a feature is missing, find a bug or have any suggestions, please
feel free to create an issue or open a pull request :)

## License

The project is MIT licensed.
