from uuid import UUID
from typing import List, Optional
from application.domain.models.event import HabitEvent
from interfaces.repositories.habit_event_repository import HabitEventRepository


class HabitEventService:
    def __init__(self, habit_event_repo: HabitEventRepository):
        self.habit_event_repo = habit_event_repo

    def create_habit_event(self, person_id: UUID, habit_id: UUID, notes: Optional[str] = None) -> HabitEvent:
        event = HabitEvent(person_id=person_id, habit_id=habit_id, notes=notes)
        return self.habit_event_repo.save(event)

    def update_habit_event(self, event_id: UUID, **kwargs) -> Optional[HabitEvent]:
        event = self.habit_event_repo.get_by_id(event_id)
        if not event:
            return None
        for key, value in kwargs.items():
            if hasattr(event, key):
                setattr(event, key, value)
        return self.habit_event_repo.save(event)

    def get_habit_event(self, event_id: UUID) -> Optional[HabitEvent]:
        return self.habit_event_repo.get_by_id(event_id)

    def list_habit_events(self, habit_id: UUID) -> List[HabitEvent]:
        return self.habit_event_repo.find_by_habit_id(habit_id)

    def delete_habit_event(self, event_id: UUID) -> bool:
        return self.habit_event_repo.delete(event_id)
