import json
import os

from datetime import datetime
class AdoptionRequest:
    def __init__(self, user_id, pet_id, email, shelter_id):
        self.user_id = user_id
        self.pet_id = pet_id
        self.email = email
        self.shelter_id = shelter_id
        self.timestamp = datetime.utcnow().isoformat()
        self.days_since = "0 days ago"
        self.status = "Pending"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "pet_id": self.pet_id,
            "email": self.email,
            "shelter_id": self.shelter_id,
            "timestamp": self.timestamp,
            "days_since": self.days_since,
            "status": self.status
        }

def save_request_to_json(request_obj, filename=None):
    if filename is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = os.path.join(base_dir, "data", "requests.json")

    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)

    with open(filename, "r+") as f:
        data = json.load(f)
        data.append(request_obj.to_dict())
        f.seek(0)
        json.dump(data, f, indent=4)

