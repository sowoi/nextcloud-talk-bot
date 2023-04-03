import requests
import xml.etree.ElementTree as ET


HEADERSNC = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'OCS-APIRequest': 'true',
    "Authorization": f"Bearer {PASSWORD}"
} 

FILES = None


def list_files_in_directory():
    # WebDAV API-URL
    webdav_url = f"{NEXTCLOUD_URL}/remote.php/dav/files/{USERNAME}/{NC_FOLDER}"
    headers = {
        "OCS-APIRequest": "true",
        "Accept": "application/xml",
    }

    response = requests.request("PROPFIND", webdav_url, headers=headers, auth=(USERNAME, PASSWORD))

    # XML-Antwort parsen
    tree = ET.fromstring(response.content)

    print(tree)
    
    # Dateien und Verzeichnisse auflisten
    files = []
    for elem in tree.findall(".//{DAV:}href"):
        path = elem.text.split('/')[-1]
        if path != "":
            files.append(path)
    

    print("Listed files: " , files)

