from abc import ABC, abstractmethod
from typing import List, Optional
from application.domain.models.person import Person
from uuid import UUID


class PersonRepository(ABC):
    @abstractmethod
    def save(self, person: Person) -> Person:
        pass

    @abstractmethod
    def get_by_id(self, person_id: UUID) -> Optional[Person]:
        pass

    @abstractmethod
    def find_all(self) -> List[Person]:
        pass

    @abstractmethod
    def delete(self, person_id: UUID) -> bool:
        pass
