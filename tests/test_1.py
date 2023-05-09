import pytest
import requests
import collections
import json
from nextcloud_talk_bot.first_run_setup import FirstRunSetup
#from nextcloud_talk_bot.nextcloud_user import NextcloudUser

def mock_os_path_exists(path):
    return True



def mock_user(monkeypatch):
    user_data["ocs"]["meta"]["statuscode"] = "200"
    return user_data["ocs"]["meta"]["statuscode"]

    

@pytest.fixture
def check_nextcloud_credentials(monkeypatch):
    Result = collections.namedtuple("Result", ["valid", "room_name", "room_token"])
    return Result


@pytest.fixture
def nextcloud_requests(monkeypatch):
    return 200


def test_check_if_data_file_already_exists_true(monkeypatch):
    check_data = FirstRunSetup()
    monkeypatch.setattr("os.path.exists", mock_os_path_exists)
    monkeypatch.setattr("builtins.input", lambda _: 'no')
    with pytest.raises(SystemExit):
        check_data.check_if_data_file_already_exists()
        
        

def test_get_credentials(monkeypatch):
    check_data = FirstRunSetup()
    inputs = ['self', 'https://example.org', 'testBot']
    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))
    monkeypatch.setattr('getpass.getpass', lambda _ : 'testPassword')   
    with pytest.raises(requests.exceptions.MissingSchema):
        check_data.get_credentials()
        
def test_check_nextcloud_credentials(check_nextcloud_credentials, monkeypatch):
    # Setup
    url = "https://example.com/nextcloud"
    username = "testuser"
    password = "testpassword"    
    check_cred = FirstRunSetup()
    monkeypatch.setattr("status_code", lambda _ : mock_user)
    check_cred.check_nextcloud_credentials(url, username, password)
    assert result.valid
    assert result.room_name is not None
    assert result.room_token is not None


    

