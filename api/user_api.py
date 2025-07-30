import os
import json
import aiohttp
import asyncio

from config import DOMAIN


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
    url = f"{DOMAIN}reports"

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


async def update_bio(session_id: str, new_bio: str) -> dict:
    url = f"{DOMAIN}change-bio"
    data = {"session_id": session_id, "bio": new_bio}
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


async def create_spam_task(dataset_path, worker_id, messages_count, msg_text):
    url = f"{DOMAIN}start-spam"
    payload = {
        "users_path": dataset_path,
        "worker_id": worker_id,
        "messages_count": messages_count,
        "msg_text": msg_text,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            text = await response.text()
            return json.loads(text)


async def delete_session_api(session_id):
    url = f"{DOMAIN}delete-session"
    payload = {
        "session_id": session_id,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as response:
            return True


async def get_all_links():
    url = f"{DOMAIN}links"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def delete_link(link_id: int):
    url = f"{DOMAIN}delete-link/{link_id}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={"link_id": link_id}) as resp:
            return await resp.json()

async def add_link(link: str, link_name: str):
    url = f"{DOMAIN}add-link"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={"link": link, "spam_text": False, "link_name": link_name}) as resp:
            return await resp.json()

async def get_link(link_id: int):
    url = f"{DOMAIN}get-link"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={"link_id": link_id}) as resp:
            return await resp.json()


async def check_link(link: str):
    url = f"{DOMAIN}check-link"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={"link": link}) as resp:
            return await resp.json()


async def update_status(link_id: int, status: bool):
    url = f"{DOMAIN}update-status"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={"link_id": link_id, "status": str(status)}) as resp:
            return await resp.json()


async def upload_file_to_link(file_path: str, link_id: int):
    url = f"{DOMAIN}upload-file"
    if not os.path.isfile(file_path):
        return {"success": False, "error": "Файл не найден"}

    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            form = aiohttp.FormData()
            form.add_field("file", f, filename=os.path.basename(file_path), content_type="text/plain")
            form.add_field("link_id", str(link_id))

            async with session.post(url, data=form) as resp:
                return await resp.json()


async def main():
    print(await check_link("oko_ua"))


# if __name__ == "__main__":
#     asyncio.run(main())
