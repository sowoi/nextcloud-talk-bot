from cryptography.fernet import Fernet
import os

def read_nextcloud_data():
    """
    Helper Script.
    Reads Nextcloud configuration data from a file, decrypts the password, and returns the data as a dictionary.
    
    This function reads the Nextcloud configuration data from the '.nextclouddata' file, decrypts the password
    stored in the '.password' file using a key from the '.decode' file, and returns the data as a dictionary.
    
    Returns:
        data (dict): A dictionary containing the Nextcloud configuration data, including the decrypted password.
    """
    # Check if the .nextclouddata file exists
    if not os.path.exists(".nextclouddata"):
        print("The .nextclouddata file does not exist. Please run the first_run_setup script first.")
        return

    # Read the .nextclouddata file and extract the data
    data = {}
    with open(".nextclouddata", "r") as data_file:
        for line in data_file:
            key, value = line.strip().split("::")
            data[key] = value

            
    with open(".decode", "r") as decode_file:
        decode_password = decode_file.readline()
        f = Fernet(decode_password)


    # Password decryption
    with open(".password", "r") as password_file:
        encrypted_password = password_file.readline()
        decrypted_password = f.decrypt(encrypted_password).decode()
        data['PASSWORD'] = decrypted_password

    return data
