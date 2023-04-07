import os

def create_bash_scripts():
    install_script = """#!/bin/bash

if [ "$(whoami)" == "www-data" ]; then
    php occ talk:command:add iob nc /srv/scripts/nextcloudtalkbot/nextcloud_talk_bot/nextcloud_activities.py 1 2
else
    echo "This script must be run as www-data user"
    exit 1
fi
"""

    uninstall_script = """#!/bin/bash

command_id=$(php occ talk:command:list | grep -E "iob" | awk '{print $1}')

if [ ! -z "$command_id" ]; then
    php occ talk:command:delete "$command_id"
else
    echo "No command with name 'iob' found"
fi
"""

    with open("install.sh", "w") as install_file:
        install_file.write(install_script)

    with open("uninstall.sh", "w") as uninstall_file:
        uninstall_file.write(uninstall_script)

    # Make the scripts executable
    os.chmod("install.sh", 0o755)
    os.chmod("uninstall.sh", 0o755)

create_bash_scripts()