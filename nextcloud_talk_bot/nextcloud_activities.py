#/usr/bin/python3
import requests
from read_data import read_nextcloud_data
from translations import TRANSLATIONS
from constants import HEADERSNC

class NextcloudActivities:
    """
    A class to handle Nextcloud activities.
    """

    def __init__(self, NEXTCLOUD_URL, USERNAME, PASSWORD):
        self.NEXTCLOUD_URL = NEXTCLOUD_URL
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD

    def get_last_activities(self):
        """
        Get the last activities from Nextcloud.

        :return: A list of activities.
        """
        api_url = f"{self.NEXTCLOUD_URL}/ocs/v2.php/cloud/activity"
        auth = (self.USERNAME, self.PASSWORD)
        response = requests.get(api_url, headers=HEADERSNC, auth=auth)

        if response.status_code == 200:
            data = response.json()
            activities = data['ocs']['data']
            return activities

    def search_last_activities(self, activities):
        """
        Search for events and to-dos in the given activities.

        :param activities: A list of activities.
        :return: A list of filtered activities containing events and to-dos.
        """
        filtered_data = []
        for item in activities:
            subject = item['subject']
            date = item['date']
            if 'event' in subject or 'to-do' in subject:
                filtered_data.append({'subject': subject, 'date': date})

        return filtered_data

if __name__ == "__main__":
    data = read_nextcloud_data()

    for key, value in data.items():
        locals()[key] = value

    nextcloud = NextcloudActivities(NEXTCLOUD_URL, USERNAME, PASSWORD)
    last_activities = nextcloud.get_last_activities()
    filtered_activities = nextcloud.search_last_activities(last_activities)
    print(filtered_activities)
