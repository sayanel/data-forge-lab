from uuid import UUID
from application.domain.services.habit_event_service import HabitEventService


class HabitEventUseCases:
    def __init__(self, habit_event_service: HabitEventService):
        self.habit_event_service = habit_event_service

    def create_habit_event(self, person_id: UUID, habit_id: UUID, notes: str):
        return self.habit_event_service.create_habit_event(person_id, habit_id, notes)

    def update_habit_event(self, event_id: UUID, **kwargs):
        return self.habit_event_service.update_habit_event(event_id, **kwargs)

    def get_habit_event(self, event_id: UUID):
        return self.habit_event_service.get_habit_event(event_id)

    def list_habit_events(self, habit_id: UUID):
        return self.habit_event_service.list_habit_events(habit_id)

    def delete_habit_event(self, event_id: UUID):
        return self.habit_event_service.delete_habit_event(event_id)
