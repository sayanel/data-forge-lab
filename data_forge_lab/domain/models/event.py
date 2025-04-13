from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


@dataclass
class HabitEvent:
    person_id: UUID
    habit_id: UUID
    event_id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
    notes: Optional[str] = None
    status: str = "pending"  # Status can be "pending", "completed", "missed"

    def complete(self):
        """Mark the habit event as completed."""
        self.status = "completed"

    def miss(self):
        """Mark the habit event as missed."""
        self.status = "missed"

    def update_notes(self, new_notes: str):
        """Update the notes for the habit event."""
        self.notes = new_notes

    def to_dict(self):
        return {
            "event_id": str(self.event_id),
            "person_id": str(self.person_id),
            "habit_id": str(self.habit_id),
            "timestamp": self.timestamp.isoformat(),
            "notes": self.notes,
            "status": self.status
        }
