import requests


def add_new_user():
    url = "http://localhost:5555/print-user"
    data = {"user_id": 123, "username": "test_user", "key": "abc123xyz"}

    response = requests.post(url, data=data)
    print("Status code:", response.status_code)
    print("Response:", response.json())


def get_users():
    url = "http://localhost:5555/users"

    response = requests.get(url)
    print("Status code:", response.status_code)
    return response.json()


if __name__ == "__main__":
    # add_new_user()
    get_users()
