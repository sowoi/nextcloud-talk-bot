import logging
from .nextcloud_requests import NextcloudRequests
from .i18n import _


class NextcloudSearch:
    def __init__(self, base_url, username, password):
        """
        Initializes the NextcloudSearch class.

        :param base_url: The base URL of the Nextcloud instance.
        :param username: The username for authentication.
        :param password: The password for authentication.
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.nextcloud_requests = NextcloudRequests(
            self.base_url, self.password)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_providers(self):
        """
        Retrieves the ID of the given search provider.

        :param provider_name: The name of the search provider.
        :return: The ID of the search provider if found, None otherwise.
        """
        endpoint = "/ocs/v2.php/search/providers"
        response = self.nextcloud_requests.send_request(endpoint)
        providers = response['ocs']['data']

        self.logger.info(f"Retrieved search providers: {providers}")

        return providers

    def search(self, query, provider_id=None, limit=5):
        """
        Searches Nextcloud using the given query and provider ID.
        0
        :param query: The search query.
        :param provider_id: The optional provider ID. If not provided, all available providers will be used.
        :param limit: limits the search results (default: 5)
        :return: A list of search results.
        """
        if provider_id is None:
            providers = self.get_providers()
        else:
            providers = [
                provider for provider in self.get_providers() if provider['id'] == provider_id]

        if not providers:
            raise ValueError(f"Provider {provider_id} not found.")

        results = []
        searchProviderResults = {}
        for provider in providers:
            endpoint = f"/ocs/v2.php/search/providers/{provider['id']}/search?term={query}&limit={limit}"
            response = self.nextcloud_requests.send_request(endpoint)

            for entry in response['ocs']['data']['entries']:
                result = {}
                result['title'] = entry.get('title', '')
                result['subline'] = entry.get('subline', '')
                result['resourceUrl'] = entry.get('resourceUrl', '')
                results.append(result)
        searchProviderResults[provider['id']] = results

        self.logger.info(
            f"Search results for query '{query}' using provider {provider_id}: {results}")

        return searchProviderResults
