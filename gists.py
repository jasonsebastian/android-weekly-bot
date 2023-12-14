import os
from dotenv import load_dotenv
import requests

load_dotenv()

GIST_ID = os.getenv("GIST_ID")
GIST_TOKEN = os.getenv("GIST_TOKEN")


def get_gist_content():
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    response = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=headers)
    if response.status_code == 200:
        gist_content = response.json()["files"]["subscribers.json"]["content"]
        return gist_content
    else:
        return None


def update_gist(new_content):
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    data = {"files": {"subscribers.json": {"content": new_content}}}
    response = requests.patch(
        f"https://api.github.com/gists/{GIST_ID}", json=data, headers=headers
    )
    return response.status_code == 200


if __name__ == "__main__":
    print(get_gist_content())
