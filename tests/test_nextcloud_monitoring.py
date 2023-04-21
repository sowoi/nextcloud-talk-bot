import unittest
from unittest.mock import patch
from nextcloud_talk_bot.nextcloud_monitoring import NextcloudMonitoring


class TestNextcloudMonitoring(unittest.TestCase):

    def test_init_with_token(self):
        nc = NextcloudMonitoring(
            "https://example.com/ocs/v2.php/apps/serverinfo/api/v1/info",
            monitoring_token="my-token")
        self.assertEqual(
            nc.base_url,
            "https://example.com/ocs/v2.php/apps/serverinfo/api/v1/info")
        self.assertEqual(nc.monitoring_token, "my-token")

    @patch("nextcloud_talk_bot.nextcloud_monitoring.NextcloudMonitoring._read_token",
           return_value="my-token")
    def test_init_without_token(self, mock_read_token):
        nc = NextcloudMonitoring("https://example.com")
        self.assertEqual(
            nc.base_url,
            "https://example.com")
        self.assertEqual(nc.monitoring_token, "my-token")
        mock_read_token.assert_called_once()

    @patch("builtins.open", unittest.mock.mock_open(read_data="my-token"))
    def test_read_token(self):
        nc = NextcloudMonitoring("https://example.com")
        token = nc._read_token()
        self.assertEqual(token, "my-token")

    @patch("requests.get")
    def test_get_monitoring_data_raw(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ocs": "test_data"}
        mock_get.return_value = mock_response

        nc = NextcloudMonitoring(
            "https://example.com",
            monitoring_token="my-token")
        data = nc.get_monitoring_data_raw()
        self.assertEqual(data, {"ocs": "test_data"})
        mock_get.assert_called_once()

    # Additional tests can be added for check_monitoring() to validate printed
    # output and warnings.


if __name__ == '__main__':
    unittest.main()
