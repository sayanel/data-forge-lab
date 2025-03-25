from datetime import date
from typing import List, Optional
from domain.models.person import Person
from interfaces.repositories.person_repository import PersonRepository
from uuid import UUID, uuid4


class PersonService:
    def __init__(self, person_repo: PersonRepository):
        self.person_repo = person_repo

    def create_person(self, first_name: str, last_name: str, date_of_birth: date, email: str, phone_number: str, address: str, person_id: Optional[UUID] = uuid4, gender: Optional[str] = None, notification_preferences: Optional[dict] = None, language_preference: str = "English") -> Person:
        person = Person(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            email=email,
            phone_number=phone_number,
            address=address,
            gender=gender,
            person_id=person_id,
            notification_preferences=notification_preferences or {},
            language_preference=language_preference
        )
        return self.person_repo.save(person)

    def update_person(self, person_id: UUID, **kwargs) -> Optional[Person]:
        person = self.person_repo.get_by_id(person_id)
        if not person:
            return None
        person.update_details(**kwargs)
        return self.person_repo.save(person)

    def get_person(self, person_id: UUID) -> Optional[Person]:
        return self.person_repo.get_by_id(person_id)

    def list_persons(self) -> List[Person]:
        return self.person_repo.find_all()

    def delete_person(self, person_id: UUID) -> bool:
        return self.person_repo.delete(person_id)
