from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.habit import Habit
from uuid import UUID


class HabitRepository(ABC):
    @abstractmethod
    def save(self, habit: Habit) -> Habit:
        pass

    @abstractmethod
    def get_by_id(self, habit_id: UUID) -> Optional[Habit]:
        pass

    @abstractmethod
    def find_all(self) -> List[Habit]:
        pass

    @abstractmethod
    def find_by_person_id(self, person_id: UUID) -> List[Habit]:
        pass

    @abstractmethod
    def delete(self, habit_id: UUID) -> bool:
        pass
