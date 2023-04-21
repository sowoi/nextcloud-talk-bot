import unittest
from unittest.mock import Mock

from nextcloud_talk_bot.confirmation import Confirmation


class TestConfirmation(unittest.TestCase):

    def test_are_you_sure_yes(self):
        input_mock = Mock(return_value="yes")
        confirm = Confirmation("delete", "file", input_func=input_mock)
        self.assertTrue(confirm.are_you_sure())
        input_mock.assert_called_once_with(
            "Are you sure you want to delete 'file'? This process is irrevocable! (yes/no): ")

    def test_are_you_sure_no(self):
        input_mock = Mock(return_value="no")
        confirm = Confirmation("delete", "file", input_func=input_mock)
        self.assertFalse(confirm.are_you_sure())
        input_mock.assert_called_once_with(
            "Are you sure you want to delete 'file'? This process is irrevocable! (yes/no): ")

    def test_are_you_sure_invalid_input(self):
        input_mock = Mock(side_effect=["invalid", "yes"])
        confirm = Confirmation("delete", "file", input_func=input_mock)
        self.assertTrue(confirm.are_you_sure())
        input_mock.assert_has_calls([
            unittest.mock.call(
                "Are you sure you want to delete 'file'? This process is irrevocable! (yes/no): "),
            unittest.mock.call(
                "Are you sure you want to delete 'file'? This process is irrevocable! (yes/no): "),
        ])


if __name__ == "__main__":
    unittest.main()
