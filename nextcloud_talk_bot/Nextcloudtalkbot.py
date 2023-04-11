import os
from .check_local_user_enviroment import SudoPrivileges
from .first_run_setup import FirstRunSetup
from .nextcloud_activities import NextcloudActivities
from .nextcloud_file_operations import NextcloudFileOperations
from .nextcloud_talk_extractor import NextcloudTalkExtractor
from .nextcloud_user import NextcloudUser
from .nextcloud_meeting import NextcloudMeeting
from .nextcloud_poll import NextcloudPoll
from .nextcloud_requests import NextcloudRequests
from .nextcloud_data import NextcloudData
from .nextcloud_messages import NextcloudMessages
from .headers import NextcloudHeaders
from .translations import TRANSLATIONS
from .confirmation import are_you_sure
from .permissions_map import permissions_map
from .conversations_map import conversations_map


class NextcloudTalkBot:     
    def __init__(self):
        self._data = None
        home_dir = os.path.expanduser("~")
        nextclouddata_file_path = os.path.join(home_dir, ".nextclouddata")
        if os.path.exists(nextclouddata_file_path):
            self._data = NextcloudData.read_nextcloud_data()
        
        else:
            # .nextclouddata file does not exists
            pass

    def __getattr__(self, name):
        if self._data and name in self._data:
            return self._data[name]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
