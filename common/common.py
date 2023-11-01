import requests


def request_json(url: str) -> dict:
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        error_message = f"Error getting chain registry info for {url}"
        raise Exception(error_message)
