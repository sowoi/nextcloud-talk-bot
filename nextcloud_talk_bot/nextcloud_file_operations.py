#/usr/bin/python3

import requests
import os
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

    def __init__(self, base_url, username, password, nc_remote_folder=None, local_folder=None, remote_file=None):
        """
        Initialize the NextcloudTalkExtractor class with the required credentials.

        :param base_url: The base URL for the Nextcloud server.
        :param username: The username for the Nextcloud user account.
        :param password: The password for the Nextcloud user account.
        :param nc_remote_folder: The path of the folder of the use.
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.nc_remote_folder = nc_remote_folder
        self.local_folder = local_folder
        self.remote_file = remote_file
        

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
        webdav_url = f"{self.base_url}/remote.php/dav/files/{self.username}/{self.nc_remote_folder}"

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


    def send_local_file_to_nextcloud_folder(self):
        """
        Upload local files to a specified Nextcloud folder.

        This method iterates through all the files in the local folder, uploads each file to the specified
        Nextcloud folder, and deletes the local file upon successful upload.
        """
        for filename in os.listdir(self.local_folder):
            print("Sending file to Nextcloud Talk")
            for filename in os.listdir(self.local_folder):
                    # Create file path
                    file_path = os.path.join(self.local_folder, filename)

                    # Send file to Nextcloud Talk Room
                    with open(file_path, "rb") as file:
                        content_type = mimetypes.guess_type(file_path)[0]
                        headers = HEADERSNC.copy()
                        headers["Content-Type"] = content_type
                    
                        url = f"{self.base_url}/remote.php/dav/files/{self.username}/{self.nc_remote_folder}/{filename}"

                        try:
                            print("Sending ", filename)
                            response = requests.put(url, headers=HEADERSNC, data=file)
                            response.raise_for_status()
                            # If success delete the local file
                            if response.status_code == 201:
                                print("Send successfull")
                                os.remove(file_path)
                        except requests.exceptions.HTTPError as e:
                            print(f"Error sending the file {filename}: {e}")


    def delete_remote_file_in_nextcloud(self):
        """
        Delete a remote file in the specified Nextcloud folder.

        This method sends a DELETE request to the Nextcloud server to remove the remote file
        located in the user's specified folder.
        """        
        delete_url = f"{self.base_url}/remote.php/dav/files/{self.username}/{self.nc_remote_folder}/{self.remote_file}"
        requests.delete(delete_url, auth=(self.username, self.password))
        print(f"deleted: {self.remote_file} in {self.nc_remote_folder}")
           