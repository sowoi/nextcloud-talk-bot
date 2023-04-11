from .nextcloud_data import NextcloudData
from .nextcloud_requests import NextcloudRequests

class NextcloudMessages:
    @staticmethod
    def send_message_to_nextcloud_talk_group(message):
        """
        Send a message to a Nextcloud Talk group.

        Args:
            message (str): The message you want to send.

        Returns:
            None
        """
        # Send a message to the group   
        data = {'actorDisplayName': "OkkoBot", DISPLAYNAME: message}
        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{ROOM}"
        NextcloudRequests.post_request(endpoint,json=data)
        print(f"Message sent: {message}")