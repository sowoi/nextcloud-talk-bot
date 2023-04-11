from cryptography.fernet import Fernet
import os

class NextcloudData:
    @staticmethod
    def read_nextcloud_data():
        """
        Helper script.
        Reads Nextcloud configuration data from a file, decrypts the password, and returns the data as a dictionary.
        
        This function reads the Nextcloud configuration data from the '.nextclouddata' file, decrypts the password
        stored in the '.password' file using a key from the '.decode' file, and returns the data as a dictionary.
        
        Returns:
            data (dict): A dictionary containing the Nextcloud configuration data, including the decrypted password.
        """
        current_directory = os.path.dirname(os.path.realpath(__file__))
        nextclouddata_file_path = os.path.join(current_directory,".nextclouddata")
        password_file_path = os.path.join(current_directory,".password")
        decode_file_path = os.path.join(current_directory,".decode")

        # Check if the .nextclouddata file exists
        if not os.path.exists(nextclouddata_file_path):
            print("The .nextclouddata file does not exist. Please run the first_run_setup script first.")
            return

        # Read the .nextclouddata file and extract the data
        data = {}
        with open(nextclouddata_file_path, "r") as data_file:
            for line in data_file:
                key, value = line.strip().split("::")
                data[key] = value
                
        with open(decode_file_path, "r") as decode_file:
            decode_password = decode_file.readline()
            f = Fernet(decode_password)


        # Password decryption
        with open(password_file_path, "r") as password_file:
            encrypted_password = password_file.readline()
            decrypted_password = f.decrypt(encrypted_password).decode()
            data['PASSWORD'] = decrypted_password
            
        return data

if __name__ == "__main__":
    NextcloudData.read_nextcloud_data()
