# Nextcloud Talk Bot: First Run Setup

## Overview

The FirstRunSetup class is designed to handle the first run setup process for a Nextcloud application. This class will prompt the user for credentials, verify them with the Nextcloud API, and store the necessary information in a local file.

## Usage

To run the FirstRunSetup, import the wizard by 
```
from nextcloud_talk_bot.first_run_setup import FirstRunSetup

FirstRunSetup.first_run()                                                                                                   
```
The user will be guided through the setup process, and the necessary data will be stored in a file called .nextclouddata in your home directory.
The login data for the server is stored in user directory $HOME/.nextclouddata.


## Security

The password is stored encrypted in the usepath in the .password file.
The corresponding decryption password is stored in .decode. 
Alternatively, the decryption password can be stored in the NCDECODE environment variable and the user password in the NCPASSWORD environment variable.
A mix of storing decryption password in environment variable and password in .password file or vice versa is also possible and recommended.

However, since third parties can read the password with little effort as soon as they have access to your system, it is advisable not to use admin users for this package.

## Methods

1. get_credentials()

Executes the full setup process, verifies the credentials, and writes the data to the .nextclouddata file.


2. check_if_data_file_already_exists()

Checks if the .nextclouddata file exists. If it does, the user is prompted to confirm whether they want to continue and overwrite the file or abort the setup process.


3. encrypt_password()

This method encrypts the given password using Fernet symmetric encryption. It stores the encrypted password in a file named .password and the encryption key in a file named .decode.


## Exmples

```
from nextcloud_talk_bot.Nextcloudtalkbot import NextcloudTalkBot

bot = NextcloudTalkBot()
url = bot.NEXTCLOUD_URL
username = bot.USERNAME
password = bot.PASSWORD

# get preferred language of user
user = NextcloudUser(url, username, password)
preferred_language = user.get_preferred_language()
print(preferred_language)

# search for activity "event"
event = NextcloudActivities(url, username, password)
search_event = event.search_last_activities("event")
print(search_event)


```