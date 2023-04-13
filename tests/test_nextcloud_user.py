import unittest
from unittest.mock import MagicMock
from nextcloud_talk_bot.nextcloud_user import NextcloudUser


class TestNextcloudUser(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://example.com/nextcloud"
        self.user = "testuser"
        self.password = "mypassword"
        self.nextcloud_user = NextcloudUser(
            self.base_url, self.user, self.password)

    def test_test_user_login(self):
        mock_response = {"ocs": {"data": {"id": self.user}}}
        self.nextcloud_user.nextcloud_requests.send_request = MagicMock(
            return_value=mock_response)

        response = self.nextcloud_user.test_user_login()
        self.assertEqual(response, mock_response)

    def test_get_preferred_language(self):
        mock_response = {
            "ocs": {
                "data": {
                    "id": self.user,
                    "language": "en",
                }
            }
        }
        self.nextcloud_user.nextcloud_requests.send_request = MagicMock(
            return_value=mock_response)

        response = self.nextcloud_user.get_preferred_language()
        self.assertEqual(response, "en")

    def test_get_quota(self):
        mock_response = {
            "ocs": {
                "data": {
                    "id": self.user,
                    "quota": {
                        "free": 53687091200,
                        "used": 1073741824,
                        "total": 54760833024,
                        "relative": 1.96,
                    },
                }
            }
        }
        self.nextcloud_user.nextcloud_requests.send_request = MagicMock(
            return_value=mock_response)

        response = self.nextcloud_user.get_quota()
        self.assertEqual(response, mock_response["ocs"]["data"]["quota"])


if __name__ == "__main__":
    unittest.main()
