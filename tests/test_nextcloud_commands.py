import unittest
from unittest.mock import MagicMock, patch
from nextcloud_talk_bot.nextcloud_commands import NextcloudCommands


class TestNextcloudCommands(unittest.TestCase):
    @patch('nextcloud_talk_bot.Nextcloudtalkbot.NextcloudTalkBot', autospec=True)
    def test_command(self, mock_nc_talk_bot):
        # Set the attributes of the MagicMock to prevent AttributeError
        mock_nc_talk_bot.return_value.NEXTCLOUD_URL = "https://example.com"
        mock_nc_talk_bot.return_value.USERNAME = "user"
        mock_nc_talk_bot.return_value.PASSWORD = "password"

    @patch('inspect.getmembers')
    def test_get_first_class(self, mock_getmembers):
        nc_command = NextcloudCommands("activities")
        nc_command.module = MagicMock()
        nc_command.get_first_class()
        mock_getmembers.assert_called_once()

    def test_print_first_class_docstring(self):
        nc_command = NextcloudCommands("activities")
        nc_command.get_first_class = MagicMock(
            return_value=MagicMock(
                __name__="TestClass",
                __doc__="Test docstring."))
        nc_command.print_first_class_docstring()

    def test_print_method_docstring(self):
        nc_command = NextcloudCommands("activities")
        nc_command.get_first_class = MagicMock(
            return_value=MagicMock(
                test_method=MagicMock(
                    __doc__="Test method docstring.")))
        nc_command.print_method_docstring("test_method")

    @patch('inspect.getmembers')
    def test_print_available_classes_and_methods(self, mock_getmembers):
        nc_command = NextcloudCommands("activities")
        nc_command.module = MagicMock()
        nc_command.print_available_classes_and_methods()
        mock_getmembers.assert_called_once()

    @patch('nextcloud_talk_bot.nextcloud_commands.NextcloudTalkBot')
    def test_call_class_method(self, mock_bot):
        mock_bot.return_value.NEXTCLOUD_URL = 'https://example.com'
        mock_bot.return_value.USERNAME = 'user'
        mock_bot.return_value.PASSWORD = 'password'
        nc_command = NextcloudCommands("activities")
        nc_command.get_first_class = MagicMock(return_value=MagicMock())
        mock_method = MagicMock(return_value="Test result")
        nc_command.bot = MagicMock(activities=MagicMock(test_method=mock_method))
        result = nc_command.call_class_method("test_method", "arg1", "arg2")
        mock_method.assert_called_once_with("arg1", "arg2")
        self.assertEqual(result, "Test result")


if __name__ == '__main__':
    unittest.main()
