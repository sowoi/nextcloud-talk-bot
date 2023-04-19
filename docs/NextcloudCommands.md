# Nextcloud Talk Bot: Commands
Unfortunately, in the current versions of Nextcloud Talk it is not possible to add commands via API. 
As a workaround, there are two scripts:

# setup_nextcloud_talk_bot.sh

This Bash script is designed to create the necessary commands for the bot user's Nextcloud Talk Commandos automatically. The script will create a Python Venv environment in which the necessary modules are installed. 
After that, a Python script is downloaded from the Github repository. The script must run on a server with Nextcloud installed, and the calling user should have the ability to call commands as www-data. 
During the process, the script will ask for the username and password of a bot user. Please ensure that you do not use an administration account and create an app password for the bot user. 
If the directory where the script was started is deleted, you will have to start the setup from scratch.
The script creates a wrapper for ncbot.py called ncbot.sh which has the sole purpose of starting ncbot.py via Python Venv. 

```
# Install / uninstall
./setup_nextcloud_talk.sh [--uninstall]

# Setup
./setup_nextcloud_talk.sh --setup
```

The script takes an optional --uninstall argument to uninstall the Nextcloud Talk Commando created by the script.

## Functions
create_virtualenv()  
This function creates a Python Venv environment in which the necessary modules are installed. If the script is already running in a virtual environment, it will inform the user. The virtual environment is activated, and the necessary package is installed using pip.

uninstall()  
This function uninstalls the NextcloudTalkBot package and removes the virtual environment. If the script is not running in a virtual environment, it will ask for the Nextcloud installation directory. After that, it will get the ID of the "ncb" command, and if it exists, it will remove it.

main()  
This function is the main function of the script. It checks if the script is running as the 'www-data' user and creates the virtual environment. It then asks for the Nextcloud installation directory, who should see the response, and who can use the command. After that, it downloads the ncbot.py script from the Github repository and allows access for www-data to the script. 
It creates a ncbot.sh script that will be used to run the ncbot.py script. It then adds the ncb command to the Nextcloud Talk Commandos and starts the first run setup.
Security
To make the script more secure, we use the set -u option to avoid using undefined variables. We also check if the script is running in a virtual environment before executing any commands. This ensures that the script does not accidentally use the wrong version of Python or any other dependencies.


# ncbot.py
This module provides a Python framework to call Nextcloud commands via NextcloudTalkBot. 

## FirstSetup

The FirstSetup class creates logindata for your bot users and saves them securely. See [FirstRunSetup](FirstRunSetup) for more information about this.

## NextcloudCommands

The NextcloudCommands class is designed to print the docstrings of classes and methods from specified modules. This class requires the following parameters which it derrives from the FirstSetup process:

input_name: The name of the input used to map to a module.
base_url: The base URL of your Nextcloud instance (optional).
username: Your Nextcloud username (optional).
password: Your Nextcloud password (optional).
room_name: The name of the Nextcloud Talk room (optional).

NextcloudCommands includes the following methods:

map_input_to_module(): A method that maps an input name to a module.
load_module(): A method that loads the module.
get_first_class(): A method that retrieves the first class of the module.
print_first_class_docstring(): A method that prints the docstring of the first class of the module.
print_method_docstring(): A method that prints the docstring of the method.
call_class_method(): A method that calls the class method with arguments.
print_available_classes_and_methods(): A method that prints the available classes and methods of the module.
print_method_parameters(): A method that prints the parameters of the method.
print_available_classes(): A method that prints the available options.

## NLPCommands

This class provides natural language processing (NLP) functionality to classify user intents and extract relevant information from user queries. 
It uses the spaCy library for NLP and includes methods to classify user intents related to polls, users, messages, activities, files, meetings, search, and calendar events.

To use Spacy as a Natural Language Processor, it is necessary to download a model.

```
python -m spacy download en_core_web_sm
```
The command downloads the model for the English language file. 

## Usage

```SHELL
python ncbot.py [--function METHOD_NAME] [--args [ARGS ...]] [--help] [--list] [--setup] [input_name]
```

The following arguments are available:

- input_name: The name of the input used to map to a module.
- --function, -f: The name of the function to call.
- --args, -a: The arguments to pass to the function.
- --help, -h: Print help.
- --list, -l: List available options or functions.
- --setup, -s: Run the first run setup.



# Use in the Nextcloud Talk app:

The new commands are started directly in the chat with /ncb.

## Examples

```
# print help
/ncb -h 

# show list of options
/ncb -l

# show list of functions
/ncb <option> -l

# run function
/ncb <option> <function>

# print help to option or function
/ncb <option>/<function> -h
```
