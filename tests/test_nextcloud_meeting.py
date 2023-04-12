import unittest
from unittest.mock import MagicMock, patch
from nextcloud_talk_bot.nextcloud_meeting import NextcloudMeeting


class TestNextcloudMeeting(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://example.com/nextcloud"
        self.username = "user"
        self.password = "password"
        self.meeting = NextcloudMeeting(self.base_url, self.username, self.password)
        
        with patch('nextcloud_talk_bot.nextcloud_meeting.NextcloudRequests') as mock_nextcloud_requests:
            self.mock_send_request = MagicMock()
            mock_nextcloud_requests.return_value.send_request = self.mock_send_request


    @patch("nextcloud_talk_bot.nextcloud_meeting.NextcloudTalkExtractor")
    @patch("nextcloud_talk_bot.nextcloud_meeting.NextcloudRequests")
    def test_create_room(self, mock_nextcloud_requests, mock_nextcloud_talk_extractor):
        """
        Test the create_room method of the NextcloudMeeting class.

        :param mock_nextcloud_requests: The mock NextcloudRequests instance.
        :param mock_nextcloud_talk_extractor: The mock NextcloudTalkExtractor instance.
        """
        room_name = "test_room"
        
        mock_nextcloud_talk_extractor.get_conversations_ids.return_value = {}
        mock_nextcloud_requests.post_request.return_value = {
            "ocs": {
                "data": {"token": "12345", "displayName": room_name}
            }
        }

        result = self.meeting.create_room(room_name)
        self.assertEqual(result, f"{room_name} successfully created")

    @patch("nextcloud_talk_bot.nextcloud_meeting.NextcloudTalkExtractor")
    @patch("nextcloud_talk_bot.nextcloud_meeting.NextcloudRequests")
    def test_delete_room(self, mock_nextcloud_requests, mock_nextcloud_talk_extractor):
        """
        Test the delete_room method of the NextcloudMeeting class.

        :param mock_nextcloud_requests: The mock NextcloudRequests instance.
        :param mock_nextcloud_talk_extractor: The mock NextcloudTalkExtractor instance.
        """
        room_name = "test_room"

        mock_nextcloud_talk_extractor.get_conversations_ids.return_value = {room_name: "12345"}
        
        with patch("builtins.input", return_value="yes"):
            self.meeting.delete_room(room_name)
            mock_nextcloud_requests.delete_request.assert_called_with("/ocs/v2.php/apps/spreed/api/v4/room/12345")


if __name__ == "__main__":
    unittest.main()
