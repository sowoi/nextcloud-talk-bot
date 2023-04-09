#/usr/bin/python3
import os
import sys
import getpass
import json
import collections
from cryptography.fernet import Fernet
from check_local_user_enviroment import check_user_and_abort_if_root_or_sudo
from nextcloud_user import NextcloudUser
from nextcloud_talk_extractor import NextcloudTalkExtractor
from nextcloud_requests import NextcloudRequests


class FirstRunSetup:
    """
    A class to handle the first run setup process for a Nextcloud application.
    This class will prompt the user for credentials, verify them with the Nextcloud API,
    and store the necessary information in a local file.
    """

    @staticmethod
    def encrypt_password(password):
        """
        Encrypts the given password using Fernet symmetric encryption.
        Stores the encrypted password in a file named '.password' and
        the encryption key in a file named '.decode'.
        
        Args:
            password (str): The plaintext password to encrypt.

        Returns:
            bytes: The encryption key.
        """
        uid = os.getuid()  
        gid = os.getgid()
        mode = 0o640
        
        # encrypt the password
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted_password = f.encrypt(password.encode())
        
        current_directory = os.path.dirname(os.path.realpath(__file__))
        password_file_path = os.path.join(current_directory,".password")
        
        # Store the encrypted text and the key in different files
        with open(password_file_path, "wb") as password_file:
            password_file.write(encrypted_password)
            
        decode_file_path = os.path.join(current_directory,".decode")
        with open(decode_file_path, "wb") as decode_file:
            decode_file.write(key)
            
        os.chown(password_file_path, uid, gid)
        os.chmod(password_file_path, mode)
        os.chown(decode_file_path, uid, gid)
        os.chmod(decode_file_path, mode) 
            
        return key

    @staticmethod
    def get_nextcloud_url():
        """Prompt the user for the Nextcloud URL and return it."""
        nextcloud_url = input("Please enter your complete Nextcloud address including https://: ")
        return nextcloud_url

    @staticmethod
    def get_username():
        """Prompt the user for the username and return it."""
        username = input("Please specify the username of the bot user:")
        return username

    @staticmethod
    def get_password():
        """Prompt the user for the password and return it."""
        password = getpass.getpass("Please enter the bot user's app password:")
        return password


    @staticmethod
    def check_nextcloud_credentials(url, username, password):
        """
        Check if the provided Nextcloud credentials are valid by calling the Nextcloud API.
        
        Args:
            url (str): The Nextcloud URL.
            username (str): The username.
            password (str): The password.

        Returns:
           (collections.namedtuple): A named tuple containing a boolean indicating if the credentials are valid and the room name.
        """
        Result = collections.namedtuple("Result", ["valid", "room"])
        user = NextcloudUser(url, username, password)
        user_data = user.test_user_login()
        user_data = json.loads(json.dumps(user_data))
        status_code = user_data["ocs"]["meta"]["statuscode"]
        if(status_code == 200):
            print("Login data are OK")
            extractor = NextcloudTalkExtractor(url, username, password)
            conversation_ids = extractor.get_conversations_ids()
            print("Found the following chats about the entered user. Select the chat by entering the number in front of it.")
            for i, rooms in enumerate(conversation_ids):
                print(f"{i+1}. {rooms}")
            roomSelection = FirstRunSetup.select_nextcloud_talk_room(conversation_ids) 
            for i, rooms in enumerate(conversation_ids):
                if i == roomSelection - 1:
                    selectedRoom = rooms
            room = conversation_ids[selectedRoom]
            return Result(valid=True, room=room)
        return Result(valid=False, room=None)

    @staticmethod
    def select_nextcloud_talk_room(conversation_ids):
        """
        Prompts the user to select the Nextcloud Talk chat room and returns its index in the list.

        Parameters:
        conversation_ids (list): The list of available Nextcloud Talk chat rooms.

        Returns:
        (int): The index of the selected chat room in the list.
        """
        while True:
            try:
                roomSelection = int(input("Please enter the number of the list item you want to select: "))
                if roomSelection < 1 or roomSelection > len(conversation_ids):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please enter a number between 1 and", len(conversation_ids), ".")
        return roomSelection

    @staticmethod
    def get_credentials():
        """
        Executes the full setup process, verifies the credentials and writes the data to the .nextclouddata file.
        """
        # Query the parameters one by one
        nextcloud_url = FirstRunSetup.get_nextcloud_url()
        username = FirstRunSetup.get_username()
        password = FirstRunSetup.get_password()

        # Verification of credentials with Nextcloud API
        result = FirstRunSetup.check_nextcloud_credentials(nextcloud_url, username, password)
        if not result.valid:
            print("Incorrect login data. Please try again.")
            return
        room = result.room
        
        # Encryption of the password and storage of the key
        FirstRunSetup.encrypt_password(password)

        # Writing the data to the .nextclouddata file
        current_directory = os.path.dirname(os.path.realpath(__file__))
        nextclouddata_file_path = os.path.join(current_directory,".nextclouddata") 
        with open(nextclouddata_file_path, "w") as data_file:
            data_file.write(f"NEXTCLOUD_URL::{nextcloud_url}\n")
            data_file.write(f"USERNAME::{username}\n")
            data_file.write(f"ROOM::{room}\n")
      
        # Delete the password from the working memory to keep it safe
        del password
        
        print(f"Data successfully written to {nextclouddata_file_path}")
        
    def check_if_data_file_already_exists():
        # Check if the .nextclouddata file exists
        current_directory = os.path.dirname(os.path.realpath(__file__))
        nextclouddata_file_path = os.path.join(current_directory,".nextclouddata")
        if os.path.exists(nextclouddata_file_path):
            print("The .nextclouddata file already exists. If you continue, this file will be overwritten.")
            while True:
                user_input = input("Are you sure you want to continue? (yes/no): ")
                if user_input.lower() == 'no':
                    print("FirstRunSetup aborted.")
                    sys.exit()
                elif user_input.lower() == 'yes':
                    print("Continuing with FirstRunSetup...")
                    break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")
        return

if __name__ == "__main__":
    FirstRunSetup.check_if_data_file_already_exists()
    check_user_and_abort_if_root_or_sudo()
    print("""This wizard guides you through the configuration of the framework.
Make sure you have created a bot user that has only limited rights.
Enable 2FA for this bot user and create an app password in Nextcloud. 
""")
    FirstRunSetup.get_credentials()
