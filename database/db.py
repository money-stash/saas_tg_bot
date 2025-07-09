class Database:
    def user_exists(self, data: dict, user_id: str) -> bool:
        for user in data.get("users", []):
            if str(user.get("user_id")) == str(user_id):
                return True

        return False


db = Database()
