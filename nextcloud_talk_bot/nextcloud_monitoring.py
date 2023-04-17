import os
import json
import requests

class NextcloudMonitoring:
    """
    Interact with Nextcloud's monitoring API and fetch server information. 
    This class requires a token created via OCS command on the Nextcloud command.  
    """

    def __init__(self, url, token=None):
        """
        Initialize the NextcloudMonitoring class.
        
        :param url: The base URL of the Nextcloud instance.
        :param token: Optional authentication token. If not provided, the token will be read from the ".monitoring" file.
        """
        self.url = url.rstrip("/") + "/ocs/v2.php/apps/serverinfo/api/v1/info"
        self.token = token if token else self._read_token()


    def _read_token(self):
        """
        Read the authentication token from the '.monitoring' file in the home directory.
        
        :return: The authentication token as a string.
        """
        home_dir = os.path.expanduser("~")
        monitoring_file = os.path.join(home_dir, ".monitoring")
        with open(monitoring_file, "r") as f:
            return f.read().strip()

    def get_monitoring_data_raw(self):
        """
        Fetch the raw monitoring data from the Nextcloud instance.
        
        :return: A dictionary containing the monitoring data.
        """
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'OCS-APIRequest': 'true',"NC-Token": self.token}
        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(f"Request failed with status code {response.status_code}")

    def check_monitoring(self):
        data = self.get_monitoring_data_raw()
        nextcloud_data = data['ocs']['data']['nextcloud']
        system_data = nextcloud_data['system']
        storage_data = nextcloud_data['storage']
        apps_data = system_data['apps']

        mem_free = system_data['mem_free']
        swap_free = system_data['swap_free']
        storage_free = system_data['freespace']
        cpuload = system_data['cpuload']
        app_updates = apps_data['app_updates']

        print(f"Memory Free: {mem_free}")
        print(f"Swap Free: {swap_free}")
        print(f"Storage Free: {storage_free}")
        print(f"CPU Load: {cpuload}")

        mem_free_percentage = (mem_free / system_data['mem_total']) * 100
        if mem_free_percentage < 20:
            print("Warning: Less than 20% memory free.")

        if swap_free < system_data['swap_total']:
            print("Warning: The system is swapping.")

        if storage_free < 10 * 1024 * 1024 * 1024:
            print("Warning: Less than 10GB storage free.")

        if max(cpuload) > 10:
            print("Warning: CPU load is greater than 10.")

        if app_updates:
            print("Warning: There are app updates available for the following apps:")
            for app, version in app_updates.items():
                print(f"  - {app}: {version}")

 
if __name__ == "__main__":
    nextcloud_url = "https://nextcloudserver.abxys"
    user_token = "your-token-here"  # Replace with the user's token
    monitoring = NextcloudMonitoring(nextcloud_url, user_token)
    monitoring.check_monitoring()