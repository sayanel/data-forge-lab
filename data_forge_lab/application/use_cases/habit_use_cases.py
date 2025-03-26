from uuid import UUID
from domain.services.habit_service import HabitService
from interfaces.repositories.habit_repository import HabitRepository
from interfaces.repositories.habit_event_repository import HabitEventRepository


class HabitUseCases:
    def __init__(self, habit_service: HabitService):
        self.habit_service = habit_service

    def create_habit(self, person_id: UUID, name: str, goal: str, category: str):
        return self.habit_service.create_habit(person_id, name, goal, category)

    def update_habit(self, habit_id: UUID, **kwargs):
        return self.habit_service.update_habit(habit_id, **kwargs)

    def get_habit(self, habit_id: UUID):
        return self.habit_service.get_habit(habit_id)

    def list_habits(self, person_id: UUID):
        return self.habit_service.list_habits(person_id)

    def delete_habit(self, habit_id: UUID):
        return self.habit_service.delete_habit(habit_id)
