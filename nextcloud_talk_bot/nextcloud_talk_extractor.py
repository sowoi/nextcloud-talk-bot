"""
interact with the Nextcloud Talk API and extract data
"""
import argparse
from .nextcloud_data import NextcloudData
from .nextcloud_requests import NextcloudRequests
from .permissions_map import permissions_map
from .i18n import _


class NextcloudTalkExtractor:
    """
    A class to interact with the Nextcloud Talk API and extract data.
    """

    def __init__(
            self,
            base_url,
            username,
            password,
            room_id=None,
            message_limit=None):
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
        self.nextcloud_requests = NextcloudRequests(
            self.base_url, self.password)

    def get_conversations_ids(self):
        """
        Get the list of conversations for the authenticated user.

        :return: A dictionary containing the list of conversation tokens and names.
        """
        endpoint = "/ocs/v2.php/apps/spreed/api/v4/room"
        response = self.nextcloud_requests.send_request(endpoint)
        conversation_list = response
        # Extract the conversation IDs
        conversation_ids = {}
        for room in conversation_list["ocs"]["data"]:
            conversation_token = room["token"]
            conversation_name = room["displayName"]
            conversation_ids[conversation_name] = conversation_token
        return conversation_ids

    def get_participants(self, room_id):
        """
        Get the list of participants in a specific conversation.

        :param room_id: The token of the conversation for which to retrieve participants.
        :return: A lists containing the list of participants.
        """
        endpoint = f"/ocs/v2.php/apps/spreed/api/v4/room/{room_id}/participants"
        response = self.nextcloud_requests.send_request(endpoint)
        # Extract the participants IDs
        participant_names = []
        for participants in response["ocs"]["data"]:
            participant_name = participants["displayName"]
            participant_names.append(participant_name)
        return participant_names

    def get_user_permissions(self, room_id):
        """
        Get the permissions of all users in a Nextcloud Talk room.

        :param room_id: The ID of the Nextcloud Talk room.
        :type room_id: str

        :return: A dictionary containing user IDs as keys and their permissions as values.
        :rtype: dict

        :raises Exception: If there is an error with the API request.
        """
        endpoint = f"/ocs/v2.php/apps/spreed/api/v4/room/{room_id}/participants"
        response = self.nextcloud_requests.send_request(endpoint)
        all_users_permissions = {}
        for participant in response["ocs"]["data"]:
            user_id = participant["actorId"]
            user_permissions = participant["permissions"]
            allowed_actions = []

            for code, description in permissions_map.items():
                if user_permissions & code == code:
                    allowed_actions.append(description)

            all_users_permissions[user_id] = ", ".join(allowed_actions)

        return all_users_permissions

    def get_messages(self, room_id, message_limit=1):
        """
        Get the messages in a specific conversation, with an optional limit.

        :param room_id: The token of the conversation for which to retrieve messages.
        :param limit: The maximum number of messages to retrieve (default: 100).
        :return: A JSON object containing the list of messages.
        """
        self.message_limit = message_limit
        paramsMessages = {
            "limit": self.message_limit,
            "lookIntoFuture": 0
        }
        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{room_id}"
        response = self.nextcloud_requests.send_request(
            endpoint, params=paramsMessages)

        # Extract the participants IDs
        messages_list = []
        for message in response["ocs"]["data"]:
            messages = message["message"]
            messages_list.append(messages)
        return messages_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    args = parser.parse_args()
    data = NextcloudData.read_nextcloud_data()
    for key, value in data.items():
        locals()[key] = value
    extractor = NextcloudTalkExtractor(NEXTCLOUD_URL, USERNAME, PASSWORD)
    participants = extractor.get_user_permissions(ROOM)
    print(participants)
