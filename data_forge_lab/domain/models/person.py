from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Person:
    first_name: str
    last_name: str
    date_of_birth: date
    email: str
    phone_number: str
    address: str
    gender: str = None
    person_id: UUID = field(default_factory=uuid4)
    notification_preferences: dict = field(default_factory=dict)
    language_preference: str = "English"
    creation_date: date = field(default_factory=date.today)
    last_updated: date = field(default_factory=date.today)

    def update_details(self, **kwargs):
        print(f"update_details: {kwargs}")
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.last_updated = date.today()

    def __post_init__(self):
        if not isinstance(self.person_id, UUID):
            self.person_id = UUID(str(self.person_id))

    def to_dict(self):
        # Convert the object to a dictionary, excluding any non-serializable attributes
        return {
            "person_id": str(self.person_id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth.isoformat(),  # Ensure date is in ISO format
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "gender": self.gender,
            "language_preference": self.language_preference,
            "creation_date": self.creation_date.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }

    def to_creation_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "gender": self.gender,
            "notification_preferences": self.notification_preferences,
            "language_preference": self.language_preference,
            "person_id": str(self.person_id),
        }
