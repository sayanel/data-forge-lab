from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pymongo.collection import Collection

from application.domain.models.event import HabitEvent
from interfaces.repositories.habit_event_repository import HabitEventRepository


class MongoHabitEventRepository(HabitEventRepository):
    def __init__(self, collection: Collection):
        self.collection = collection

    def save(self, event: HabitEvent) -> HabitEvent:
        event_dict = event.to_dict()
        self.collection.update_one(
            {"event_id": str(event.event_id)},
            {"$set": event_dict},
            upsert=True
        )
        return event

    def get_by_id(self, event_id: UUID) -> Optional[HabitEvent]:
        doc = self.collection.find_one({"event_id": str(event_id)})
        return self._from_dict(doc) if doc else None

    def find_all(self) -> List[HabitEvent]:
        docs = self.collection.find()
        return [self._from_dict(doc) for doc in docs]

    def find_by_habit_id(self, habit_id: UUID) -> List[HabitEvent]:
        docs = self.collection.find({"habit_id": str(habit_id)})
        return [self._from_dict(doc) for doc in docs]

    def delete(self, event_id: UUID) -> bool:
        result = self.collection.delete_one({"event_id": str(event_id)})
        return result.deleted_count > 0

    def _from_dict(self, data: dict) -> HabitEvent:
        return HabitEvent(
            event_id=UUID(data["event_id"]),
            person_id=UUID(data["person_id"]),
            habit_id=UUID(data["habit_id"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            notes=data.get("notes"),
            status=data["status"]
        )
