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
        # Configure the mock to return the same habit object on get_by_id
        mock_habit_repo.get_by_id.return_value = habit
        # Configure the mock to simply return the habit object passed to save
        mock_habit_repo.save.side_effect = lambda h: h

        service = HabitEventService(habit_event_repo=self.repo, event_publisher=self.publisher, habit_repo=mock_habit_repo)

        # Day 1: first completion
        event1_timestamp = datetime(2024, 1, 1, 10, 0, 0)
        with unittest.mock.patch('application.domain.services.habit_event_service.datetime') as mock_dt:
            mock_dt.now.return_value = event1_timestamp
            mock_dt.date.today.return_value = event1_timestamp.date()
            service.create_habit_event(person_id, habit_id, notes="Day 1", timestamp=event1_timestamp)

            # Check if habit_repo.save was called and get the habit object that was passed
            mock_habit_repo.save.assert_called_once()
            saved_habit_day1 = mock_habit_repo.save.call_args[0][0]  # Get the first argument of the first call

            # Assert that the service updated the habit
            self.assertEqual(1, saved_habit_day1.streak)
            # Compare dates, as time might differ slightly or be set to start of day in service
            self.assertEqual(saved_habit_day1.last_completed.date(), event1_timestamp.date())

        # Day 2: consecutive completion
        event2_timestamp = datetime(2024, 1, 2, 10, 0, 0)
        with unittest.mock.patch('application.domain.services.habit_event_service.datetime') as mock_dt:
            mock_dt.now.return_value = event2_timestamp
            mock_dt.date.today.return_value = event2_timestamp.date()
            service.create_habit_event(person_id, habit_id, notes="Day 2", timestamp=event2_timestamp)

            mock_habit_repo.save.assert_called_with(habit)
            saved_habit_day2 = mock_habit_repo.save.call_args[0][0]

            self.assertEqual(2, saved_habit_day2.streak)
            self.assertEqual(saved_habit_day2.last_completed.date(), event2_timestamp.date())

        # Day 3: consecutive completion
        event3_timestamp = datetime(2024, 1, 3, 10, 0, 0)
        with unittest.mock.patch('application.domain.services.habit_event_service.datetime') as mock_dt:
            mock_dt.now.return_value = event3_timestamp
            mock_dt.date.today.return_value = event3_timestamp.date()
            service.create_habit_event(person_id, habit_id, notes="Day 3", timestamp=event3_timestamp)

            saved_habit_day3 = mock_habit_repo.save.call_args[0][0]

            self.assertEqual(3, saved_habit_day3.streak)
            self.assertEqual(saved_habit_day3.last_completed.date(), event3_timestamp.date())

        # Day 5: skip a day, streak should reset
        event5_timestamp = datetime(2024, 1, 5, 10, 0, 0)
        with unittest.mock.patch('application.domain.services.habit_event_service.datetime') as mock_dt:
            mock_dt.now.return_value = event5_timestamp
            mock_dt.date.today.return_value = event5_timestamp.date()
            service.create_habit_event(person_id, habit_id, notes="Day 5", timestamp=event5_timestamp)

            saved_habit_day5 = mock_habit_repo.save.call_args[0][0]

            self.assertEqual(1, saved_habit_day5.streak)
            self.assertEqual(saved_habit_day5.last_completed.date(), event5_timestamp.date())
