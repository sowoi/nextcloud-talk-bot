import requests
from headers import create_headers

class NextcloudRequests:
    """
    This class provides functionality to send requests to the Nextcloud API.
    """

    def __init__(self, base_url, password):
        """
        Initialize the NextcloudRequests instance with the Nextcloud base URL and password.

        Args:
            base_url (str): The base URL of the Nextcloud server.
            password (str): The password of the Nextcloud user.
        """
        self.base_url = base_url
        self.password = password

    def send_request(self, endpoint, params=None):
        """
        Send a request to the Nextcloud API and return the response.

        Args:
            endpoint (str): The API endpoint to send the request to.
            params (dict, optional): A dictionary of query parameters to include in the request.

        Returns:
            dict: A dictionary containing the response data if the request is successful,
            raises an exception otherwise.
        """
        headers = create_headers(self.password)
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        print(response)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {url} {headers}, {params}")