# Nextcloud Talk Bot: Search

NextcloudSearch provides methods for searching Nextcloud using the Nextcloud Search API. It is designed to be used in conjunction with a Nextcloud instance, and requires authentication credentials to access the API.

## Initialization

To create an instance of the NextcloudSarch class, you will need the following information:

- base_url: The base URL for the Nextcloud server.
- username: The username for the Nextcloud user account.
- password: The password for the Nextcloud user account.


## Usage

```
# Via Bot
from nextcloud_talk_bot.Nextcloudtalkbot import NextcloudTalkBot

#Initialize bot:
bot = NextcloudTalkBot()

# Via Module
from nextcloud_talk_bot.nextcloud_search import NextcloudSearch
# create instance
search = NextcloudSearch(base_url="https://example.com", username="user", password="password")
```
    
## Methods

1. get_providers()  
Retrieves the available search providers from the Nextcloud Search API.
Returns: A list of search provider dictionaries.
2. search(query, provider_id)  
Searches Nextcloud using the given query and provider ID.
- query: The search query.
- provider_id: The optional provider ID. If not provided, all available providers will be used.
- limit = limit of search results (default: 5)
Returns: A dictionary of search results for each provider. Each key in the dictionary represents the provider ID, and the corresponding value is a list of search result dictionaries.

Exceptions:  
Raises a ValueError exception if the specified provider ID is not found.
## Examples

```python
# search for "Test" in mails
bot.search("Test", "mail")

# search for "Test" on all provider
bot.search("Test")

# search for "Test" on provider fulltextsearch and limit results to first 5
bot.search("Test", "fulltextsearch", limit=5)

```