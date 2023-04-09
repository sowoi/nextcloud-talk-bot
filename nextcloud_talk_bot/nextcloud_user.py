from nextcloud_requests import NextcloudRequests

class NextcloudUser:
    """
    This class represents a Nextcloud User and provides functionality to fetch the user's data
    and test user login.
    """

    def __init__(self, base_url, user, password):
        """
        Initialize the NextcloudUser instance with Nextcloud credentials.

        :param base_url: The base URL of the Nextcloud server.
        :type base_url: str
        :param user: The username of the Nextcloud user.
        :type user: str
        :param password: The password of the Nextcloud user.
        :type password: str
        """
        self.base_url = base_url
        self.user = user
        self.password = password
        self.nextcloud_requests = NextcloudRequests(base_url, password)

    def test_user_login(self):
        """
        Test user login by attempting to retrieve user data from Nextcloud using the provided
        credentials.

        :return: A dictionary containing the user's data if the login is successful,
                 an error message otherwise.
        :rtype: dict
        """
        endpoint = "/ocs/v2.php/cloud/user"
        return self.nextcloud_requests.send_request(endpoint)

    def get_preferred_language(self):
        """
        Get the user's preferred language from the Nextcloud server.

        :return: The preferred language if the request is successful,
                 raises an exception otherwise.
        :rtype: str
        """
        endpoint = f"/ocs/v2.php/cloud/users/{self.user}"
        user_data = self.nextcloud_requests.send_request(endpoint)["ocs"]["data"]
        return user_data["language"]

    def get_quota(self):
        """
        Get the user's quota information from the Nextcloud server.

        :return: A dictionary containing the user's quota information if the request is successful,
                 raises an exception otherwise.
        :rtype: dict
        """
        endpoint = f"/ocs/v2.php/cloud/users/{self.user}"
        user_data = self.nextcloud_requests.send_request(endpoint)["ocs"]["data"]
        return user_data["quota"]
