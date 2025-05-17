import json
import os

class User:
    def __init__(self, username, email, raw_password):
        if len(raw_password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        
        self.id = self.get_next_id()
        self.username = username
        self.email = email
        self.password = self.manual_hash(raw_password)

    def manual_hash(self, password):
        salt = "xyz123"
        return (password[::-1] + salt).upper()

    def verify_password(self, input_password):
        return self.password == self.manual_hash(input_password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    def save(self):
        users = []
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    pass

        users.append(self.to_dict())

        with open("users.json", "w") as f:
            json.dump(users, f, indent=2)

    @staticmethod
    def get_next_id():
        if not os.path.exists("users.json"):
            return 1
        with open("users.json", "r") as f:
            try:
                users = json.load(f)
                if not users:
                    return 1
                return max(user["id"] for user in users) + 1
            except json.JSONDecodeError:
                return 1
