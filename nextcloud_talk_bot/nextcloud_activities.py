"""
handle activities
"""
import logging

from .nextcloud_data import NextcloudData
from .translations import TRANSLATIONS
from .nextcloud_requests import NextcloudRequests
from .i18n import _


class NextcloudActivities:
    """
    A class to handle Nextcloud activities.
    """

    def __init__(self, base_url, username, password, activity=None):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.activity = activity
        self.nextcloud_requests = NextcloudRequests(
            self.base_url, self.password)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_last_activities(self):
        """
        Get the last activities from Nextcloud.

        :return: A list of activities.
        """
        endpoint = "/ocs/v2.php/cloud/activity"
        response = self.nextcloud_requests.send_request(endpoint)
        self.logger.info("Getting the last activities from Nextcloud")
        return response['ocs']['data']

    def search_last_activities(self, activity):
        """
        Search for events, to-dos or file-operations in the given activities.

        :param activities: he activity to search for, i.e. to-do, event, shared, deleted, created, changed
        :return: A list of filtered activities.
        """
        response = self.get_last_activities()
        filtered_data = []
        for item in response:
            subject = item['subject']
            date = item['date']
            if activity in subject:
                filtered_data.append({'subject': subject, 'date': date})
        self.logger.info(f"Searching for '{activity}' in the last activities")
        return filtered_data


if __name__ == "__main__":
    ncdata = NextcloudData
    data = ncdata.read_nextcloud_data()
    for key, value in data.items():
        locals()[key] = value

    nextcloud = NextcloudActivities(NEXTCLOUD_URL, USERNAME, PASSWORD)
    last_activities = nextcloud.search_last_activities(activity="event")
    print(last_activities)
