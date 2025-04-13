# data_forge_lab/infrastructure/persistence/mongodb/habit.py

from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pymongo.collection import Collection

from domain.models.habit import Habit
from interfaces.repositories.habit_repository import HabitRepository


class MongoHabitRepository(HabitRepository):
    def __init__(self, collection: Collection):
        self.collection = collection

    def save(self, habit: Habit) -> Habit:
        habit_dict = habit.to_dict()

        self.collection.update_one(
            {"habit_id": str(habit.habit_id)},
            {"$set": habit_dict},
            upsert=True
        )
        return habit

    def get_by_id(self, habit_id: UUID) -> Optional[Habit]:
        doc = self.collection.find_one({"habit_id": str(habit_id)})
        return self._from_dict(doc) if doc else None

    def find_all(self) -> List[Habit]:
        docs = self.collection.find()
        return [self._from_dict(doc) for doc in docs]

    def find_by_person_id(self, person_id: UUID) -> List[Habit]:
        docs = self.collection.find({"person_id": str(person_id)})
        return [self._from_dict(doc) for doc in docs]

    def delete(self, habit_id: UUID) -> bool:
        result = self.collection.delete_one({"habit_id": str(habit_id)})
        return result.deleted_count > 0

    def _from_dict(self, data: dict) -> Habit:
        return Habit(
            habit_id=UUID(data["habit_id"]),
            person_id=UUID(data["person_id"]),
            name=data["name"],
            goal=data["goal"],
            category=data["category"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else None,
            streak=data.get("streak", 0),
            last_completed=datetime.fromisoformat(data["last_completed"]) if data.get("last_completed") else None
        )
