import unittest
from unittest.mock import MagicMock
from nextcloud_talk_bot.nextcloud_poll import NextcloudPoll


class TestNextcloudPoll(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://example.com"
        self.username = "testuser"
        self.password = "testpassword"
        self.room_name = "testroom"
        self.question = "What is your favorite color?"
        self.voting_options = ["Red", "Blue", "Green"]
        self.max_votes = 1
        self.result_mode = 0
        self.poll_id = 0

        self.nextcloud_poll = NextcloudPoll(self.base_url, self.username, self.password, self.room_name, self.question,
                                            self.voting_options, self.max_votes, self.result_mode, self.poll_id)

    def test_create_poll(self):
        self.nextcloud_poll.nextcloud_talk_extractor.get_conversations_ids = MagicMock(
            return_value={self.room_name: "token"}
        )
        self.nextcloud_poll.nextcloud_requests.post_request = MagicMock()

        self.nextcloud_poll.create_poll(self.question, self.voting_options, self.max_votes, self.result_mode)

        self.nextcloud_poll.nextcloud_talk_extractor.get_conversations_ids.assert_called_once()
        self.nextcloud_poll.nextcloud_requests.post_request.assert_called_once()

    def test_get_poll_result(self):
        self.nextcloud_poll.nextcloud_talk_extractor.get_conversations_ids = MagicMock(
            return_value={self.room_name: "token"}
        )
        self.nextcloud_poll.nextcloud_requests.send_request = MagicMock()

        self.nextcloud_poll.get_poll_result(self.poll_id)

        self.nextcloud_poll.nextcloud_talk_extractor.get_conversations_ids.assert_called_once()
        self.nextcloud_poll.nextcloud_requests.send_request.assert_called_once()

    def test_close_poll(self):
        self.nextcloud_poll.nextcloud_talk_extractor.get_conversations_ids = MagicMock(
            return_value={self.room_name: "token"}
        )
        self.nextcloud_poll.get_poll_result = MagicMock(
            return_value={"ocs": {"meta": {"statuscode": 200}, "data": {"question": self.question}}}
        )
        self.nextcloud_poll.nextcloud_requests.delete_request = MagicMock()
        Confirmation = MagicMock()
        Confirmation.are_you_sure = MagicMock(return_value=True)

        self.nextcloud_poll.close_poll(self.poll_id)

        self.nextcloud_poll.nextcloud_talk_extractor.get_conversations_ids.assert_called_once()
        self.nextcloud_poll.get_poll_result.assert_called_once()
        self.nextcloud_poll.nextcloud_requests.delete_request.assert_called_once()
        Confirmation.are_you_sure.assert_called_once_with("close", self.question)


if __name__ == "__main__":
    unittest.main()
