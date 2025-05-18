from models.entity import Entity

class User(Entity):
    file_path = "../data/users.json"

    def __init__(self, username, email, raw_password):
        if len(raw_password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        self.id = self.get_next_id()
        self.username = username
        self.email = email
        self.password = self.manual_hash(raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
