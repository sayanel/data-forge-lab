from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Optional
from application.domain.models.habit import Habit
from interfaces.repositories.habit_repository import HabitRepository


class HabitService:
    def __init__(self, habit_repo: HabitRepository):
        self.habit_repo = habit_repo

    def create_habit(self, person_id: UUID, name: str, goal: str, category: str, habit_id: Optional[UUID] = None) -> Habit:
        if not habit_id:
            habit_id = uuid4()
            
        habit = Habit(person_id=person_id, name=name, goal=goal, category=category, habit_id=habit_id)
        return self.habit_repo.save(habit)

    def update_habit(self, habit_id: UUID, **kwargs) -> Optional[Habit]:
        habit = self.habit_repo.get_by_id(habit_id)
        if not habit:
            return None
        for key, value in kwargs.items():
            if hasattr(habit, key):
                setattr(habit, key, value)
        habit.updated_at = datetime.now()
        return self.habit_repo.save(habit)

    def get_habit(self, habit_id: UUID) -> Optional[Habit]:
        return self.habit_repo.get_by_id(habit_id)

    def list_habits(self, person_id: UUID) -> List[Habit]:
        return self.habit_repo.find_by_person_id(person_id)

    def delete_habit(self, habit_id: UUID) -> bool:
        return self.habit_repo.delete(habit_id)
