import unittest
from unittest.mock import patch, MagicMock
from flask import Flask

from interfaces.controllers.habit_controller import HabitController, init_habit_controller
from infrastructure.persistence.in_memory import HabitRepositoryImpl, HabitEventRepositoryImpl


class TestHabitController(unittest.TestCase):

    def setUp(self):
        # Initialize Flask app
        self.app = Flask(__name__)

        # Initialize repositories
        self.habit_repo = HabitRepositoryImpl()
        self.event_repo = HabitEventRepositoryImpl()

        # Initialize the habit controller
        self.habit_controller = init_habit_controller(self.habit_repo)

        # Register blueprint
        self.app.register_blueprint(self.habit_controller.habit_blueprint, url_prefix='/api')

        # Set up the test client
        self.client = self.app.test_client()

    @patch('application.use_cases.habit_use_cases.HabitUseCases.create_habit')
    def test_create_habit(self, mock_create_habit):
        # Mock the create_habit method
        mock_habit = {
            "habit_id": "123e4567-e89b-12d3-a456-426614174000",
            "person_id": "12345678-1234-1234-1234-123456789abc",
            "name": "Test Habit",
            "goal": "Daily",
            "category": "Health"
        }
        mock_create_habit.return_value = mock_habit

        # Send a POST request to create a habit
        response = self.client.post('/api/habits', json={
            "person_id": "12345678-1234-1234-1234-123456789abc",
            "name": "Test Habit",
            "goal": "Daily",
            "category": "Health"
        })

        # Assert the response
        self.assertEqual(response.status_code, 201)
        self.assertIn("Test Habit", response.json["name"])

    @patch('application.use_cases.habit_use_cases.HabitUseCases.update_habit')
    def test_update_habit(self, mock_update_habit):
        # Mock the update_habit method
        mock_habit = {
            "habit_id": "123e4567-e89b-12d3-a456-426614174000",
            "person_id": "12345678-1234-1234-1234-123456789abc",
            "name": "Updated Habit",
            "goal": "Daily",
            "category": "Health"
        }
        mock_update_habit.return_value = mock_habit

        # Send a PUT request to update a habit
        response = self.client.put('/api/habits/123e4567-e89b-12d3-a456-426614174000', json={
            "name": "Updated Habit"
        })

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Updated Habit", response.json["name"])

    @patch('application.use_cases.habit_use_cases.HabitUseCases.get_habit')
    def test_get_habit(self, mock_get_habit):
        # Mock the get_habit method
        mock_habit = {
            "habit_id": "123e4567-e89b-12d3-a456-426614174000",
            "person_id": "12345678-1234-1234-1234-123456789abc",
            "name": "Test Habit",
            "goal": "Daily",
            "category": "Health"
        }
        mock_get_habit.return_value = mock_habit

        # Send a GET request to retrieve a habit
        response = self.client.get('/api/habits/123e4567-e89b-12d3-a456-426614174000')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Habit", response.json["name"])

    @patch('application.use_cases.habit_use_cases.HabitUseCases.list_habits')
    def test_list_habits(self, mock_list_habits):
        # Mock the list_habits method
        mock_habits = [
            {
                "habit_id": "123e4567-e89b-12d3-a456-426614174000",
                "person_id": "12345678-1234-1234-1234-123456789abc",
                "name": "Test Habit",
                "goal": "Daily",
                "category": "Health"
            }
        ]
        mock_list_habits.return_value = mock_habits

        # Send a GET request to list habits
        response = self.client.get('/api/users/12345678-1234-1234-1234-123456789abc/habits')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    @patch('application.use_cases.habit_use_cases.HabitUseCases.delete_habit')
    def test_delete_habit(self, mock_delete_habit):
        # Mock the delete_habit method
        mock_delete_habit.return_value = True

        # Send a DELETE request to delete a habit
        response = self.client.delete('/api/habits/123e4567-e89b-12d3-a456-426614174000')

        # Assert the response
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()
