from models.entity import Entity

class Shelter(Entity):
    file_path = "shelters.json"

    def __init__(self, name, email, raw_password):
        if len(raw_password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        self.id = self.get_next_id()
        self.name = name
        self.email = email
        self.password = self.manual_hash(raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
