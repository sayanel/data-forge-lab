from uuid import UUID
from typing import List, Optional
from domain.models.event import HabitEvent
from interfaces.repositories.event_repository import HabitEventRepository


class HabitEventService:
    def __init__(self, event_repo: HabitEventRepository):
        self.event_repo = event_repo

    def log_event(self, person_id: UUID, habit_id: UUID, notes: Optional[str] = None) -> HabitEvent:
        event = HabitEvent(person_id=person_id, habit_id=habit_id, notes=notes)
        return self.event_repo.save(event)

    def update_event(self, event_id: UUID, **kwargs) -> Optional[HabitEvent]:
        event = self.event_repo.get_by_id(event_id)
        if not event:
            return None
        for key, value in kwargs.items():
            if hasattr(event, key):
                setattr(event, key, value)
        return self.event_repo.save(event)

    def get_event(self, event_id: UUID) -> Optional[HabitEvent]:
        return self.event_repo.get_by_id(event_id)

    def list_events(self, habit_id: UUID) -> List[HabitEvent]:
        return self.event_repo.find_by_habit_id(habit_id)

    def delete_event(self, event_id: UUID) -> bool:
        return self.event_repo.delete(event_id)
