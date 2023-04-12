# test_nextcloud_activities.py

import unittest
from unittest.mock import MagicMock, patch
from nextcloud_talk_bot.nextcloud_activities import NextcloudActivities


class TestNextcloudActivities(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://test.nextcloud.com"
        self.username = "username"
        self.password = "password"

        with patch('nextcloud_talk_bot.nextcloud_activities.NextcloudRequests') as mock_nextcloud_requests:
            self.mock_send_request = MagicMock()
            mock_nextcloud_requests.return_value.send_request = self.mock_send_request

            self.nextcloud_activities = NextcloudActivities(self.base_url, self.username, self.password)

    def test_get_last_activities(self):
        activities = [{"subject": "Test activity 1", "date": "2023-04-10T00:00:00+00:00"},
                      {"subject": "Test activity 2", "date": "2023-04-11T00:00:00+00:00"}]

        self.mock_send_request.return_value = {"ocs": {"data": activities}}

        result = self.nextcloud_activities.get_last_activities()
        self.assertEqual(result, activities)
        self.mock_send_request.assert_called_with("/ocs/v2.php/cloud/activity")

    def test_search_last_activities(self):
        activities = [{"subject": "Test event", "date": "2023-04-10T00:00:00+00:00"},
                      {"subject": "Test to-do", "date": "2023-04-11T00:00:00+00:00"}]

        self.mock_send_request.return_value = {"ocs": {"data": activities}}

        result = self.nextcloud_activities.search_last_activities(activity="event")
        self.assertEqual(result, [{"subject": "Test event", "date": "2023-04-10T00:00:00+00:00"}])


if __name__ == "__main__":
    unittest.main()