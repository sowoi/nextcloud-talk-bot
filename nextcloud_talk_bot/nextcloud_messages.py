from .nextcloud_requests import NextcloudRequests
from .nextcloud_talk_extractor import NextcloudTalkExtractor

class NextcloudMessages:
    def __init__(self, base_url, username, password, room):
        
        self.base_url = base_url
        self.username = username
        self.password = password
        self.room = room
        self.nextcloud_requests = NextcloudRequests(base_url, password)
        self.nextcloud_talk_extractor = NextcloudTalkExtractor(base_url, username, password)


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
        
    def mark_chat_nextcloud_talk_group(self, mark=read):
        
        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{self.room}/read"


    
    def delete_message_in_nextcloud_talk_group(self, message):
        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{self.room}"
        

if __name__ ==  'main':
     def send_message_to_nextcloud_talk_group(self, message)