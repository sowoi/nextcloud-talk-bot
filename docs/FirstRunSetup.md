# Nextcloud Talk Bot: First Run Setup

## Overview

The FirstRunSetup class is designed to handle the first run setup process for a Nextcloud application. This class will prompt the user for credentials, verify them with the Nextcloud API, and store the necessary information in a local file.

## Usage

To run the FirstRunSetup, simply execute the script first_run_setup.py. The user will be guided through the setup process, and the necessary data will be stored in a file called .nextclouddata.


## Methods

get_credentials()

Executes the full setup process, verifies the credentials, and writes the data to the .nextclouddata file.


check_if_data_file_already_exists()

Checks if the .nextclouddata file exists. If it does, the user is prompted to confirm whether they want to continue and overwrite the file or abort the setup process.


encrypt_password()

This method encrypts the given password using Fernet symmetric encryption. It stores the encrypted password in a file named .password and the encryption key in a file named .decode.