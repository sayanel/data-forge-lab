import unittest
from uuid import uuid4
from unittest.mock import MagicMock
from application.domain.services.habit_event_service import HabitEventService
from application.domain.models.event import HabitEvent
from infrastructure.persistence.in_memory import InMemoryHabitEventRepository
from datetime import datetime, timedelta
from application.domain.models.habit import Habit


class TestHabitEventService(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryHabitEventRepository()
        self.publisher = MagicMock()
        self.service = HabitEventService(habit_event_repo=self.repo, event_publisher=self.publisher)

    def test_create_habit_event(self):
        person_id = uuid4()
        habit_id = uuid4()
        event = self.service.create_habit_event(person_id, habit_id, notes="Did yoga")
        self.assertEqual(event.person_id, person_id)
        self.assertEqual(event.habit_id, habit_id)
        self.assertEqual(event.notes, "Did yoga")

    def test_update_habit_event(self):
        person_id = uuid4()
        habit_id = uuid4()
        event = self.service.create_habit_event(person_id, habit_id, notes="A")
        updated = self.service.update_habit_event(event.event_id, notes="B")
        self.assertEqual(updated.notes, "B")

    def test_list_habit_events(self):
        person_id = uuid4()
        habit_id = uuid4()
        self.service.create_habit_event(person_id, habit_id, notes="1")
        self.service.create_habit_event(person_id, habit_id, notes="2")
        events = self.service.list_habit_events(habit_id)
        self.assertEqual(len(events), 2)

    def test_delete_habit_event(self):
        person_id = uuid4()
        habit_id = uuid4()
        event = self.service.create_habit_event(person_id, habit_id, notes="X")
        deleted = self.service.delete_habit_event(event.event_id)
        self.assertTrue(deleted)
        self.assertIsNone(self.service.get_habit_event(event.event_id))

    def test_streak_logic(self):
        # Setup mock habit_repo and inject into service
        mock_habit_repo = MagicMock()
        person_id = uuid4()
        habit_id = uuid4()
        habit = Habit(person_id=person_id, name="Test", goal="Daily", category="Health", habit_id=habit_id)
        mock_habit_repo.get_by_id.return_value = habit
        mock_habit_repo.save.side_effect = lambda h: h

        service = HabitEventService(habit_event_repo=self.repo, event_publisher=self.publisher, habit_repo=mock_habit_repo)

        # Day 1: first completion
        event1 = HabitEvent(person_id=person_id, habit_id=habit_id, notes="Day 1", status="completed", timestamp=datetime(2024, 1, 1, 10, 0, 0))
        self.repo.save(event1)
        service.create_habit_event(person_id, habit_id, notes="Day 1")
        habit.last_completed = event1.timestamp
        habit.streak = 1

        # Day 2: consecutive completion
        event2 = HabitEvent(person_id=person_id, habit_id=habit_id, notes="Day 2", status="completed", timestamp=datetime(2024, 1, 2, 10, 0, 0))
        self.repo.save(event2)
        service.create_habit_event(person_id, habit_id, notes="Day 2")
        habit.last_completed = event2.timestamp
        habit.streak += 1
        self.assertEqual(habit.streak, 2)

        # Day 4: skip a day, streak should reset
        event3 = HabitEvent(person_id=person_id, habit_id=habit_id, notes="Day 4", status="completed", timestamp=datetime(2024, 1, 4, 10, 0, 0))
        self.repo.save(event3)
        service.create_habit_event(person_id, habit_id, notes="Day 4")
        habit.last_completed = event3.timestamp
        habit.streak = 1
        self.assertEqual(habit.streak, 1) 