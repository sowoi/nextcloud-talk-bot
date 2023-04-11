import sys
from nextcloud_requests import NextcloudRequests
from nextcloud_talk_extractor import NextcloudTalkExtractor
from confirmation import are_you_sure

class NextcloudPoll:
    
    def __init__(self, base_url, username, password, room_name, question=None, voting_options=None, max_votes=None, result_mode=None, poll_id=None):
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
        conversation_list = self.nextcloud_talk_extractor.get_conversations_ids()
        if room_name not in conversation_list:
            return f"{room_name} does not exist"
        else:
            room_token = conversation_list[room_name]
            
        endpoint = f"/ocs/v2.php/apps/spreed/api/v1/poll/{room_token}/{poll_id}"
        print(endpoint)
        
        
        response = self.nextcloud_requests.send_request(endpoint)
        return(response)
        

            
    

    def close_poll(self, poll_id=0):
        conversation_list = self.nextcloud_talk_extractor.get_conversations_ids()
        if room_name not in conversation_list:
            return f"{room_name} does not exist"
        else:
            if not NextcloudPoll.get_poll_result(self, poll_id)["ocs"]["meta"]["statuscode"] == 200:
                return "PollId not found"
            else:
                poll_question = NextcloudPoll.get_poll_result(self, poll_id)["ocs"]["data"]["question"]
                if are_you_sure("close", poll_question):
                    room_token = conversation_list[room_name]
                    endpoint = endpoint = f"/ocs/v2.php/apps/spreed/api/v1/poll/{room_token}/{poll_id}"
                    self.nextcloud_requests.delete_request(endpoint)
    
                    print(f"Closed poll '{room_name}'")
                else:
                    print("Poll closing aborted.")
                    sys.exit()
