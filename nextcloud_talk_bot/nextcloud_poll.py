import sys
from .nextcloud_requests import NextcloudRequests
from .nextcloud_talk_extractor import NextcloudTalkExtractor
from .confirmation import are_you_sure

class NextcloudPoll:
    """
    This class provides methods to create, get, and close polls in a Nextcloud Talk room.

    :param base_url: The base URL of your Nextcloud instance, e.g., https://your.nextcloud.com.
    :param username: Your Nextcloud username.
    :param password: Your Nextcloud password.
    :param room_name: The name of the room where you want to create the poll.
    :param question: The question for the poll.
    :param voting_options: A list of strings representing the options for the poll.
    :param max_votes: The maximum number of votes per user (default is 1).
    :param result_mode: The result mode of the poll (0 = show after vote, 1 = show always).
    :param poll_id: The ID of an existing poll to get or close.
    """

    def __init__(self, base_url, username, password, room_name, question=None, voting_options=None, max_votes=1, result_mode=0, poll_id=None):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.room_name = room_name
        self.question = question
        self.voting_options = voting_options
        self.result_mode = result_mode
        self.max_votes = max_votes
        self.poll_id = poll_id
        self.nextcloud_requests = NextcloudRequests(base_url, password)
        self.nextcloud_talk_extractor = NextcloudTalkExtractor(base_url, username, password)


    def create_poll(self, question=None, voting_options=None, max_votes=1, result_mode=0):
        """
        Create a new poll in the specified Nextcloud Talk room.

        :param question: The question for the poll.
        :param voting_options: A list of strings representing the options for the poll.
        :param max_votes: The maximum number of votes per user (default is 1).
        :param result_mode: The result mode of the poll (0 = show after vote, 1 = show always).
        """

        conversation_list = self.nextcloud_talk_extractor.get_conversations_ids()
        if room_name not in conversation_list:
            return f"{room_name} does not exist"
        else:
            room_token = conversation_list[room_name]
            
        # Set the poll data
        poll_data = {
            "question": f"{question}",
            "options": voting_options,
            "resultMode": f"{result_mode}",
            "maxVotes": f"{max_votes}"
        }

        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/poll/{room_token}"

        self.nextcloud_requests.post_request(endpoint, json=poll_data)
    
    
    def get_poll_result(self, poll_id=0):
        """
        Get the result of a specific poll in the specified Nextcloud Talk room.

        :param poll_id: The ID of the poll to get.
        """
        conversation_list = self.nextcloud_talk_extractor.get_conversations_ids()
        if room_name not in conversation_list:
            return f"{room_name} does not exist"
        else:
            room_token = conversation_list[room_name]
            
        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/poll/{room_token}/{poll_id}"
        print(endpoint)
        
        
        response = self.nextcloud_requests.send_request(endpoint)
        return
