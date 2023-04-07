# Nextcloud Talk Bot: Extractor

The NextcloudUser class represents a Nextcloud user and provides functionality to fetch user data and test user login by interacting with the Nextcloud API.

## Initialization:
To create an instance of the NextcloudTalkExtractor class, you will need the following information:

- base_url: The base URL for the Nextcloud server.
- username: The username for the Nextcloud user account.
- password: The password for the Nextcloud user account.

## Methods:

_send_request(self, endpoint)

This method sends a request to the Nextcloud API and returns the response.

Arguments:

    endpoint (str): The API endpoint to send the request to.

Returns:

    dict: A dictionary containing the response data if the request is successful, raises an exception otherwise.

test_user_login(self)

This method tests user login by attempting to retrieve user data from Nextcloud using the provided credentials.

Returns:

    dict: A dictionary containing the user's data if the login is successful, an error message otherwise.

get_preferred_language(self)

This method gets the user's preferred language from the Nextcloud server.

Returns:

    str: The preferred language if the request is successful, raises an exception otherwise.

get_quota(self)

This method gets the user's quota information from the Nextcloud server.

Returns:

    dict: A dictionary containing the user's quota information if the request is successful, raises an exception otherwise.


## Example

Here's an example of how to use the NextcloudUser class:

python

from nextcloud_user import NextcloudUser

base_url = "https://your-nextcloud-instance.com"
user = "your-username"
password = "your-password"

nc_user = NextcloudUser(base_url, user, password)
login_response = nc_user.test_user_login()

if "ocs" in login_response and "data" in login_response["ocs"]:
    print("Login successful!")
    preferred_language = nc_user.get_preferred_language()
    print(f"Preferred language: {preferred_language}")
    quota = nc_user.get_quota()
    print(f"Quota: {quota}")
else:
    print("Login failed!")

This code snippet demonstrates how to create an instance of the NextcloudUser class, test user login, get the user's preferred language, and fetch their quota information.