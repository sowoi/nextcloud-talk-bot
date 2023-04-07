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

    def _send_request(self, endpoint):
        """
        Send a request to the Nextcloud API and return the response.

        Args:
            endpoint (str): The API endpoint to send the request to.

        Returns:
            dict: A dictionary containing the response data if the request is successful,
            raises an exception otherwise.
        """
        headers = create_headers(self.password)
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}")

    def test_user_login(self):
        """
        Test user login by attempting to retrieve user data from Nextcloud using the provided
        credentials.

        Returns:
            dict: A dictionary containing the user's data if the login is successful,
            an error message otherwise.
        """
        endpoint = "/ocs/v2.php/cloud/user"
        return self._send_request(endpoint)

    def get_preferred_language(self):
        """
        Get the user's preferred language from the Nextcloud server.

        Returns:
            str: The preferred language if the request is successful,
            raises an exception otherwise.
        """
        endpoint = f"/ocs/v2.php/cloud/users/{self.user}"
        user_data = self._send_request(endpoint)["ocs"]["data"]
        return user_data["language"]

    def get_quota(self):
        """
        Get the user's quota information from the Nextcloud server.

        Returns:
            dict: A dictionary containing the user's quota information if the request is successful,
            raises an exception otherwise.
        """
        endpoint = f"/ocs/v2.php/cloud/users/{self.user}"
        user_data = self._send_request(endpoint)["ocs"]["data"]
        return user_data["quota"]