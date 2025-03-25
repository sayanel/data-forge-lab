from uuid import UUID
from typing import List, Optional

from domain.models.person import Person
from domain.models.habit import Habit
from domain.models.event import HabitEvent

from interfaces.repositories.person_repository import PersonRepository
from interfaces.repositories.event_repository import HabitEventRepository
from interfaces.repositories.habit_repository import HabitRepository


Database = None


class PersonRepositoryImpl(PersonRepository):
    def __init__(self):
        self.storage = {}

    def save(self, person: Person) -> Person:
        self.storage[person.person_id] = person
        print(f"self.storage: {self.storage}")
        return person

    def get_by_id(self, person_id: UUID) -> Optional[Person]:
        return self.storage.get(person_id)

    def find_all(self) -> List[Person]:
        return list(self.storage.values())

    def delete(self, person_id: UUID) -> bool:
        # Delete the person by ID and return True if successful, False otherwise
        if person_id in self.storage:
            del self.storage[person_id]
            return True
        return False


class HabitEventRepositoryImpl(HabitEventRepository):
    def __init__(self):
        self.storage = {}

    def save(self, event: HabitEvent) -> HabitEvent:
        self.storage[event.event_id] = event
        print(f"self.storage: {self.storage}")
        return event

    def get_by_id(self, event_id: UUID) -> Optional[HabitEvent]:
        return self.storage.get(event_id)

    def find_all(self) -> List[HabitEvent]:
        return list(self.storage.values())

    def find_by_habit_id(self, habit_id: UUID) -> List[HabitEvent]:
        return [event for event in self.storage.values() if event.habit_id == habit_id]

    def delete(self, event_id: UUID) -> bool:
        if event_id in self.storage:
            del self.storage[event_id]
            return True
        return False


class HabitRepositoryImpl(HabitRepository):
    def __init__(self):
        self.storage = {}

    def save(self, habit: Habit) -> Habit:
        self.storage[habit.habit_id] = habit
        print(f"self.storage: {self.storage}")
        return habit

    def get_by_id(self, habit_id: UUID) -> Optional[Habit]:
        return self.storage.get(habit_id)

    def find_all(self) -> List[Habit]:
        return list(self.storage.values())

    def find_by_person_id(self, person_id: UUID) -> List[Habit]:
        return [habit for habit in self.storage.values() if habit.person_id == person_id]

    def delete(self, habit_id: UUID) -> bool:
        if habit_id in self.storage:
            del self.storage[habit_id]
            return True
        return False
