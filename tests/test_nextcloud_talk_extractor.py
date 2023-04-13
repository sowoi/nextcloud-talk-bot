import unittest
from unittest.mock import MagicMock
from nextcloud_talk_bot.nextcloud_talk_extractor import NextcloudTalkExtractor


class TestNextcloudTalkExtractor(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://example.com/nextcloud"
        self.username = "testuser"
        self.password = "mypassword"
        self.room_id = "12345678"
        self.talk_extractor = NextcloudTalkExtractor(
            self.base_url, self.username, self.password, self.room_id)

    def test_get_conversations_ids(self):
        mock_response = {
            "ocs": {
                "data": [
                    {"token": "12345678", "displayName": "Test Room"},
                    {"token": "87654321", "displayName": "Another Room"}
                ]
            }
        }
        self.talk_extractor.nextcloud_requests.send_request = MagicMock(
            return_value=mock_response)

        conversations = self.talk_extractor.get_conversations_ids()
        self.assertEqual(
            conversations, {
                "Test Room": "12345678", "Another Room": "87654321"})

    def test_get_participants(self):
        mock_response = {
            "ocs": {
                "data": [
                    {"displayName": "Alice"},
                    {"displayName": "Bob"}
                ]
            }
        }
        self.talk_extractor.nextcloud_requests.send_request = MagicMock(
            return_value=mock_response)

        participants = self.talk_extractor.get_participants(self.room_id)
        self.assertEqual(participants, ["Alice", "Bob"])

    def test_get_user_permissions(self):
        mock_response = {
            "ocs": {
                "data": [
                    {"actorId": "1", "permissions": 3},
                    {"actorId": "2", "permissions": 1}
                ]
            }
        }
        self.talk_extractor.nextcloud_requests.send_request = MagicMock(
            return_value=mock_response)

        permissions = self.talk_extractor.get_user_permissions(self.room_id)
        self.assertEqual(permissions, {
            "1": "Default permissions (will pick the one from the next level of: user, call, conversation), Custom permissions (this is required to be able to remove all other permissions), Start call",
            "2": "Default permissions (will pick the one from the next level of: user, call, conversation), Custom permissions (this is required to be able to remove all other permissions)"
        })

    def test_get_messages(self):
        mock_response = {
            "ocs": {
                "data": [
                    {"message": "Hello, World!"},
                    {"message": "How are you?"}
                ]
            }
        }
        self.talk_extractor.nextcloud_requests.send_request = MagicMock(
            return_value=mock_response)

        messages = self.talk_extractor.get_messages(
            self.room_id, message_limit=2)
        self.assertEqual(messages, ["Hello, World!", "How are you?"])


if __name__ == "__main__":
    unittest.main()
