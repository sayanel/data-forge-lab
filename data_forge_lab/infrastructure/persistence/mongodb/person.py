import uuid
from uuid import UUID
from bson import ObjectId
from datetime import date, datetime
from typing import List, Optional

from pymongo.collection import Collection

from application.domain.models.person import Person
from interfaces.repositories.person_repository import PersonRepository


class MongoPersonRepository(PersonRepository):
    def __init__(self, collection: Collection):
        self.collection = collection

    def save(self, person: Person) -> Person:
        print(f"Person: {person} - {type(person)}")
        person_dict = person.to_dict()
        person_dict["person_id"] = str(person.person_id)
        print(f"person_dict: {person_dict}")
        person_dict["creation_date"] = person.creation_date.isoformat()
        person_dict["last_updated"] = person.last_updated.isoformat()

        existing = self.collection.find_one({"person_id": str(person.person_id)})
        if existing:
            self.collection.replace_one({"person_id": str(person.person_id)}, person_dict)
        else:
            self.collection.insert_one(person_dict)

        return person

    def get_by_id(self, person_id: UUID) -> Optional[Person]:
        doc = self.collection.find_one({"person_id": str(person_id)})

        if doc:
            return self._from_dict(doc)

        raise ValueError(f"Person with ID {person_id} not found.")

    def find_all(self) -> List[Person]:
        persons = []
        for doc in self.collection.find():
            persons.append(self._from_dict(doc))
        return persons

    def delete(self, person_id: UUID) -> bool:
        result = self.collection.delete_one({"person_id": str(person_id)})
        return result.deleted_count > 0

    def _from_dict(self, data: dict) -> Person:
        return Person(
            person_id=UUID(data["person_id"]),
            first_name=data["first_name"],
            last_name=data["last_name"],
            date_of_birth=date.fromisoformat(data["date_of_birth"]),
            email=data["email"],
            phone_number=data["phone_number"],
            address=data["address"],
            gender=data.get("gender"),
            notification_preferences=data.get("notification_preferences", {}),
            language_preference=data.get("language_preference", "English"),
            creation_date=date.fromisoformat(data.get("creation_date", date.today().isoformat())),
            last_updated=date.fromisoformat(data.get("last_updated", date.today().isoformat())),
        )
