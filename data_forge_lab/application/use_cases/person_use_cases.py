from uuid import UUID
from datetime import date
from typing import Optional
from application.domain.models.person import Country

from application.domain.services.person_service import PersonService


class PersonUseCases:
    def __init__(self, person_service: PersonService):
        self.person_service = person_service

    def create_person(self, first_name: str, last_name: str, date_of_birth: date, email: str, phone_number: str, address: str, country: Country, gender: Optional[str] = None, notification_preferences: Optional[dict] = None, language_preference: str = "English"):
        return self.person_service.create_person(first_name, last_name, date_of_birth, email, phone_number, address, country, gender, notification_preferences, language_preference)

    def update_person(self, person_id: UUID, **kwargs):
        return self.person_service.update_person(person_id, **kwargs)

    def get_person(self, person_id: UUID):
        return self.person_service.get_person(person_id)

    def list_persons(self):
        return self.person_service.list_persons()

    def delete_person(self, person_id: UUID):
        return self.person_service.delete_person(person_id)
