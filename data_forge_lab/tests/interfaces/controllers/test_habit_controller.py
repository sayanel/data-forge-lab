import unittest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch
from uuid import UUID

from interfaces.controllers.habit_controller import habit_blueprint
from application.use_cases.habit_use_cases import HabitUseCases
from domain.services.habit_service import HabitService
from infrastructure.persistence.in_memory import HabitRepositoryImpl


class TestHabitController(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(habit_blueprint, url_prefix='/api')
        self.client = self.app.test_client()

        self.default_person_id = "12345678-1234-1234-1234-123456789abc"

        self.habit_repository = HabitRepositoryImpl()

        self.habit_service = HabitService(self.habit_repository)
        self.habit_use_cases = HabitUseCases(self.habit_service)

    @patch('interfaces.controllers.habit_controller.habit_use_cases')
    def test_create_habit(self, mock_use_cases):
        mock_use_cases.create_habit.return_value = {
            "habit_id": "123e4567-e89b-12d3-a456-426614174000",
            "person_id": self.default_person_id,
            "name": "Test Habit",
            "goal": "Daily",
            "category": "Health"
        }

        response = self.client.post('/api/habits', json={
            "person_id": self.default_person_id,
            "name": "Test Habit",
            "goal": "Daily",
            "category": "Health"
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn("Test Habit", response.json["name"])

    @patch('interfaces.controllers.habit_controller.HabitUseCases.update_habit')
    def test_update_habit(self, mock_update_habit):
        mock_update_habit.return_value = {
            "habit_id": "123e4567-e89b-12d3-a456-426614174000",
            "person_id": self.default_person_id,
            "name": "Updated Habit",
            "goal": "Daily",
            "category": "Health"
        }

        response = self.client.put('/api/habits/123e4567-e89b-12d3-a456-426614174000', json={
            "name": "Updated Habit"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated Habit", response.json["name"])

    @patch('interfaces.controllers.habit_controller.HabitUseCases.get_habit')
    def test_get_habit(self, mock_get_habit):
        mock_get_habit.return_value = {
            "habit_id": "123e4567-e89b-12d3-a456-426614174000",
            "person_id": "12345678-1234-1234-1234-123456789abc",
            "name": "Test Habit",
            "goal": "Daily",
            "category": "Health"
        }

        response = self.client.get('/api/habits/123e4567-e89b-12d3-a456-426614174000')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Habit", response.json["name"])

    @patch('interfaces.controllers.habit_controller.HabitUseCases.list_habits')
    def test_list_habits(self, mock_list_habits):
        mock_list_habits.return_value = [
            {
                "habit_id": "123e4567-e89b-12d3-a456-426614174000",
                "person_id": self.default_person_id,
                "name": "Test Habit",
                "goal": "Daily",
                "category": "Health"
            }
        ]

        response = self.client.get(f"/api/users/{self.default_person_id}/habits")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    @patch('interfaces.controllers.habit_controller.HabitUseCases.delete_habit')
    def test_delete_habit(self, mock_delete_habit):
        mock_delete_habit.return_value = True

        response = self.client.delete('/api/habits/123e4567-e89b-12d3-a456-426614174000')

        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
