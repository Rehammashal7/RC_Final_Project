import json
import os

class Entity:
    file_path = ""  # Must be set by subclasses

    def save(self):
        records = []
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                try:
                    records = json.load(f)
                except json.JSONDecodeError:
                    pass

        records.append(self.to_dict())

        with open(self.file_path, "w") as f:
            json.dump(records, f, indent=2)

    @classmethod
    def get_next_id(cls):
        if not os.path.exists(cls.file_path):
            return 1
        with open(cls.file_path, "r") as f:
            try:
                records = json.load(f)
                if not records:
                    return 1
                return max(record["id"] for record in records) + 1
            except json.JSONDecodeError:
                return 1
    @staticmethod
    def manual_hash(password):
        salt = "xyz123"
        return (password[::-1] + salt).upper()

    @staticmethod
    def verify_password(input_password, stored_password):
        return stored_password == Entity.manual_hash(input_password)
