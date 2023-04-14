import unittest
from unittest.mock import Mock, patch

from nextcloud_talk_bot.nextcloud_activities import NextcloudActivities


class TestNextcloudActivities(unittest.TestCase):

    def test_get_last_activities(self):
        mock_response = {
            'ocs': {
                'data': [
                    {'subject': 'test event', 'date': '2023-04-13T10:00:00+00:00'}
                ]
            }
        }
        with patch("nextcloud_talk_bot.nextcloud_activities.NextcloudRequests") as MockNextcloudRequests:
            MockNextcloudRequests.return_value.send_request.return_value = mock_response
            nextcloud_activities = NextcloudActivities(
                "https://example.com", "username", "password")
            result = nextcloud_activities.get_last_activities()
            self.assertEqual(result, mock_response['ocs']['data'])

    def test_search_last_activities(self):
        activities = [
            {'subject': 'test event', 'date': '2023-04-13T10:00:00+00:00'},
            {'subject': 'test to-do', 'date': '2023-04-12T10:00:00+00:00'},
            {'subject': 'test event', 'date': '2023-04-11T10:00:00+00:00'},
        ]
        expected_filtered_activities = [
            {'subject': 'test event', 'date': '2023-04-13T10:00:00+00:00'},
            {'subject': 'test event', 'date': '2023-04-11T10:00:00+00:00'},
        ]
        with patch("nextcloud_talk_bot.nextcloud_activities.NextcloudRequests") as MockNextcloudRequests:
            nextcloud_activities = NextcloudActivities(
                "https://example.com", "username", "password")
            nextcloud_activities.get_last_activities = Mock(
                return_value=activities)
            result = nextcloud_activities.search_last_activities(
                activity="event")
            self.assertEqual(result, expected_filtered_activities)


if __name__ == "__main__":
    unittest.main()
