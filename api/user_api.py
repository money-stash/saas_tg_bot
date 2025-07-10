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


# if __name__ == "__main__":
#     add_new_user()
#     get_users()
