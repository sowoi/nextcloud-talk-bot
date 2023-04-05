import getpass
import json
import collections
from cryptography.fernet import Fernet
from get_user import get_user_data
from get_conversation_id import extract_talk_conversation_ids

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
        # encrypt the password
        key = Fernet.generate_key()
        f = Fernet(key)
        encrypted_password = f.encrypt(password.encode())
        
        # Store the encrypted text and the key in different files
        with open(".password", "wb") as password_file:
            password_file.write(encrypted_password)
        
        with open(".decode", "wb") as decode_file:
            decode_file.write(key)
            
        return key

    @staticmethod
    def get_nextcloud_url():
        """Prompt the user for the Nextcloud URL and return it."""
        nextcloud_url = input("Nextcloud-URL: ")
        return nextcloud_url

    @staticmethod
    def get_username():
        """Prompt the user for the username and return it."""
        username = input("Username: ")
        return username

    @staticmethod
    def get_password():
        """Prompt the user for the password and return it."""
        password = getpass.getpass("Password: ")
        return password

    @staticmethod
    def get_room():
        """Prompt the user for the room and return it."""
        room = input("Room: ")
        return room

    @staticmethod
    def get_nc_remote_folder():
        """Prompt the user for the Nextcloud remote folder and return it."""
        nc_remote_folder = input("Nextcloud folder for file uploads: ")
        return nc_remote_folder

    @staticmethod
    def check_nextcloud_credentials(url, username, password, room):
        """
        Check if the provided Nextcloud credentials are valid by calling the Nextcloud API.
        
        Args:
            url (str): The Nextcloud URL.
            username (str): The username.
            password (str): The password.
            room (str): The room.

        Returns:
           (collections.namedtuple): A named tuple containing a boolean indicating if the credentials are valid and the room name.        """
        Result = collections.namedtuple("Result", ["valid", "room"])
        user_data = (get_user_data(url, username, password))
        user_data = json.loads(json.dumps(user_data))
        status_code = user_data["ocs"]["meta"]["statuscode"]
        if(status_code == 200):
            print("Login data are OK")
            conversation_ids = extract_talk_conversation_ids(url, username, password)
            print(conversation_ids)
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
        room = FirstRunSetup.get_room()
        nc_remote_folder = FirstRunSetup.get_nc_remote_folder()

        # Verification of credentials with Nextcloud API
        result = FirstRunSetup.check_nextcloud_credentials(nextcloud_url, username, password, room)
        if not result.valid:
            print("Incorrect login data. Please try again.")
            return
        room = result.room
        
        # Encryption of the password and storage of the key
        FirstRunSetup.encrypt_password(password)

        # Writing the data to the .nextclouddata file
        with open(".nextclouddata", "w") as data_file:
            data_file.write(f"NEXTCLOUD_URL::{nextcloud_url}\n")
            data_file.write(f"USERNAME::{username}\n")
            data_file.write(f"ROOM::{room}\n")
            data_file.write(f"NC_REMOTE_FOLDER::{nc_remote_folder}\n")
       
        # Delete the password from the working memory to keep it safe
        del password
        
        print("Data successfully written to .nextclouddata file")

if __name__ == "__main__":
    FirstRunSetup.get_credentials()
