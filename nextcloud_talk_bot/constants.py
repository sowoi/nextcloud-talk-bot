#/usr/bin/python3
from read_data import read_nextcloud_data

data = read_nextcloud_data()
PASSWORD = data['PASSWORD']

HEADERSNC = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'OCS-APIRequest': 'true',
    'Authorization': f"Bearer {PASSWORD}",
    'Accept-Language': 'en'
}