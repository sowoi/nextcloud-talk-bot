import unittest
from unittest.mock import MagicMock, patch
from nextcloud_talk_bot.nextcloud_poll import NextcloudPoll


class TestNextcloudPoll(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://example.com/nextcloud"
        self.username = "user"
        self.password = "password"
        self.room_name = "room_name"

        with patch('nextcloud_talk_bot.nextcloud_poll.NextcloudRequests') as mock_nextcloud_requests:
            self.mock_send_request = MagicMock()
            mock_nextcloud_requests.return_value = self.mock_send_request

            with patch('nextcloud_talk_bot.nextcloud_poll.NextcloudTalkExtractor') as mock_nextcloud_talk_extractor:
                self.mock_talk_extractor = MagicMock()
                mock_nextcloud_talk_extractor.return_value = self.mock_talk_extractor

                self.nextcloud_poll = NextcloudPoll(
                    self.base_url, self.username, self.password, self.room_name)

    def test_create_poll_success(self):
        self.mock_talk_extractor.get_conversations_ids.return_value = {
            self.room_name: "12345"}

        question = "Sample Question"
        voting_options = ["Option 1", "Option 2"]
        max_votes = 2
        result_mode = 1

        self.nextcloud_poll.create_poll(
            question, voting_options, max_votes, result_mode)
        self.mock_send_request.post_request.assert_called()

    def test_create_poll_room_not_exist(self):
        self.mock_talk_extractor.get_conversations_ids.return_value = {}

        result = self.nextcloud_poll.create_poll(
            "Sample Question", ["Option 1", "Option 2"])
        self.assertEqual(result, f"{self.room_name} does not exist")

    def test_get_poll_result_success(self):
        self.mock_talk_extractor.get_conversations_ids.return_value = {
            self.room_name: "12345"}
        poll_id = 1
        sample_response = {"ocs": {"data": {"some_data": "data"}}}
        self.mock_send_request.send_request.return_value = sample_response

        result = self.nextcloud_poll.get_poll_result(poll_id)
        self.assertEqual(result, sample_response)

    def test_get_poll_result_room_not_exist(self):
        self.mock_talk_extractor.get_conversations_ids.return_value = {}

        result = self.nextcloud_poll.get_poll_result(1)
        self.assertEqual(result, f"{self.room_name} does not exist")

    @patch("nextcloud_talk_bot.nextcloud_poll.Confirmation")
    def test_close_poll_success(self, mock_confirmation):
        self.mock_talk_extractor.get_conversations_ids.return_value = {
            self.room_name: "12345"}
        mock_confirmation.are_you_sure.return_value = True
        poll_id = 1
        sample_response = {
            "ocs": {
                "meta": {
                    "statuscode": 200}, "data": {
                    "question": "Sample Question"}}}
        self.mock_send_request.send_request.return_value = sample_response

        with patch("builtins.print") as mock_print:
            self.nextcloud_poll.close_poll(poll_id)
            mock_print.assert_called_with(f"Closed poll '{self.room_name}'")

    def test_close_poll_room_not_exist(self):
        self.mock_talk_extractor.get_conversations_ids.return_value = {}

        result = self.nextcloud_poll.close_poll(1)
        self.assertEqual(result, f"{self.room_name} does not exist")


if __name__ == "__main__":
    unittest.main()
