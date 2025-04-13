from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


habit_categories = {
    "Health": ["Exercise", "Hydration", "Sleep", "Meditation", "Healthy Eating"],
    "Personal Development": ["Reading", "Learning a Skill", "Journaling", "Language Learning"],
    "Productivity": ["Time Management", "Planning", "Organization"],
    "Social": ["Connect with Friends", "Volunteering", "Networking"],
    "Financial": ["Saving Money", "Budgeting", "Investing"]
}


@dataclass
class Habit:
    person_id: UUID
    name: str
    goal: str
    category: str
    habit_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    streak: int = 0
    last_completed: Optional[datetime] = None

    def complete(self):
        self.streak += 1
        self.last_completed = datetime.now()
        self.updated_at = datetime.now()

    def miss(self):
        self.streak = 0
        self.updated_at = datetime.now()

    def update_goal(self, new_goal: str):
        self.goal = new_goal
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "habit_id": str(self.habit_id),
            "person_id": str(self.person_id),
            "name": self.name,
            "goal": self.goal,
            "category": self.category,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "streak": self.streak,
            "last_completed": self.last_completed.isoformat() if self.last_completed else None
        }
