"""
send requests to the Nextcloud API
"""
import requests
import logging
from requests_cache import CachedSession, disabled, install_cache

from .headers import NextcloudHeaders
from .i18n import _

install_cache('.ncb_requests', backend='sqlite', expire_after=90)
session = CachedSession('.ncb_requests', backend='sqlite',
                        expire_after=90)

# Create a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class NextcloudRequests:
    """
    This class provides functionality to send requests to the Nextcloud API.

    :param base_url: The base URL of the Nextcloud instance.
    :param password: The app password for the Nextcloud account.
    """

    def __init__(self, base_url, password=None, monitoring_token=None):
        self.base_url = base_url
        self.password = password
        self.monitoring_token = monitoring_token
        self.headers = NextcloudHeaders.create_headers(self.password)

    def send_request(self, endpoint, params=None, extra_headers=None):
        """
        Send a GET request to the specified Nextcloud API endpoint.

        :param endpoint: The API endpoint to send the request to.
        :param params: Optional dictionary of query parameters to include in the request. Default is None.
        :param extra_headers: Optional dictionary of additional headers to include in the request. Default is None.
        :return: The JSON response from the server.
        :raises Exception: If the response status code is not 200.
        """
        session.get('https://httpbin.org/get')
        headers = self.headers.copy()
        if extra_headers:
            headers.update(extra_headers)

        url = f"{self.base_url}{endpoint}"
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30)

        try:
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.warning(_("The request timed out."))
        except requests.exceptions.ConnectionError:
            logger.warning(_("There was a problem connecting to the API."))
        except requests.exceptions.HTTPError as error:
            if response.status_code == 401:
                logger.warning(
                    _("Authentication failed. Please check your credentials."))
            elif response.status_code == 403:
                logger.warning(
                    _("You don't have permission to access the requested resource."))
            elif response.status_code == 404:
                logger.warning(_("The requested resource was not found."))
            elif response.status_code >= 500:
                logger.warning(
                    _("There was a server-side error. Please try again later."))
            else:
                logger.warning(_(f"An HTTP error occurred: {error}"))

        return response.json()

    def send_request_to_monitoring(self, endpoint):
        session.get('https://httpbin.org/get')
        headers = NextcloudHeaders.create_nc_token_headers(
            self.monitoring_token)
        url = f"{self.base_url}{endpoint}"
        response = requests.get(
            url,
            headers=headers,
            timeout=10)
        if response.status_code == 429:
            raise ThrottlingException(_(
                "Your request has been throttled. Please try again later."))
        try:
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logger.warning(_("The request timed out."))
        except requests.exceptions.ConnectionError:
            logger.warning(_("There was a problem connecting to the API."))
        except requests.exceptions.HTTPError as error:
            if response.status_code == 401:
                logger.warning(
                    _("Authentication failed. Please check your credentials."))
            elif response.status_code == 403:
                logger.warning(
                    _("You don't have permission to access the requested resource."))
            elif response.status_code == 404:
                logger.warning(_("The requested resource was not found."))
            elif response.status_code >= 500:
                logger.warning(
                    _("There was a server-side error. Please try again later."))
            else:
                logger.warning(_(f"An HTTP error occurred: {error}"))

        return response.json()

    def post_request(self, endpoint, json=None):
        """
        Send a POST request to the specified Nextcloud API endpoint.

        :param endpoint: The API endpoint to send the request to.
        :param json: Optional dictionary containing the JSON payload to include in the request. Default is None.
        :return: The JSON response from the server.
        :raises Exception: If the response status code is not 200 or 201.
        """
        with disabled():
            headers = self.headers
            url = f"{self.base_url}{endpoint}"
            response = requests.post(
                url, headers=headers, json=json, timeout=10)

            try:
                response.raise_for_status()
            except requests.exceptions.Timeout:
                logger.warning(_("The request timed out."))
            except requests.exceptions.ConnectionError:
                logger.warning(_("There was a problem connecting to the API."))
            except requests.exceptions.HTTPError as error:
                if response.status_code == 401:
                    logger.warning(
                        _("Authentication failed. Please check your credentials."))
                elif response.status_code == 403:
                    logger.warning(
                        _("You don't have permission to access the requested resource."))
                elif response.status_code == 404:
                    logger.warning(_("The requested resource was not found."))
                elif response.status_code >= 500:
                    logger.warning(
                        _("There was a server-side error. Please try again later."))
                else:
                    logger.warning(_(f"An HTTP error occurred: {error}"))

            return response.json()

    def delete_request(self, endpoint):
        """
        Send a DELETE request to the specified Nextcloud API endpoint.

        :param endpoint: The API endpoint to send the request to.
        :return: None
        :raises Exception: If the response status code is not 204.
        """
        with disabled():
            headers = self.headers
            url = f"{self.base_url}{endpoint}"
            response = requests.delete(url, headers=headers, timeout=10)

            try:
                response.raise_for_status()
            except requests.exceptions.Timeout:
                logger.warning(_("The request timed out."))
            except requests.exceptions.ConnectionError:
                logger.warning(_("There was a problem connecting to the API."))
            except requests.exceptions.HTTPError as error:
                if response.status_code == 401:
                    logger.warning(
                        _("Authentication failed. Please check your credentials."))
                elif response.status_code == 403:
                    logger.warning(
                        _("You don't have permission to access the requested resource."))
                elif response.status_code == 404:
                    logger.warning(_("The requested resource was not found."))
                elif response.status_code >= 500:
                    logger.warning(
                        _("There was a server-side error. Please try again later."))
                else:
                    logger.warning(_(f"An HTTP error occurred: {error}"))


class ThrottlingException(Exception):
    pass
