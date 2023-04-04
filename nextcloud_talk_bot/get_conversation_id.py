import requests
import json
from read_data import read_nextcloud_data

data = read_nextcloud_data()

for key, value in data.items():
    locals()[key] = value

HEADERSNC = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'OCS-APIRequest': 'true',
    "Authorization": f"Bearer {PASSWORD}"
}





def extract_talk_conversation_ids(base_url, username, password):
    # Get an access token
    auth_url = base_url + "/ocs/v2.php/cloud/user?format=json"
    response = requests.get(auth_url, headers=HEADERSNC, auth=(username, password))
    
    # Get a list of all Talk conversations
    conversations_url = base_url + "/ocs/v2.php/apps/spreed/api/v4/room?format=json"
    headers = {"Authorization": f"Bearer {PASSWORD}"}
    response = requests.get(conversations_url, headers=headers)
    conversation_list = response.json()

    # Extract the conversation IDs
    conversation_ids = {}
    for room in conversation_list["ocs"]["data"]:
        conversation_token = room["token"]
        conversation_name = room["displayName"]
        conversation_ids[conversation_name] = conversation_token

    return conversation_ids

if __name__ == "__main__":
    extract_talk_conversation_ids(NEXTCLOUD_URL, USERNAME, PASSWORD)
