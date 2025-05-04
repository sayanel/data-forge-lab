import unittest
from uuid import uuid4

from application.domain.services.habit_service import HabitService
from application.domain.models.habit import Habit
from infrastructure.persistence.in_memory import InMemoryHabitRepository


class TestHabitService(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryHabitRepository()
        self.service = HabitService(habit_repo=self.repo)

    def test_create_habit(self):
        person_id = uuid4()
        habit = self.service.create_habit(person_id, "Exercise", "Daily", "Health")
        self.assertEqual(habit.name, "Exercise")
        self.assertEqual(habit.person_id, person_id)

    def test_prevent_duplicate_habit(self):
        person_id = uuid4()
        self.service.create_habit(person_id, "Exercise", "Daily", "Health")
        with self.assertRaises(ValueError):
            self.service.create_habit(person_id, "Exercise", "Weekly", "Health")
        # Case-insensitive
        with self.assertRaises(ValueError):
            self.service.create_habit(person_id, "exercise", "Weekly", "Health")

    def test_update_habit(self):
        person_id = uuid4()
        habit = self.service.create_habit(person_id, "Read", "Weekly", "Personal Development")
        updated = self.service.update_habit(habit.habit_id, goal="Daily")
        self.assertEqual(updated.goal, "Daily")

    def test_list_habits(self):
        person_id = uuid4()
        self.service.create_habit(person_id, "A", "Daily", "Health")
        self.service.create_habit(person_id, "B", "Weekly", "Productivity")
        habits = self.service.list_habits(person_id)
        self.assertEqual(len(habits), 2)

    def test_delete_habit(self):
        person_id = uuid4()
        habit = self.service.create_habit(person_id, "Sleep", "Nightly", "Health")
        deleted = self.service.delete_habit(habit.habit_id)
        self.assertTrue(deleted)
        self.assertIsNone(self.service.get_habit(habit.habit_id)) 