#/usr/bin/python3
import requests
from read_data import read_nextcloud_data
from headers import create_headers

class NextcloudUser:
    """
    This class represents a Nextcloud User and provides functionality to fetch the user's data
    and test user login.
    """

    def __init__(self, base_url, user, password):
        """
        Initialize the NextcloudUser instance with Nextcloud credentials.

        Args:
            base_url (str): The base URL of the Nextcloud server.
            user (str): The username of the Nextcloud user.
            password (str): The password of the Nextcloud user.
        """
        self.base_url = base_url
        self.user = user
        self.password = password
        
    def test_user_login(self):
        """
        Test user login by attempting to retrieve user data from Nextcloud using the provided
        credentials.

        Returns:
            dict: A dictionary containing the user's data if the login is successful,
            an error message otherwise.
        """
        HEADERSNC = create_headers(self.password)
        auth_url = self.base_url + "/ocs/v2.php/cloud/user"
        response = requests.get(auth_url, headers=HEADERSNC, auth=(self.user, self.password))
        return response.json()
