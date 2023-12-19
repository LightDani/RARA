from requests import get, patch


def get_request(url, headers=None, api_token=None):
    if api_token:
        headers = {"Authorization": f"Bearer {api_token}"}
    response = get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to call. Status code: {response.status_code}")
        return None


def patch_request(url, api_token, payload=None):
    headers = {"Authorization": api_token}
    patch(url=url, json=payload, headers=headers)
