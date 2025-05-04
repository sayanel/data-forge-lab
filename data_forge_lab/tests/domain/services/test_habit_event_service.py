import unittest
from uuid import uuid4
from unittest.mock import MagicMock
from application.domain.services.habit_event_service import HabitEventService
from application.domain.models.event import HabitEvent
from infrastructure.persistence.in_memory import InMemoryHabitEventRepository


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