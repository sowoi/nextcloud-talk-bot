import requests
from headers import create_headers

class NextcloudRequests:
    """
    This class provides functionality to send requests to the Nextcloud API.
    
    :param base_url: The base URL of the Nextcloud instance.
    :param password: The password for the Nextcloud account.
    """
    def __init__(self, base_url, password):
        self.base_url = base_url
        self.password = password

    def send_request(self, endpoint, params=None):
        
        """
        Send a GET request to the specified Nextcloud API endpoint.
        
        :param endpoint: The API endpoint to send the request to.
        :param params: Optional dictionary of query parameters to include in the request. Default is None.
        :return: The JSON response from the server.
        :raises Exception: If the response status code is not 200.
        """
        headers = create_headers(self.password)
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {url} {headers}, {params}")
        
    def post_request(self, endpoint, json=None):
        """
        Send a POST request to the specified Nextcloud API endpoint.
        
        :param endpoint: The API endpoint to send the request to.
        :param json: Optional dictionary containing the JSON payload to include in the request. Default is None.
        :return: The JSON response from the server.
        :raises Exception: If the response status code is not 200 or 201.
        """
       
        headers = create_headers(self.password)

        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=headers, json=json)

        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}, {url} {headers}, {json}")
        
    def delete_request(self, endpoint):
        headers = create_headers(self.password)
        url = f"{self.base_url}{endpoint}"
        
        response = requests.delete(url, headers=headers)
        

