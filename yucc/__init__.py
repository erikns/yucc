# -*- coding: utf-8 -*-
"""yucc - Your UpCloud CLI.

Copyright (C) Erik Sørensen, 2017.

Usage:
    yucc ls servers [options]
    yucc ls templates [options]
    yucc ls zones [options]
    yucc ls plans [options]
    yucc ls tags [options]
    yucc server create (--hostname=<hostname>) (--plan=<plan>)
      (--login-user=<user> --ssh-key=<ssh-key>) (--os=<os>)
      [--ensure-started] [options]
    yucc server start <uuid> [options]
    yucc server stop <uuid> [options]
    yucc server restart <uuid> [options]
    yucc server delete <uuid> [--delete-storages] [options]
    yucc server info <uuid> [options]
    yucc server tag <uuid> <tag-name> [options]
    yucc server untag <uuid> <tag-name> [options]
    yucc account [options]
    yucc profile [options]
    yucc [options]

Options:
    --hostname=<hostname>      Hostname of a server
    --title=<title>            Title of a server. If not set it will be the same
                               as the hostname.
    --plan=<plan>              Plan to use for the server
    --login-user=<user>        The username to create on the server
    --ssh-key=<ssh-key>        The ssh public key to deploy to the server
    --zone=<zone>              The zone to deploy to. Default might be read from
                               profile.
    --os=<os>                  The operating system for the new server.
    --ensure-started           Wait for the server to start when creating the
                               server.
    --delete-storages          Also delete storages when deleting server
    --tags=<filter_tags>       When listing servers with ls servers, only show elements
                               with these tags (logic OR)
    --tags-operator=<op>       When matching tags, require all or one tag to be present
                               ('all' or 'one') [default: one]
    -p, --profile=<profile>    Settings profile to use. Read from
                               ~/.yuccrc file. [default: default]
    -P, --prompt-credentials   Prompt for credentials rather than reading
                               them from profile
    -q, --quiet                Be silent. Only output essential data
    -h, --help                 Show this helpscreen and exit
    -v, --verbose              Verbose output
    --debug                    Output debugging information
    --version                  Print version and exit

Commands:
    ls                         List resources (servers, templates, zones, plans, tags)
    account                    Show basic account information
    profile                    Dump profile information

"""

__version__ = '0.8.1'
__prog__ = 'yucc'
