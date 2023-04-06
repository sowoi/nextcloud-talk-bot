#/usr/bin/python3
import argparse
import requests
from read_data import read_nextcloud_data
from headers import create_headers


class NextcloudTalkExtractor:
    """
    A class to interact with the Nextcloud Talk API and extract data.
    """

    def __init__(self, base_url, username, password, room_id=None, message_limit=None):
        """
        Initialize the NextcloudTalkExtractor class with the required credentials.

        :param base_url: The base URL for the Nextcloud server.
        :param username: The username for the Nextcloud user account.
        :param password: The password for the Nextcloud user account.
        :param room: The room token for the Nextcloud chat group.
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.room_id = room_id
        self.message_limit = message_limit


    def get_conversations_ids(self):
        """
        Get the list of conversations for the authenticated user.

        :return: A dictionary containing the list of conversation tokens and names.
        """
        HEADERSNC = create_headers(self.password)
        response = requests.get(f"{self.base_url}/ocs/v2.php/apps/spreed/api/v4/room", headers=HEADERSNC, auth=(self.username, self.password))
        response.raise_for_status()
        conversation_list = response.json()

        # Extract the conversation IDs
        conversation_ids = {}
        for room in conversation_list["ocs"]["data"]:
            conversation_token = room["token"]
            conversation_name = room["displayName"]
            conversation_ids[conversation_name] = conversation_token       
        return conversation_ids
    
    
    def get_participants(self, room_id, message_limit=None):
        """
        Get the list of participants in a specific conversation.

        :param room_id: The token of the conversation for which to retrieve participants.
        :return: A lists containing the list of participants.
        """
        response = requests.get(f"{self.base_url}/ocs/v2.php/apps/spreed/api/v4/room/{room_id}/participants", headers=HEADERSNC)
        response.raise_for_status()
        # Extract the participants IDs
        participant_names = []
        for participants in response.json()["ocs"]["data"]:
            participant_name = participants["displayName"]
            participant_names.append(participant_name)
        return participant_names
            
    def get_messages(self, room_id, message_limit=1):
        """
        Get the messages in a specific conversation, with an optional limit.

        :param room_id: The token of the conversation for which to retrieve messages.
        :param limit: The maximum number of messages to retrieve (default: 100).
        :return: A JSON object containing the list of messages.
        """
        response = requests.get(f"{self.base_url}/ocs/v2.php/apps/spreed/api/v1/chat/{room_id}", headers=HEADERSNC, params={"limit": message_limit, "lookIntoFuture":0})
        response.raise_for_status()
        # Extract the participants IDs
        messages_list = []
        for message in response.json()["ocs"]["data"]:
            messages = message["message"]
            messages_list.append(messages)
        return messages_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    args = parser.parse_args()
    data = read_nextcloud_data()
    for key, value in data.items():
        locals()[key] = value
    extractor = NextcloudTalkExtractor(NEXTCLOUD_URL, USERNAME, PASSWORD)
    participants = extractor.get_participants(room_id=ROOM)
    print(participants)
    messages = extractor.get_messages(room_id=ROOM, message_limit=5)
    print(messages)

 
