# Nextcloud Talk Bot: Messages

NextcloudMessages provides a set of methods to interact with a Nextcloud Talk group's chat. It uses the NextcloudRequests and NextcloudTalkExtractor classes to send and receive messages.

## Initialization

To create an instance of the NextcloudTalkExtractor class, you will need the following information:

- base_url: The base URL for the Nextcloud server.
- username: The username for the Nextcloud user account.
- password: The password for the Nextcloud user account.
- room_name: The name of the room where messages are handled.


## Usage

```
from nextcloud_talk_bot.nextcloud_messages import NextcloudMessages
# create instance
messages = NextcloudMessages(base_url="https://example.com/nextcloud", username="user", password="pass", room="myroom")
```
    
## Methods

1. send_message_to_nextcloud_talk_group(message_string)  
Sends a message to a Nextcloud Talk group.
2. receive_messages_of_nextcloud_talk_group(message_limit)
Retrieves the last message_limit messages from a Nextcloud Talk group or mthe last "message_limit" number of messages (default is 1)  
returns: mesage dictionary with message_id and actor
3. delete_message_in_nextcloud_talk_group(message_id)
Deletes a message from a Nextcloud Talk group if message_id is provided. If not: prompts the user to select a message from the last 10 messages.

## Examples

```python
# send message
messages.send_message_to_nextcloud_talk_group("Hello, everyone!")

# receive jlast 10 messages
messages_dict = messages.receive_messages_of_nextcloud_talk_group(message_limit=10)

# receives
# {
#  id_1: (actor_1, message_1),
#  id_2: (actor_2, message_2),
#  ...
#}


# delete message
messages.delete_message_in_nextcloud_talk_group(message_id=1234)

```