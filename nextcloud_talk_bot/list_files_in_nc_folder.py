import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth
from read_data import read_nextcloud_data
from constants import HEADERSNC


data = read_nextcloud_data()

for key, value in data.items():
    locals()[key] = value
    print(key, value)

FILES = None


def list_files_in_nextcloud_folder(base_url, username, password, folder_path):
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
    webdav_url = f"{base_url}/remote.php/dav/files/{username}{folder_path}"

    # Send a PROPFIND request to the WebDAV URL
    headers = {"Depth": "1"}
    response = requests.request("PROPFIND", webdav_url, headers=headers, auth=HTTPBasicAuth(username, password))
    print(response.text)

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

if __name__ == "__main__":
    NEXTCLOUD_URL = "https://ok.fahmed.de"
    USERNAME = "okko"
    PASSWORD = "bYdqH-Fq8aa-2rMYa-mzfsi-9rgEr"
    FOLDER_PATH = "/Code"
    file_list = list_files_in_nextcloud_folder(NEXTCLOUD_URL, USERNAME, PASSWORD, "Code")