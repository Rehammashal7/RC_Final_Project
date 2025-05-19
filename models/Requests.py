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

def save_request_to_json(adoption_request):
    try:
        with open("data/requests.json", "r") as f:
            existing = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []

    existing.append(adoption_request.to_dict())

    with open("data/requests.json", "w") as f:
        json.dump(existing, f, indent=2)

