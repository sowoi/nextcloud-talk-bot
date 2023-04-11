import sys
from nextcloud_requests import NextcloudRequests
from nextcloud_talk_extractor import NextcloudTalkExtractor
from confirmation import are_you_sure


class NextcloudMeeting:
    """
    A class to create a meeting room using the Nextcloud Talk API.
    
    :param base_url: The base URL of the Nextcloud instance.
    :param user: The username for the Nextcloud account.
    :param password: The password for the Nextcloud account.
    """
    
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.nextcloud_requests = NextcloudRequests(base_url, password)
        self.nextcloud_talk_extractor = NextcloudTalkExtractor(base_url, username, password)


    def create_room(self, room_name):
        """
        Create a new meeting room.

        :param room_name: The name of the meeting room to create.
        :return: The room ID of the created meeting room or an error message.
        """
        
        conversation_list = self.nextcloud_talk_extractor.get_conversations_ids()
        for room in conversation_list.keys():
            conversation_name = room
            if conversation_name == room_name:
                return f"{room_name} already exists"
        
        endpoint = "/ocs/v2.php/apps/spreed/api/v4/room"

        payload = {"roomType": 2, "invite": "", "source": "conversation", "roomName": room_name}
        response = self.nextcloud_requests.post_request(endpoint, json=payload)

        room_id = response["ocs"]["data"]["token"]
        room_name = response["ocs"]["data"]["displayName"]
        if room_id:
           return f"{room_name} successfull created"
        else:
           return f"Error: Could not create {room_name}"


    def delete_room(self, room_name):
        """
        Delete a room in the Nextcloud Talk instance by its name, after asking for confirmation.
        
        :param room_name: The name of the room to be deleted.
        :return: A message indicating the room does not exist, or None if the room is successfully deleted.
        """
        
        conversation_list = self.nextcloud_talk_extractor.get_conversations_ids()
        if room_name not in conversation_list:
            return f"{room_name} does not exist"
        else:
            if are_you_sure("delete", room_name):
                delete_room = conversation_list[room_name]    
                endpoint = f"/ocs/v2.php/apps/spreed/api/v4/room/{delete_room}"
                self.nextcloud_requests.delete_request(endpoint)
                print(f"Deleted {room_name}")
            else:
                print("Aborted.")
                sys.exit()

