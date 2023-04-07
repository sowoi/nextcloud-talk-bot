# Nextcloud Talk Bot: Extractor

The NextcloudTalkExtractor class is a utility for interacting with the Nextcloud Talk API and extracting data. 
It provides methods for fetching conversations, participants, and messages for an authenticated user.

## Initialization:
To create an instance of the NextcloudTalkExtractor class, you will need the following information:

- base_url: The base URL for the Nextcloud server.
- username: The username for the Nextcloud user account.
- password: The password for the Nextcloud user account.
- room_id (optional): The room token for the Nextcloud chat group.
- message_limit (optional): The default maximum number of messages to retrieve.

## Methods:

1. get_conversations_ids()
    Purpose: Fetch the list of conversations for the authenticated user.
    Returns: A dictionary containing the list of conversation tokens and names.

2. get_participants(room_id, message_limit=None)
    Purpose: Fetch the list of participants in a specific conversation.
    Parameters:
        - room_id: The token of the conversation for which to retrieve participants.
    Returns: A list containing the participant display names.

3. get_messages(room_id, message_limit=1)
    Purpose: Fetch the messages in a specific conversation, with an optional limit.
    Parameters:
        - room_id: The token of the conversation for which to retrieve messages.
        - message_limit: The maximum number of messages to retrieve (default: 100).
    Returns: A list containing the messages as strings.

## Example Usage:

    from nextcloud_talk_extractor import NextcloudTalkExtractor

    base_url = "https://my.nextcloud.com"
    username = "my_username"
    password = "my_password"

    extractor = NextcloudTalkExtractor(base_url, username, password)

    # Get the list of conversations
    conversations = extractor.get_conversations_ids()
    print(conversations)

    # Get the participants of a specific conversation
    room_id = "conversation_token"
    participants = extractor.get_participants(room_id)
    print(participants)

    # Get the messages of a specific conversation
    messages = extractor.get_messages(room_id, message_limit=100)
    print(messages)