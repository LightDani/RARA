from connection import get_request
from requests import post
from keyring import set_password, get_password
from clear_console import clear_console
from time import sleep


def get_credential():
    try:
        clear_console()
        print("Press Ctrl+C to cancel")
        email = input("Enter your email: ")
        try:
            from getpass import getpass

            password = getpass("Enter your password: ")
        except ImportError:
            password = input("Enter your password: ")
        login_data = {"name": "", "email": email, "password": password}
        return login_data
    except KeyboardInterrupt:
        clear_console()
        print("Good bye!")
        return exit(1)


def get_api_token():
    api_token = get_password("rakamin", "api_token")
    if api_token:
        print("Last session detected, try to use old credential")
        print("Checking token validity...")
        headers = {
            "sort_column": "created_at",
            "sort_direction": "desc",
            "disable_pagination": "true",
            "Authorization": f"Bearer {api_token}",
        }
        json_data = get_request(
            url="https://api.rakamin.com/api/v1/user_notifications",
            headers=headers,
        )
        if json_data:
            print("Token is valid, Welcome!")
        else:
            print("Token is expired. Please Re-Login!")
            sleep(2)
            return None
    else:
        print("No session detected, login first!")
    sleep(2)
    return api_token


def set_api_token(api_token):
    option = input("Do you want to save your token? (y/n) ")
    if option.lower() == "y":
        set_password("rakamin", "api_token", api_token)
        print("Successfully saved token.")
        sleep(0.5)


def login():
    login_api = "https://api.rakamin.com/api/v1/auth/login"
    api_token = None
    while True:
        login_data = get_credential()
        if login_data == None:
            break
        response = post(login_api, data=login_data)

        if response.status_code == 200:
            api_token = response.json()["data"]["auth_token"]
            set_api_token(api_token)
            break
        else:
            print(response.status_code)
            print(f"Failed to authenticate. Status code: {response.status_code}")
            sleep(2)
    return api_token


def start():
    api_token = get_api_token()
    if not api_token:
        api_token = login()
    return api_token
