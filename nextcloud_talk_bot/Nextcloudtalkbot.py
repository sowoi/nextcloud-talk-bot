import os
from .check_local_user_enviroment import SudoPrivileges
from .first_run_setup import FirstRunSetup
from .nextcloud_activities import NextcloudActivities
from .nextcloud_file_operations import NextcloudFileOperations
from .nextcloud_talk_extractor import NextcloudTalkExtractor
from .nextcloud_user import NextcloudUser
from .nextcloud_meeting import NextcloudMeeting
from .nextcloud_poll import NextcloudPoll
# from .nextcloud_requests import NextcloudRequests
from .nextcloud_data import NextcloudData
from .nextcloud_messages import NextcloudMessages
from .headers import NextcloudHeaders
from .translations import TRANSLATIONS
# from .confirmation import Confirmation
from .permissions_map import permissions_map
from .conversations_map import conversations_map
# from .docstring_printer import DocstringPrinter


class NextcloudTalkBot:
    def __init__(
            self,
            base_url=None,
            username=None,
            password=None,
            room_name=None,
            room_token=None):
        self._data = None
        home_dir = os.path.expanduser("~")
        nextclouddata_file_path = os.path.join(home_dir, ".nextclouddata")
        if os.path.exists(nextclouddata_file_path):
            self._data = NextcloudData.read_nextcloud_data()
            self.config = {
                "nextcloud_base_data": {
                    "base_url": f"{self._data['NEXTCLOUD_URL']}",
                    "username": f"{self._data['USERNAME']}",
                    "password": f"{self._data['PASSWORD']}"
                },
                "nextcloud_base_data_without_username": {
                    "base_url": f"{self._data['NEXTCLOUD_URL']}",
                    "password": f"{self._data['PASSWORD']}"
                },
                "nextcloud_base_data_with_room_token": {
                    "base_url": f"{self._data['NEXTCLOUD_URL']}",
                    "username": f"{self._data['USERNAME']}",
                    "password": f"{self._data['PASSWORD']}",
                    "room_token": f"{self._data['ROOM_TOKEN']}"
                },
                "nextcloud_base_data_with_room_name": {
                    "base_url": f"{self._data['NEXTCLOUD_URL']}",
                    "username": f"{self._data['USERNAME']}",
                    "password": f"{self._data['PASSWORD']}",
                    "room_name": f"{self._data['ROOM_NAME']}"
                }
            }

        else:
            # .nextclouddata file does not exists
            self.config = {
                "nextcloud_base_data": {
                    "base_url": base_url,
                    "username": username,
                    "password": password
                },
                "nextcloud_base_data_without_username": {
                    "base_url": base_url,
                    "password": password
                },
                "nextcloud_base_data_with_room_token": {
                    "base_url": base_url,
                    "username": username,
                    "password": password,
                    "room_token": room_token
                },
                "nextcloud_base_data_with_room_name": {
                    "base_url": base_url,
                    "username": username,
                    "password": password,
                    "room_name": room_name
                }
            }

        self.activities = NextcloudActivities(
            **self.config["nextcloud_base_data"])
        self.file = NextcloudFileOperations(
            **self.config["nextcloud_base_data"])
        self.extractor = NextcloudTalkExtractor(
            **self.config["nextcloud_base_data"])
        self.user = NextcloudUser(**self.config["nextcloud_base_data"])
        self.meeting = NextcloudMeeting(**self.config["nextcloud_base_data"])
        self.poll = NextcloudPoll(
            **self.config["nextcloud_base_data_with_room_name"])
        self.messages = NextcloudMessages(
            **self.config["nextcloud_base_data_with_room_token"])
        self.setup = FirstRunSetup()
        self.translations = TRANSLATIONS
        self.permissions_map = permissions_map
        self.conversations_map = conversations_map

    def __getattr__(self, name):
        if self._data and name in self._data:
            return self._data[name]
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'")
