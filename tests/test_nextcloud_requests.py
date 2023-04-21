import unittest
from unittest.mock import MagicMock
from nextcloud_talk_bot.nextcloud_requests import NextcloudRequests


class TestNextcloudRequests(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://example.com/nextcloud"
        self.password = "mypassword"
        self.nextcloud_requests = NextcloudRequests(
            self.base_url, self.password)

    def test_send_request(self):
        endpoint = "/api/v1/users"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"users": []}

        with unittest.mock.patch("requests.get", return_value=mock_response) as mock_get:
            response = self.nextcloud_requests.send_request(endpoint)
            self.assertEqual(response, {"users": []})
            mock_get.assert_called_with(
                f"{self.base_url}{endpoint}",
                headers=self.nextcloud_requests.headers,
                params=None,
                timeout=30)

    def test_post_request(self):
        endpoint = "/api/v1/users"
        json_payload = {"username": "testuser", "email": "test@example.com"}
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"user": "testuser"}

        with unittest.mock.patch("requests.post", return_value=mock_response) as mock_post:
            response = self.nextcloud_requests.post_request(
                endpoint, json=json_payload)
            self.assertEqual(response, {"user": "testuser"})
            mock_post.assert_called_with(
                f"{self.base_url}{endpoint}",
                headers=self.nextcloud_requests.headers,
                json=json_payload,
                timeout=10)

    def test_delete_request(self):
        endpoint = "/api/v1/users/testuser"
        mock_response = MagicMock()
        mock_response.status_code = 200

        with unittest.mock.patch("requests.delete", return_value=mock_response) as mock_delete:
            self.nextcloud_requests.delete_request(endpoint)
            mock_delete.assert_called_with(
                f"{self.base_url}{endpoint}",
                headers=self.nextcloud_requests.headers,
                timeout=10)


if __name__ == "__main__":
    unittest.main()
