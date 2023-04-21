"""
send messages, receives messages, etc
"""

import sys
import logging

from .nextcloud_requests import NextcloudRequests
from .nextcloud_talk_extractor import NextcloudTalkExtractor
from .i18n import _


class NextcloudMessages:
    def __init__(self, base_url, username, password, room_token):
        """
        Initialize the NextcloudMessages class.

        :param base_url: The base URL of the Nextcloud server.
        :type base_url: str
        :param username: The username for the Nextcloud account.
        :type username: str
        :param password: The password for the Nextcloud account.
        :type password: str
        :param room_token: The room token for the Nextcloud Talk group.
        :type room_token: str
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.room_token = room_token
        self.nextcloud_requests = NextcloudRequests(
            self.base_url, self.password)
        self.nextcloud_talk_extractor = NextcloudTalkExtractor(
            self.base_url, self.username, self.password)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def send_message_to_nextcloud_talk_group(self, message):
        """
        Send a message to a Nextcloud Talk group.

        :param message: The message you want to send.
        :type message: str
        :return: None
        """
        data = {'actorDisplayName': "Guest", 'message': message}
        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{self.room_token}"
        self.nextcloud_requests.post_request(endpoint, json=data)
        print(f"{_('Message sent: ')}{message}")
        self.logger.info(
            f"Sent message '{message}' to room '{self.room_token}'")

    def receive_messages_of_nextcloud_talk_group(self, message_limit=1):
        """
        Receive messages of a Nextcloud Talk group.

        :param message_limit: The maximum number of messages to receive.
        :type message_limit: int, optional, default: 1
        :return: A dictionary with message ids as keys and tuples of actor and message as values.
        :rtype: dict
        """
        self.message_limit = message_limit

        paramsMessages = {
            "limit": self.message_limit,
            "lookIntoFuture": 0,
            "includeLastKnown": 1
        }

        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{self.room_token}"
        response = self.nextcloud_requests.send_request(
            endpoint, params=paramsMessages)
        messages_dict = {}
        for messages in (response["ocs"]["data"]):
            message = messages["message"]
            actor = messages["actorDisplayName"]
            id = messages["id"]
            messages_dict[id] = actor, message
        self.logger.info(
            f"Received messages from room '{self.room_token}' with limit {message_limit}")
        return messages_dict

    def delete_message_in_nextcloud_talk_group(self, message_id=None):
        """
        Delete a message in a Nextcloud Talk group.

        :param message_id: The id of the message to be deleted, None for user selection.
        :type message_id: int, optional, default: None
        :return: A string indicating the message has been deleted.
        :rtype: str
        """
        if message_id is None:
            last_messages_dict = NextcloudMessages.receive_messages_of_nextcloud_talk_group(
                self, message_limit=10)

            last_messages = [
                (i, f"{actor}: {message}") for i, (actor, message) in enumerate(
                    last_messages_dict.values())]
            for i, message in last_messages:
                print(f"{i}: {message}")

            selection = input(
                _("Please select a message from the list that you want to delete [0-9]: "))
            selection_index = int(selection)
            if selection_index < len(last_messages):
                selected_message = list(
                    last_messages_dict.values())[selection_index]
            else:
                print(_("Invalid selection."))
                sys.exit()
            selected_message = list(
                last_messages_dict.values())[selection_index]
            selected_actor = selected_message[0]
            print(
                f"{_('You have selected the following message: ')}{selected_message[1]}")
            print(f"created by: {selected_actor}")

            for message_id, message_tuple in last_messages_dict.items():
                if message_tuple == selected_message:
                    selected_message_id = message_id
                    break

            endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{self.room_token}/{selected_message_id}"
        else:
            endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{self.room_token}/{message_id}"

        self.nextcloud_requests.delete_request(endpoint)
        self.logger.info(
            f"Deleted message with id '{message_id}' in room '{self.room_token}'")
        return _("Message deleted")
