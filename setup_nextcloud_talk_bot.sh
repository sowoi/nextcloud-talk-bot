#!/bin/bash
#
# This script creates the necessary commands for the bot user's Nextcloud Talk Commandos fully automatically. 
# During the process, a Python Venv environment is created in which the necessary modules are installed. After that, a Python script is downloaded from my Github repository. Which gives execute permissions for www-data. 
# This bash script must run on a server with Nextcloud installed. The calling user should have the possibility to call commands as www-data. During the process it will ask for username and password of a bot user. 
# Please do not use an administration account! Create an app password for the bot user. 
# If the directory where the script was started is deleted, you will have to start the setup from scratch. 
#

set -u
create_virtualenv() {
  # Check if the script is already running in a virtual environment
  if [[ $VIRTUAL_ENV != "" ]]; then 
    echo 'Script is already running in a virtual environment.'
    which python                             
  else
    # Create a new virtual environment
    python3 -m venv .venv
    echo 'Virtual environment created.'

    # Activate the virtual environment
    source ./.venv/bin/activate
    which python

    # Install the package using pip
    pip install nextcloudtalkbot
    echo 'NextcloudTalkBot installed.'
  fi
}

uninstall() {
  # Check if the script is running in a virtual environment
  if [[ $VIRTUAL_ENV != "" ]]; then 


    # Uninstall the package using pip
    pip uninstall nextcloudtalkbot
    echo 'NextcloudTalkBot uninstalled.'

    # Deactivate the virtual environment
    deactivate

    # Remove the virtual environment
    rm -rf .venv
    echo 'Virtual environment removed.'

    echo "The 'ncb' command with ID '$ncb_id' has been removed."
  else
    read -p "Please enter the Nextcloud installation directory: " nextcloud_directory
    # Get the ID of the "ncb" command                                                                                                                                                                                                                       
    ncb_id=$(sudo -u www-data php ${nextcloud_directory}/occ talk:command:list| grep nct | cut -d '|' -f 2)
    if [ -z "$ncb_id" ]; then
	echo "Bot not found in Nextcloud Talk"
    else
	echo "ncb_id"
	ncb_id_w=${ncb_id// /}
	command="sudo -u www-data php ${nextcloud_directory}/occ talk:command:delete $ncb_id_w"
	echo "Running $command"

	if ! $command; then
	    echo "An error occurred while executing the command."
	    exit 1
	fi
    fi

    echo 'No virtual environment found. Nothing to uninstall.'
  fi
}

main() {
  current_user=$(getent passwd www-data | cut -d: -f1)
  if [ "$current_user" != "www-data" ]; then
    echo "This script must be run as the 'www-data' user."
    exit 1
  fi

  if [[ "$1" == "--uninstall" ]]; then
    uninstall
    exit 0
  fi
  
  create_virtualenv
  
  read -p "Please enter the Nextcloud installation directory: " nextcloud_directory
  read -p "Who should see the response: 0 - No one, 1 - User, 2 - All [Enter 0 - 2]: " response
  read -p "Who can use this command: 0 - Disabled, 1 - Moderators, 2 - Users, 3 - Guests [Enter 0 -3]: " enabled

  echo "Downloading ncbot.py"

  wget https://raw.githubusercontent.com/sowoi/nextcloud-talk-bot/main/nextcloud_talk_bot/ncbot.py
  source ./.venv/bin/activate

  PYTHON_PATH=$(which python)
  echo $PYTHON_PAH

  echo "Allow access for www-data to the script ncbot.py"

  script_directory=$(dirname "$(realpath "$0")")

cat <<EOF > ncbot.sh
#!/usr/bin/env bash
set -u
args="\$@"
eval "$script_directory/.venv/bin/python $script_directory/ncbot.py \$args"
EOF

  chown www-data:www-data ncbot.*
  chmod u+x ncbot.*
  SCRIPT_PATH="$script_directory/ncbot.sh {ARGUMENTS}"

  echo $SCRIPT_PATH

  command="sudo -u www-data php ${nextcloud_directory}/occ talk:command:add ncb nct \"$SCRIPT_PATH\" ${response} ${enabled}"
  echo "Running $command"
  eval "$command"
  echo "Command executed successfully."

  echo "Starting first run setup"

  eval "sudo -u www-data ${script_directory}/ncbot.sh --setup"

  echo "Setup executed successfully."
  

  

  deactivate
}

if [[ "$1" == "--uninstall" ]]; then
  uninstall
else
  main
fi
