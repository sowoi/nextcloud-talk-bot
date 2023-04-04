import getpass
import requests
import json
from cryptography.fernet import Fernet
from get_user import get_user_data
from get_conversation_id import extract_talk_conversation_ids

def encrypt_password(password):
    # encrypt the password
    key = Fernet.generate_key()
    print(key)
    f = Fernet(key)
    print(f)
    encrypted_password = f.encrypt(password.encode())
    print(encrypted_password)
    
    # Store the encrypted text and the key in different files
    with open(".password", "wb") as password_file:
        password_file.write(encrypted_password)
    
    with open(".decode", "wb") as decode_file:
        decode_file.write(key)    
    return key

def get_nextcloud_url():
    nextcloud_url = input("Nextcloud-URL: ")
    return nextcloud_url

def get_username():
    username = input("Username: ")
    return username

def get_password():
    password = getpass.getpass("Password: ")
    return password

def get_room():
    room = input("Room: ")
    return room

def get_nc_remote_folder():
    nc_remote_folder = input("Nextcloud folder for file uploads: ")
    return nc_remote_folder

def check_nextcloud_credentials(url, username, password, room):
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
        roomSelection = select_nextcloud_talk_room(conversation_ids) 
        for i, rooms in enumerate(conversation_ids):
            if i == roomSelection - 1:
                 selectedRoom = rooms
        room = conversation_ids[selectedRoom]

        return True



def select_nextcloud_talk_room(conversation_ids):
    while True:
        try:
            roomSelection = int(input("Bitte geben Sie die Nummer des Listenelements ein, das Sie auswählen möchten: "))
            if roomSelection < 1 or roomSelection > len(conversation_ids):
                raise ValueError
            break
        except ValueError:
            print("Ungültige Eingabe. Bitte geben Sie eine Zahl zwischen 1 und", len(conversation_ids), "ein.")
    return roomSelection

def get_credentials():
    # Query the parameters one by one
    nextcloud_url = get_nextcloud_url()
    username = get_username()
    password = get_password()
    room = get_room()
    nc_remote_folder = get_nc_remote_folder()

    # Verification of credentials with Nextcloud API
    if not check_nextcloud_credentials(nextcloud_url, username, password, room):
        print("Incorrect login data. Please try again.")
        return
    
    # Encryption of the password and storage of the key
    encrypt_password(password)

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
    get_credentials()
