from uuid import UUID
from domain.services.event_service import HabitEventService
from interfaces.repositories.event_repository import HabitEventRepository


class HabitEventUseCases:
    def __init__(self, event_service: HabitEventService):
        self.event_service = event_service

    def log_event(self, person_id: UUID, habit_id: UUID, notes: str):
        return self.event_service.log_event(person_id, habit_id, notes)

    def update_event(self, event_id: UUID, **kwargs):
        return self.event_service.update_event(event_id, **kwargs)

    def get_event(self, event_id: UUID):
        return self.event_service.get_event(event_id)

    def list_events(self, habit_id: UUID):
        return self.event_service.list_events(habit_id)

    def delete_event(self, event_id: UUID):
        return self.event_service.delete_event(event_id)
