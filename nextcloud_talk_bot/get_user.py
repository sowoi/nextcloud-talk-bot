import requests
import json
from read_data import read_nextcloud_data
from constants import HEADERSNC


data = read_nextcloud_data()

for key, value in data.items():
    locals()[key] = value
    print(value)


def get_user_data(NEXTCLOUD_URL, USERNAME, PASSWORD):
    # First, get an access token
    auth_url = NEXTCLOUD_URL + "/ocs/v2.php/cloud/user"
    response = requests.get(auth_url, headers=HEADERSNC, auth=(USERNAME, PASSWORD))
    print(response)
    return response.json()

if __name__ == "__main__":
    get_user_data(NEXTCLOUD_URL, USERNAME, PASSWORD)
