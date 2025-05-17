from uuid import UUID
from typing import List, Optional
from application.domain.models.event import HabitEvent, HabitEventCreatedMessage
from interfaces.repositories.habit_event_repository import HabitEventRepository
from interfaces.event_publisher import EventPublisher


class HabitEventService:
    def __init__(self, habit_event_repo: HabitEventRepository, event_publisher: EventPublisher, habit_repo=None):
        self.habit_event_repo = habit_event_repo
        self.event_publisher = event_publisher
        self.habit_repo = habit_repo

    def create_habit_event(self, person_id: UUID, habit_id: UUID, notes: Optional[str] = None) -> HabitEvent:
        event = HabitEvent(person_id=person_id, habit_id=habit_id, notes=notes, status="completed")
        saved = self.habit_event_repo.save(event)

        # Streak logic
        if self.habit_repo:
            habit = self.habit_repo.get_by_id(habit_id)
            if habit:
                # Only update streak if event is completed
                if getattr(event, 'status', None) == 'completed':
                    from datetime import datetime, timedelta
                    today = event.timestamp.date()
                    last_completed = habit.last_completed.date() if habit.last_completed else None
                    if last_completed and (today - last_completed).days == 1:
                        habit.streak += 1
                    else:
                        habit.streak = 1
                    habit.last_completed = event.timestamp
                    habit.updated_at = datetime.now()
                    self.habit_repo.save(habit)

        self.event_publisher.publish(saved.to_event_created())  # Emit event

        return saved

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
