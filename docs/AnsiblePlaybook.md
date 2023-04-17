# Nextcloud Talk Bot: Setup via Ansible
This Ansible playbook sets up a Nextcloud Talk bot on your Nextcloud server.

## Overview

The playbook performs the following tasks:

- Ensure the installation directory exists.
- Create a Python virtual environment.
- Install the NextcloudTalkBot package in the virtual environment.
- Download the ncbot.py script from Github.
- Create the ncbot.sh script.
- Set the ownership of the ncbot.py and ncbot.sh files.
- Add the Nextcloud Talk command.
- Run the first-time setup for the bot.

## Variables

The playbook uses the following variables:

- install_directory: The path to the directory where the bot will be installed.
- nextcloud_directory: The path to the Nextcloud installation directory.
- response: The response mode for the bot (default 2: send system messages).
- enabled: The enabled state for the bot command (default 2: enabled for all user).

## Tasks
Ensure install directory exists  
This task creates the installation directory if it does not exist.

Create virtual environment  
This task creates a Python virtual environment in the installation directory.

Install NextcloudTalkBot in virtual environment  
This task installs the nextcloudtalkbot package in the virtual environment.  

Download ncbot.py from Github  
This task downloads the ncbot.py script from the Github repository and saves it in the installation directory with executable permissions.

Create ncbot.sh  
This task creates the ncbot.sh script in the installation directory, which is a wrapper around the ncbot.py script. The script sets the correct virtual environment and Python interpreter.

Set ownership of ncbot files  
This task sets the ownership of the ncbot.py and ncbot.sh files to the www-data user and group.

Add Nextcloud Talk command  
This task adds the Nextcloud Talk command using the occ command-line tool. The command is registered with the bot's script, response mode, and enabled state.

Run first-time setup  
This task runs the first-time setup for the bot by calling the ncbot.sh script with the --setup flag. The setup process configures the bot for the Nextcloud Talk instance.