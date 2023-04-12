# Nextcloud Talk Bot: Meeting

NextcloudMeeting can be used to create and delete meeting rooms using the Nextcloud Talk API. 

## Initialization

To create an instance of the NextcloudTalkExtractor class, you will need the following information:

- base_url: The base URL for the Nextcloud server.
- username: The username for the Nextcloud user account.
- password: The password for the Nextcloud user account.


## Usage

```
from nextcloud_talk_bot.nextcloud_meeting import NextcloudMeeting
# create instance
ncm = NextcloudMeeting(base_url="https://example.com", username="user", password="password")
```
    
## Methods

1. create_room(room_name)  
This method creates a new meeting room with the specified name. If the room already exists, the method will return an error message. If the room is successfully created, the method will return a success message.  

2. delete_room(room_name)  
This method deletes a meeting room with the specified name, after asking for confirmation. If the room does not exist, the method will return an error message. If the room is successfully deleted, the method will print a success message.


## Examples

```python
# create room
ncm.create_room(room_name="My Meeting Room")

# delete room
ncm.delete_room(room_name="My Meeting Room")
```