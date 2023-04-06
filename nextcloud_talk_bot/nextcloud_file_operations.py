import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth
from read_data import read_nextcloud_data
from constants import HEADERSNC

data = read_nextcloud_data()

for key, value in data.items():
    locals()[key] = value


class NextcloudFileOperations:
    """
    A class to interact with the Nextcloud Talk API and extract data.
    """

    def __init__(self, base_url, username, password, folder_path):
        """
        Initialize the NextcloudTalkExtractor class with the required credentials.

        :param base_url: The base URL for the Nextcloud server.
        :param username: The username for the Nextcloud user account.
        :param password: The password for the Nextcloud user account.
        :param folder_path: The path of the folder of the use.
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.folder_path = folder_path
        

    def list_files_in_nextcloud_folder(self):
        """
        List all files in a Nextcloud folder.

        Args:
            base_url (str): The base URL of your Nextcloud instance.
            username (str): Your Nextcloud username.
            password (str): Your Nextcloud password.
            folder_path (str): The path of the folder to list files in.

        Returns:
            list: A list of file names in the specified folder.
        """
   
        # Define the WebDAV URL for the folder
        webdav_url = f"{self.base_url}/remote.php/dav/files/{self.username}/{self.folder_path}"

        # Send a PROPFIND request to the WebDAV URL
        headers = {"Depth": "1"}
        response = requests.request("PROPFIND", webdav_url, headers=headers, auth=HTTPBasicAuth(self.username, self.password))

        # Check if the request was successful
        if response.status_code != 207:
            print(f"Error: {response.status_code}")
            return None

        # Parse the XML response
        from xml.etree import ElementTree
        root = ElementTree.fromstring(response.content)

        # Extract the file names from the response
        file_names = []
        for response_element in root.findall("{DAV:}response"):
            href_element = response_element.find("{DAV:}href")
            if href_element is not None:
                file_name = href_element.text.split("/")[-1]
                if file_name:
                    file_names.append(file_name)

        return file_names
