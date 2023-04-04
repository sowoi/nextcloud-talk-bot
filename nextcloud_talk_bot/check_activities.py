import requests
import json
from read_data import read_nextcloud_data


data = read_nextcloud_data()

for key, value in data.items():
    locals()[key] = value


HEADERSNC = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'OCS-APIRequest': 'true',
    "Authorization": f"Bearer {PASSWORD}"
}


def get_nextcloud_last_activities(NEXTCLOUD_URL, USERNAME, PASSWORD):
    # Define API endpoint URL
    api_url = f"{NEXTCLOUD_URL}/ocs/v2.php/cloud/activity?format=json"

    # Set up the authentication
    auth = (USERNAME, PASSWORD)

    # Send an HTTP GET request
    response = requests.get(api_url, headers=HEADERSNC, auth=auth)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the activities from the JSON data
        activities = data['ocs']['data']
        #filtered_subjects = [item["subject"] for item in activities if "event" in item["subject"] or "to-do" in item["subject"]]
        filtered_data = []
        for item in activities:
            subject = item['subject']
            date = item['date']
            if 'event' in subject or 'to-do' in subject:
                 filtered_data.append({'subject': subject, 'date': date})
            
                       
        # Return the activities
        return filtered_data
    else:
        # In case of an error, return an empty list
        return []


    
if __name__ == "__main__":
    last_activities = get_nextcloud_last_activities(NEXTCLOUD_URL, USERNAME, PASSWORD)
    print(last_activities)

