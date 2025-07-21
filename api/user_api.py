import json
import aiohttp
import asyncio

DOMAIN = "http://localhost:5555/"


async def add_new_user(user_id, username, key):
    url = f"{DOMAIN}add-user"
    data = {"user_id": user_id, "username": username, "key": key}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            print("Response:", await response.json())


async def update_add_new_user(user_id, username, key):
    url = f"{DOMAIN}update-user-login"
    data = {"user_id": user_id, "username": username, "key": key}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            print("Response:", await response.json())


async def get_users():
    url = f"{DOMAIN}users"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_key_info(key):
    url = f"{DOMAIN}get_key_info"
    data = {"key": key}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.json()


async def get_sessions_info():
    url = f"{DOMAIN}get-all-sessions"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_session_info(session_id):
    url = f"{DOMAIN}get-session-by-id/{session_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_all_reports():
    url = f"{DOMAIN}all-reports"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            answer = await response.text()
            json_answer = json.loads(answer)
            return json_answer["reports"]


async def upload_session_files(session_file_path, json_file_path):
    url = f"{DOMAIN}upload-session-from-bot"
    async with aiohttp.ClientSession() as session:
        with open(session_file_path, "rb") as session_file, open(
            json_file_path, "rb"
        ) as json_file:
            data = aiohttp.FormData()
            data.add_field(
                "session_files",
                session_file,
                filename=session_file_path.split("/")[-1],
                content_type="application/octet-stream",
            )
            data.add_field(
                "session_files",
                json_file,
                filename=json_file_path.split("/")[-1],
                content_type="application/json",
            )
            async with session.post(url, data=data, allow_redirects=True) as response:
                return await response.json()


async def open_session_privacy(session_id):
    url = f"{DOMAIN}open-privacy"
    data = {"session_id": session_id}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            return await response.json()


async def upload_avatar(session_id: str, avatar_path: str) -> dict:
    url = f"{DOMAIN}upload-avatar-api/{session_id}"
    async with aiohttp.ClientSession() as session:
        with open(avatar_path, "rb") as f:
            data = aiohttp.FormData()
            data.add_field("avatar", f, filename=avatar_path, content_type="image/jpeg")
            async with session.post(url, data=data) as response:
                return await response.json()


async def update_first_name(session_id: str, new_name: str) -> dict:
    url = f"{DOMAIN}change-name"
    data = {"session_id": session_id, "first_name": new_name}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            text = await response.text()
            return json.loads(text)


async def update_surname(session_id: str, new_surname: str) -> dict:
    url = f"{DOMAIN}change-surname"
    data = {"session_id": session_id, "surname": new_surname}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            text = await response.text()
            return json.loads(text)


async def update_username(session_id: str, new_username: str) -> dict:
    url = f"{DOMAIN}change-username"
    data = {"session_id": session_id, "username": new_username}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            text = await response.text()
            return json.loads(text)


async def create_parse_task(group_identifier, worker_id) -> dict:
    url = f"{DOMAIN}create-parse-task"
    data = {"group_identifier": group_identifier, "worker_id": worker_id}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            text = await response.text()
            return json.loads(text)


async def get_report_info(report_id) -> dict:
    url = f"{DOMAIN}get_report"
    data = {"report_id": report_id}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            text = await response.text()
            return json.loads(text)


async def download_report_file(path: str, save_as: str) -> bool:
    url = f"{DOMAIN}download-report"
    payload = {"path": path}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                with open(save_as, "wb") as f:
                    f.write(await response.read())
                return save_as
            else:
                print("Ошибка загрузки:", await response.text())
                return False


# if __name__ == "__main__":
#     print(get_session_info(1))
