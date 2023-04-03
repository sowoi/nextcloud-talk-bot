import getpass
import requests
from cryptography.fernet import Fernet


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
    # Authenticate with the Nextcloud instance
    HEADERSNC = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'OCS-APIRequest': 'true',
    "Authorization": f"Bearer {password}"
    }
    session = requests.Session()
    session.auth = (username, password)

    # Send a message to the group
    headers = {'Content-Type': 'application/json'}
    data = {'actorDisplayName': "OkkoBot", 'message': "test"}
    response = session.post(f"{url}/ocs/v2.php/apps/spreed/api/v1/chat/{room}", json=data, headers=HEADERSNC)

    if response.status_code == 200 or response.status_code == 201:
        print(f"Message sent {response.status_code}")
        return True

    else:
        print(f"Failed to send message. Response status code: {response.status_code}")
        return False

def get_credentials():
    # Query the parameters one by one
    nextcloud_url = get_nextcloud_url()
    username = get_username()
    password = get_password()
    room = get_room()
    nc_remote_folder = get_nc_remote_folder()

    # Prüfung der Anmeldedaten mit Nextcloud API
    if not check_nextcloud_credentials(nextcloud_url, username, password, room):
        print("Fehlerhafte Anmeldedaten. Bitte versuchen Sie es erneut.")
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
