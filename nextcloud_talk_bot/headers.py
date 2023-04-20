class NextcloudHeaders:
    @staticmethod
    def create_headers(password):
        """
        Helper script.
        Create and return headers for Nextcloud API requests.

        This function generates a dictionary containing headers required for making
        requests to the Nextcloud API. It sets the 'Authorization' header with the
        provided password.
        """

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'OCS-APIRequest': 'true',
            'Authorization': f"Bearer {password}",
            'Accept-Language': 'en'
        }
        return headers

    @staticmethod
    def create_nc_token_headers(monitoring_token):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'OCS-APIRequest': 'true',
            "NC-Token": monitoring_token}
        return headers
