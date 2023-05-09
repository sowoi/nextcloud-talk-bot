import os
import requests

# enviroment variables
API_BASE_URL = os.getenv("NTB_URL")
API_USERNAME = os.getenv("NTB_USER")
API_PASSWORD = os.getenv("NTB_PASSWORD")
MONITORING_TOKEN = os.getenv("MONITORING_TOKEN")


def get_headers(API_PASSWORD):
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'OCS-APIRequest': 'true',
        'Authorization': f"Bearer {API_PASSWORD}",
        'Accept-Language': 'en'
    }


def get_test_room():
    headers = get_headers(API_PASSWORD)
    url = f"{API_BASE_URL}/ocs/v2.php/apps/spreed/api/v4/room"
    response = requests.get(url, headers=headers)
    conversation_list = response.json()
    for room in conversation_list["ocs"]["data"]:
        if room["displayName"] == "test":
            conversation_token = room["token"]
    return conversation_token


def test_api_endpoints(test_room_token):
    headers = get_headers(API_PASSWORD)
    GET_ENDPOINTS = [
        "/ocs/v2.php/apps/spreed/api/v4/room",
        "/ocs/v2.php/cloud/activity",
        "/ocs/v2.php/cloud/user",
        "/ocs/v2.php/search/providers",
    ]

    params = {
        "limit": 1,
        "lookIntoFuture": 0,
        "includeLastKnown": 1
    }

    poll_data = {
        "question": "Did this test work?",
        "options": ["yes", "no"],
        "resultMode": 0,
        "maxVotes": 1
    }

    # testing endpoints via requests
    for endpoint in GET_ENDPOINTS:
        url = f"{API_BASE_URL}{endpoint}"
        print(f"Testing {endpoint}")
        response = requests.get(
            url,
            headers=headers,
            params=params,
            json=poll_data)
        assert response.status_code == 200, f"Request failed {endpoint}: {response.status_code}"

    url = f"{API_BASE_URL}/ocs/v2.php/apps/spreed/api/v1/chat/{test_room_token}"
    response = requests.get(
        url,
        headers=headers,
        params=params,
        json=poll_data)
    assert response.status_code == 200, f"Request failed {endpoint}: {response.status_code}"

    data = {'actorDisplayName': "Guest", 'message': "TEST"}
    endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{test_room_token}"
    url = f"{API_BASE_URL}/{endpoint}"
    requests.post(url, headers=headers, json=data)

    url = f"{API_BASE_URL}/ocs/v2.php/apps/spreed/api/v1/chat/{test_room_token}"
    response = requests.get(
        url,
        headers=headers,
        params=params,
        json=poll_data).json()
    message_id = response['ocs']['data'][0]['id']
    endpoint = f"/ocs/v2.php/apps/spreed/api/v1/chat/{test_room_token}/{message_id}"
    url = f"{API_BASE_URL}{endpoint}"
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200, f"Request failed {endpoint}: {response.status_code}"

    url = f"{API_BASE_URL}/ocs/v2.php/apps/spreed/api/v1/poll/{test_room_token}"
    response = requests.post(url, headers=headers, json=poll_data).json()
    print("Testing /ocs/v2.php/apps/spreed/api/v1/poll/")
    assert response['ocs']['meta'][
        'statuscode'] == 201, f"Request failed {endpoint}: {response['ocs']['meta']['statuscode']}"
    poll_id = response['ocs']['data']['id']
    url = f"{url}/{poll_id}"
    response = requests.delete(url, headers=headers).json()
    assert response['ocs']['meta'][
        'statuscode'] == 200, f"Request failed {endpoint}: {response['ocs']['meta']['statuscode']}"


def test_monitoring():
    endpoint = "/ocs/v2.php/apps/serverinfo/api/v1/info"
    url = f"{API_BASE_URL}{endpoint}"
    print(f"Testing {endpoint}")

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'OCS-APIRequest': 'true',
        "NC-Token": MONITORING_TOKEN
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Request failed for {endpoint}: {response.status_code}"


if __name__ == "__main__":
    test_room_token = get_test_room()
    test_api_endpoints(test_room_token)
    test_monitoring()
    print("All API tests successfully completed.")
