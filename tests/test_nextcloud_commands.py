import unittest
from unittest.mock import MagicMock, patch
from nextcloud_talk_bot.nextcloud_commands import NextcloudCommands

class MockBot:
    def __init__(self):
        self.NEXTCLOUD_URL = "https://example.com/nextcloud"

class TestNextcloudCommandsBot(NextcloudCommands):
    def __init__(self, module_name, bot):
        super().__init__(module_name)
        self.bot = bot

class TestNextcloudCommands(unittest.TestCase):

    def test_map_input_to_module(self):
        nc_command = TestNextcloudCommandsBot("activities", bot=MockBot())
        self.assertEqual(nc_command.module_name, "nextcloud_activities")

    @patch('inspect.getmembers')
    def test_get_first_class(self, mock_getmembers):
        nc_command = TestNextcloudCommandsBot("activities", bot=MockBot())
        nc_command.module = MagicMock()
        nc_command.get_first_class()
        mock_getmembers.assert_called_once()

    def test_print_first_class_docstring(self):
        nc_command = TestNextcloudCommandsBot("activities", bot=MockBot())
        nc_command.get_first_class = MagicMock(
            return_value=MagicMock(
                __name__="TestClass",
                __doc__="Test docstring."))
        nc_command.print_first_class_docstring()

    def test_print_method_docstring(self):
        nc_command = TestNextcloudCommandsBot("activities", bot=MockBot())
        nc_command.get_first_class = MagicMock(
            return_value=MagicMock(
                test_method=MagicMock(
                    __doc__="Test method docstring.")))
        nc_command.print_method_docstring("test_method")


def test_call_class_method(self):
    nc_command = TestNextcloudCommandsBot("activities", bot=MockBot())
    nc_command.get_first_class = MagicMock(return_value=MagicMock())
    mock_method = MagicMock(return_value="Test result")
    nc_command.bot = MagicMock(activities=MagicMock(test_method=mock_method))
    result = nc_command.call_class_method("test_method", "arg1", "arg2")
    mock_method.assert_called_once_with("arg1", "arg2")
    self.assertEqual(result, "Test result")

    @patch('inspect.getmembers')
    def test_print_available_classes_and_methods(self, mock_getmembers):
        nc_command = TestNextcloudCommandsBot("activities", bot=MockBot())
        nc_command.module = MagicMock()
        nc_command.print_available_classes_and_methods()
        mock_getmembers.assert_called_once()


if __name__ == '__main__':
    unittest.main()
