from abc import ABC, abstractmethod
from application.domain.models.event import HabitEventCreatedMessage


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: HabitEventCreatedMessage) -> None:
        pass
