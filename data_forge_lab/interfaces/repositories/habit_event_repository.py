from abc import ABC, abstractmethod
from typing import List, Optional
from application.domain.models.event import HabitEvent
from uuid import UUID


class HabitEventRepository(ABC):
    @abstractmethod
    def save(self, event: HabitEvent) -> HabitEvent:
        pass

    @abstractmethod
    def get_by_id(self, event_id: UUID) -> Optional[HabitEvent]:
        pass

    @abstractmethod
    def find_all(self) -> List[HabitEvent]:
        pass

    @abstractmethod
    def find_by_habit_id(self, habit_id: UUID) -> List[HabitEvent]:
        pass

    @abstractmethod
    def delete(self, event_id: UUID) -> bool:
        pass

    @abstractmethod
    def find_by_person_id(self, person_id: UUID) -> List[HabitEvent]:
        pass
