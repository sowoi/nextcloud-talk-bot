import sys

from .nextcloud_requests import NextcloudRequests
from .nextcloud_talk_extractor import NextcloudTalkExtractor


class NextcloudMessages:
    def __init__(self, base_url, username, password, room):
        """
        Initializes a new instance of the NextcloudMessages class.

        :param base_url: The base URL of the Nextcloud instance.
        :param username: The username for the Nextcloud account.
        :param password: The password for the Nextcloud account.
        :param room: The name or ID of the Nextcloud Talk group.
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.room = room
        self.nextcloud_requests = NextcloudRequests(base_url, password)
        self.nextcloud_talk_extractor = NextcloudTalkExtractor(base_url, username, password)

    def send_message_to_nextcloud_talk_group(self, message):
        """
        Sends a message to a Nextcloud Talk group.

        :param message: The message to send.
        :type message: str
        :return: None
        """
        data = {'actorDisplayName': "Guest", 'message': message}
        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{self.room}"
        self.nextcloud_requests.post_request(endpoint, json=data)
        print(f"Message sent: {message}")

    def receive_messages_of_nextcloud_talk_group(self, message_limit=1):
        """
        Retrieves the last `message_limit` messages from a Nextcloud Talk group.

        :param message_limit: The maximum number of messages to retrieve.
        :type message_limit: int
        :return: A dictionary of message IDs mapped to tuples of (actor, message).
        :rtype: dict
        """
        self.message_limit = message_limit

        paramsMessages = {
            "limit": self.message_limit,
            "lookIntoFuture": 0,
            "includeLastKnown": 1
        }

        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{self.room}"
        response = self.nextcloud_requests.send_request(endpoint, params=paramsMessages)
        messages_dict = {}
        for messages in (response["ocs"]["data"]):
            message = messages["message"]
            actor = messages["actorDisplayName"]
            id = messages["id"]
            messages_dict[id] = actor, message
        return messages_dict

    def delete_message_in_nextcloud_talk_group(self, message_id=None):
        """
        Deletes a message from a Nextcloud Talk group.

        :param message_id: The ID of the message to delete. If None, prompts the user to select a message from the last 10 messages.
        :type message_id: int or None
        :return: A message indicating whether the operation was successful.
        :rtype: str
        """
        if message_id is None:
            last_messages_dict = self.receive_messages_of_nextcloud_talk_group(message_limit=10)

            last_messages = [(i, f"{actor}: {message}") for i, (actor, message) in enumerate(last_messages_dict.values())]
            for i, message in last_messages:
                print(f"{i}: {message}")

            selection = input("Please select a message from the list that you want to delete [0-9]: ")
            selection_index = int(selection)
            if selection_index < len(last_messages):
                selected_message = list(last_messages_dict.values())[selection_index]
            else:
                print("Invalid selection.")
                sys.exit()
            selected_message = list(last_messages_dict.values())[selection
