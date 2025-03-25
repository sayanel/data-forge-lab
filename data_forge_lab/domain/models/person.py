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
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.last_updated = date.today()

