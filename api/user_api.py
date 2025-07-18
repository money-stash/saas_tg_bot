import json
import requests

DOMAIN = "http://localhost:5555/"


def add_new_user(user_id, username, key):
    url = f"{DOMAIN}add-user"
    data = {"user_id": user_id, "username": username, "key": key}

    response = requests.post(url, data=data)
    print("Response:", response.json())


def update_add_new_user(user_id, username, key):
    url = f"{DOMAIN}update-user-login"
    data = {"user_id": user_id, "username": username, "key": key}

    response = requests.post(url, data=data)
    print("Response:", response.json())


def get_users():
    url = f"{DOMAIN}users"

    response = requests.get(url)
    return response.json()


def get_key_info(key):
    url = f"{DOMAIN}get_key_info"
    data = {"key": key}

    response = requests.post(url, data=data)
    return response.json()


def get_sessions_info():
    url = f"{DOMAIN}get-all-sessions"

    response = requests.get(url)
    return response.json()


def get_session_info(session_id):
    url = f"{DOMAIN}get-session-by-id/{session_id}"

    response = requests.get(url)
    return response.text


def upload_session_files(session_file_path, json_file_path):
    url = f"{DOMAIN}upload-session-from-bot"
    with open(session_file_path, "rb") as session_file, open(
        json_file_path, "rb"
    ) as json_file:
        files = [
            (
                "session_files",
                (
                    session_file_path.split("/")[-1],
                    session_file,
                    "application/octet-stream",
                ),
            ),
            (
                "session_files",
                (json_file_path.split("/")[-1], json_file, "application/json"),
            ),
        ]
        response = requests.post(url, files=files, allow_redirects=True)

    return response.json()


def open_session_privacy(session_id):
    url = f"{DOMAIN}open-privacy"
    data = {"session_id": session_id}

    response = requests.post(url, data=data)
    return response.json()


def upload_avatar(session_id: str, avatar_path: str) -> dict:
    url = f"{DOMAIN}upload-avatar-api/{session_id}"

    with open(avatar_path, "rb") as f:
        files = {"avatar": (avatar_path, f, "image/jpeg")}
        response = requests.post(url, files=files)

    return response.json()


def update_first_name(session_id: str, new_name: str) -> dict:
    url = f"{DOMAIN}change-name"

    data = {"session_id": session_id, "first_name": new_name}
    response = requests.post(url, data=data)

    return json.loads(response.text)


def update_surname(session_id: str, new_surname: str) -> dict:
    url = f"{DOMAIN}change-surname"

    data = {"session_id": session_id, "surname": new_surname}
    response = requests.post(url, data=data)

    return json.loads(response.text)


def update_username(session_id: str, new_username: str) -> dict:
    url = f"{DOMAIN}change-username"

    data = {"session_id": session_id, "username": new_username}
    response = requests.post(url, data=data)

    return json.loads(response.text)


# if __name__ == "__main__":
#     print(get_session_info(1))
