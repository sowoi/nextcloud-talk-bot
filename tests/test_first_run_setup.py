import unittest
from unittest.mock import patch
from nextcloud_talk_bot.first_run_setup import FirstRunSetup
from nextcloud_talk_bot.confirmation import Confirmation


class TestFirstRunSetup(unittest.TestCase):

    def test_encrypt_password(self):
        password = "test_password"
        key = FirstRunSetup.encrypt_password(password)
        self.assertIsInstance(
            key, bytes, "The encryption key should be of type 'bytes'")

    @patch("builtins.input", return_value="https://nextcloud.example.com")
    def test_get_nextcloud_url(self, input_mock):
        url = FirstRunSetup.get_nextcloud_url()
        self.assertEqual(url, "https://nextcloud.example.com")

    @patch("builtins.input", return_value="bot_user")
    def test_get_username(self, input_mock):
        username = FirstRunSetup.get_username()
        self.assertEqual(username, "bot_user")

    @patch("getpass.getpass", return_value="app_password")
    def test_get_password(self, getpass_mock):
        password = FirstRunSetup.get_password()
        self.assertEqual(password, "app_password")

    # You can add more tests for other methods like `check_nextcloud_credentials` and `select_nextcloud_talk_room`.
    # However, these tests might require more complex mocking due to their
    # interactions with external services or user input.


if __name__ == "__main__":
    unittest.main()
