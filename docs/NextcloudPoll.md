# Nextcloud Talk Bot: Poll

NextcloudPoll  can be used to create, get, and close polls in a Nextcloud Talk room. 

## Initialization

To create an instance of the NextcloudTalkExtractor class, you will need the following information:

- base_url: The base URL for the Nextcloud server.
- username: The username for the Nextcloud user account.
- password: The password for the Nextcloud user account.
- room_name: The name of the room where the poll will be created.
- question: The question for the poll.
- voting_options: A list of strings representing the options for the poll.
- max_votes: The maximum number of votes per user (default is 1).
- result_mode: The result mode of the poll (0 = show after vote, 1 = show always).
- poll_id: The ID of an existing poll to get or close.


## Usage

```
from nextcloud_talk_bot.nextcloud_poll import NextcloudPoll
# create instance
poll = NextcloudPoll(base_url="https://example.com", username="user", password="password", room_name="My Room", question="Do you like pizza?", voting_options=["Yes", "No"])
```
    
## Methods

1. create_poll(question, voting_options, max_votes, result_mode)  
This method creates a new poll with the specified question and options in the specified Nextcloud Talk room.  
2. get_poll_result(poll_id)
This method gets the result of a specific poll in the specified Nextcloud Talk room.
3. close_poll(poll_id)
This method closes a specific poll in the specified Nextcloud Talk room after asking for confirmation.

## Examples

```python
# create poll
poll.create_poll(question="Do you like pizza?", voting_options=["Yes", "No"])

# get poll result
poll.get_poll_result(poll_id=0)

# close poll
poll.close_poll(poll_id=0)
```