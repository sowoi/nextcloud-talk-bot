import sys

from .nextcloud_requests import NextcloudRequests
from .nextcloud_talk_extractor import NextcloudTalkExtractor


class NextcloudMessages:
    def __init__(self, base_url, username, password, room):

        self.base_url = base_url
        self.username = username
        self.password = password
        self.room = room
        self.nextcloud_requests = NextcloudRequests(base_url, password)
        self.nextcloud_talk_extractor = NextcloudTalkExtractor(
            base_url, username, password)

    def send_message_to_nextcloud_talk_group(self, message):
        """
        Send a message to a Nextcloud Talk group.

        Args:
            message (str): The message you want to send.

        Returns:
            None
        """
        data = {'actorDisplayName': "Guest", 'message': message}
        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{self.room}"
        self.nextcloud_requests.post_request(endpoint, json=data)
        print(f"Message sent: {message}")

    def receive_messages_of_nextcloud_talk_group(self, message_limit=1):
        self.message_limit = message_limit

        paramsMessages = {
            "limit": self.message_limit,
            "lookIntoFuture": 0,
            "includeLastKnown": 1
        }

        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{self.room}"
        response = self.nextcloud_requests.send_request(
            endpoint, params=paramsMessages)
        messages_dict = {}
        for messages in (response["ocs"]["data"]):
            message = messages["message"]
            actor = messages["actorDisplayName"]
            id = messages["id"]
            messages_dict[id] = actor, message
        return messages_dict

    def delete_message_in_nextcloud_talk_group(self, message_id=None):

        if message_id is None:
            last_messages_dict = NextcloudMessages.receive_messages_of_nextcloud_talk_group(
                self, message_limit=10)

            last_messages = [
                (i, f"{actor}: {message}") for i, (actor, message) in enumerate(
                    last_messages_dict.values())]
            for i, message in last_messages:
                print(f"{i}: {message}")

            selection = input(
                "Please select a message from the list that you want to delete [0-9]: ")
            selection_index = int(selection)
            if selection_index < len(last_messages):
                selected_message = list(
                    last_messages_dict.values())[selection_index]
            else:
                print("Invalid selection.")
                sys.exit()
            selected_message = list(
                last_messages_dict.values())[selection_index]
            selected_actor = selected_message[0]
            print(
                f"You have selected the following message:: {selected_message[1]}")
            print(f"created by: {selected_actor}")

            for message_id, message_tuple in last_messages_dict.items():
                if message_tuple == selected_message:
                    selected_message_id = message_id
                    break

            endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{self.room}/{selected_message_id}"
        else:
            endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{self.room}/{message_id}"

        self.nextcloud_requests.delete_request(endpoint)
        return "Message deleted"
