import os

from .nextcloud_requests import NextcloudRequests
from .i18n import _


class NextcloudMonitoring:
    """
    Interact with Nextcloud's monitoring API and fetch server information.
    This class requires a token created via OCS command on the Nextcloud command.
    """

    def __init__(self, base_url, monitoring_token=None):
        """
        Initialize the NextcloudMonitoring class.

        :param base_url: The base URL of the Nextcloud instance.
        :param monitoring_token: Optional authentication token. If not provided, the token will be read from the ".monitoring" file.
        """
        self.base_url = base_url
        self.monitoring_token = monitoring_token if monitoring_token is not None else self._read_token()

    def _read_token(self):
        """
        Read the authentication token from the '.monitoring' file in the home directory.

        :return: The authentication token as a string.
        """
        home_dir = os.path.expanduser("~")
        monitoring_file = os.path.join(home_dir, ".monitoring")
        with open(monitoring_file, "r") as f:
            token = f.read().strip()
            return token

    def get_monitoring_data_raw(self):
        """
        Fetch the raw monitoring data from the Nextcloud instance.

        :return: A dictionary containing the monitoring data.
        """

        endpoint = "/ocs/v2.php/apps/serverinfo/api/v1/info"
        self.request = NextcloudRequests(
            self.base_url, monitoring_token=self.monitoring_token)
        response = self.request.send_request_to_monitoring(endpoint)
        return response

    def check_monitoring(self):
        """
        Check monitoring data and generate a dictionary with results.

        :return: A dictionary containing monitoring results.
        """
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

        results = {
            'Memory Free': mem_free,
            'Swap Free': swap_free,
            'Storage Free': storage_free,
            'CPU Load': cpuload,
            'mem_free_percentage': (mem_free / system_data['mem_total']) * 100,
            'system_swapping': swap_free < system_data['swap_total'],
            'storage_less_than_10GB': storage_free < 10 * 1024 * 1024 * 1024,
            'cpu_load_greater_than_10': max(cpuload) > 10,
            'app_updates': app_updates
        }

        return results

    def show_monitoring_results(self):
        """
        Show monitoring results using the check_monitoring() method.

        :return: None
        """
        results = self.check_monitoring()
        print(f"{_('Memory Free: ')}{results['Memory Free']}")
        print(f"{_('Swap Free: ')}{results['Swap Free']}")
        print(f"{_('Storage Free: ')}{results['Storage Free']}")
        print(f"{_('CPU Load: ')}{results['CPU Load']}")

        if results['mem_free_percentage'] < 20:
            print(_("Warning: Less than 20% memory free."))

        if results['system_swapping']:
            print(_("Warning: The system is swapping."))

        if results['storage_less_than_10GB']:
            print(_("Warning: Less than 10GB storage free."))

        if results['cpu_load_greater_than_10']:
            print(_("Warning: CPU load is greater than 10."))

        if results['app_updates']:
            print(
                _("Warning: There are app updates available for the following apps:"))
            for app, version in results['app_updates'].items():
                print(f"  - {app}: {version}")
