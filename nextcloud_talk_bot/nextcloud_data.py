from cryptography.fernet import Fernet
import os
import logging
from .i18n import _


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
        home_dir = os.path.expanduser("~")
        nextclouddata_file_path = os.path.join(home_dir, ".nextclouddata")
        password_file_path = os.path.join(home_dir, ".password")
        decode_file_path = os.path.join(home_dir, ".decode")

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Check if the .nextclouddata file exists
        if not os.path.exists(nextclouddata_file_path):
            print(
                _("The .nextclouddata file does not exist. Please run the first_run_setup script first."))
            logger.error(
                "The .nextclouddata file does not exist. Please run the first_run_setup script first.")
            return None

        # Read the .nextclouddata file and extract the data
        data = {}
        with open(nextclouddata_file_path, "r") as data_file:
            for line in data_file:
                key, value = line.strip().split("::")
                data[key] = value

        ncdecode_env = os.environ.get('NCDECODE')
        if ncdecode_env is not None:
            f = Fernet(ncdecode_env)
        else:
            with open(decode_file_path, "r") as decode_file:
                decode_password = decode_file.readline()
                f = Fernet(decode_password)

        # Password decryption
        ncpassword_env = os.environ.get('NCPASSWORD')
        if ncpassword_env is not None:
            data['PASSWORD'] = ncpassword_env
        else:
            with open(password_file_path, "r") as password_file:
                encrypted_password = password_file.readline()
                decrypted_password = f.decrypt(encrypted_password).decode()
                data['PASSWORD'] = decrypted_password
        logger.info("Successfully read and decrypted Nextcloud data")
        return data


if __name__ == "__main__":
    NextcloudData.read_nextcloud_data()
