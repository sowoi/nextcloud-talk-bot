import unittest
from unittest.mock import MagicMock, patch
from nextcloud_talk_bot.nextcloud_meeting import NextcloudMeeting


class TestNextcloudMeeting(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://example.com/nextcloud"
        self.username = "user"
        self.password = "password"

        with patch('nextcloud_talk_bot.nextcloud_meeting.NextcloudRequests') as mock_nextcloud_requests:
            self.mock_send_request = MagicMock()
            mock_nextcloud_requests.return_value = self.mock_send_request

            with patch('nextcloud_talk_bot.nextcloud_meeting.NextcloudTalkExtractor') as mock_nextcloud_talk_extractor:
                self.mock_talk_extractor = MagicMock()
                mock_nextcloud_talk_extractor.return_value = self.mock_talk_extractor

                self.nextcloud_meeting = NextcloudMeeting(
                    self.base_url, self.username, self.password)

    def test_create_room_success(self):
        room_name = "test_room"
        self.mock_talk_extractor.get_conversations_ids.return_value = {}
        self.mock_send_request.post_request.return_value = {
            "ocs": {
                "data": {"token": "12345", "displayName": room_name}
            }
        }

        result = self.nextcloud_meeting.create_room(room_name)
        self.assertEqual(result, f"{room_name} successfull created")

    def test_create_room_already_exists(self):
        room_name = "test_room"
        self.mock_talk_extractor.get_conversations_ids.return_value = {
            room_name: "12345"}

        result = self.nextcloud_meeting.create_room(room_name)
        self.assertEqual(result, f"{room_name} already exists")

    @patch("nextcloud_talk_bot.nextcloud_meeting.Confirmation")
    def test_delete_room_success(self, mock_confirmation):
        room_name = "test_room"
        self.mock_talk_extractor.get_conversations_ids.return_value = {
            room_name: "12345"}
        mock_confirmation.are_you_sure.return_value = True

        with patch("builtins.print") as mock_print:
            self.nextcloud_meeting.delete_room(room_name)
            mock_print.assert_called_with(f"Deleted {room_name}")

    def test_delete_room_not_exists(self):
        room_name = "test_room"
        self.mock_talk_extractor.get_conversations_ids.return_value = {}

        result = self.nextcloud_meeting.delete_room(room_name)
        self.assertEqual(result, f"{room_name} does not exist")


if __name__ == "__main__":
    unittest.main()
