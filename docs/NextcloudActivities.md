# Nextcloud Talk Bot: Activities

This module provides the NextcloudActivities class for handling Nextcloud activities.


## Usage
```python

# Via Bot
from nextcloud_talk_bot.Nextcloudtalkbot import NextcloudTalkBot

#Initialize bot:
bot = NextcloudTalkBot()

# Via Module
from nextcloud_talk_bot.nextcloud_activities import NextcloudActivities

#Initialize the NextcloudActivities class:
nextcloud = NextcloudActivities(base_url, username, password)

#Get the last activities from Nextcloud:
last_activities = nextcloud.get_last_activities()

#Search for specific activities in the last activities:
filtered_activities = nextcloud.search_last_activities(activity)

```

## Methods

__init__(self, base_url, username, password, activity=None): Initializes the NextcloudActivities class.
get_last_activities(self): Gets the last activities from Nextcloud.
search_last_activities(self, activity): Searches for events, to-dos or file-operations in the given activities.


## Attributes

- base_url (str): The base URL of the Nextcloud instance.
- username (str): The username of the Nextcloud user.
- password (str): The password of the Nextcloud user.
- activity (str, optional): The activity to search for (e.g. to-do, event, shared, deleted, created, changed).


## Examples

```
    # Initialize the NextcloudActivities class
    nextcloud = NextcloudActivities('https://example.com/nextcloud', 'username', 'password')

    # Get the last activities from Nextcloud
    last_activities = nextcloud.get_last_activities()
    print(last_activities)

    # Search for to-do in latest activities
    activity = 'to-do'
    filtered_activities = nextcloud.search_last_activities(activity)
    print(filtered_activities)
```