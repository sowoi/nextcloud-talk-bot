import requests
import json
from read_data import read_nextcloud_data

data = read_nextcloud_data()

for key, value in data.items():
    locals()[key] = value
    print(value)


HEADERSNC = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'OCS-APIRequest': 'true',
    "Authorization": f"Bearer {PASSWORD}"
}


def get_user_data(NEXTCLOUD_URL, USERNAME, PASSWORD):
    # First, get an access token
    auth_url = NEXTCLOUD_URL + "/ocs/v2.php/cloud/user?format=json"
    response = requests.get(auth_url, headers=HEADERSNC, auth=(USERNAME, PASSWORD))
    return response.json()
    #token = response.json()["ocs"]["data"]["token"]

if __name__ == "__main__":
    get_user_data(NEXTCLOUD_URL, "schlaueshauesle", "N5a4L-2YGKQ-BtHCx-2BL4T-HofR5")
