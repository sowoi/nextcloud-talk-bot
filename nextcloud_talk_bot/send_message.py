#/usr/bin/python3
import requests
from read_data import read_nextcloud_data
from headers import create_headers



data = read_nextcloud_data()

for key, value in data.items():
    locals()[key] = value


def send_message_to_nextcloud_talk_group(message):
    """
    Send a message to a Nextcloud Talk group.

    :param base_url: The base URL of your Nextcloud instance, e.g., https://your.nextcloud.com
    :param user: Your Nextcloud username
    :param password: Your Nextcloud password
    :param room_token: The token of the Talk group you want to send a message to
    :param message: The message you want to send
    """

    # Authenticate with the Nextcloud instance
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)

    # Send a message to the group
    headers = {'Content-Type': 'application/json'}
    data = {'actorDisplayName': "OkkoBot", DISPLAYNAME: message}
    response = session.post(f"{NEXTCLOUD_URL}/ocs/v2.php/apps/spreed/api/v1/chat/{ROOM}", json=data, headers=HEADERSNC)

    if response.status_code == 200 or response.status_code == 201:
        print(f"Message sent: {message}")
    else:
        print(f"Failed to send message. Response status code: {response.status_code}")
