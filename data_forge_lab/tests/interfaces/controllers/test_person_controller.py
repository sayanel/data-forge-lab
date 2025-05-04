import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from interfaces.controllers.person_controller import PersonController, init_person_controller
from infrastructure.persistence.in_memory import InMemoryPersonRepository
from application.domain.models.person import Country, Person
from datetime import date
from uuid import UUID


class TestPersonController(unittest.TestCase):

    def setUp(self):
        # Initialize Flask app
        self.app = Flask(__name__)

        # Initialize repository
        self.person_repo = InMemoryPersonRepository()

        # Initialize the person controller
        self.person_controller = init_person_controller(self.person_repo)

        # Register blueprint
        self.app.register_blueprint(self.person_controller.person_blueprint, url_prefix='/api')

        # Set up the test client
        self.client = self.app.test_client()

    @patch('application.use_cases.person_use_cases.PersonUseCases.create_person')
    def test_create_person(self, mock_create_person):
        # Create a mock Person object
        mock_person = Person(
            person_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            email="john.doe@example.com",
            phone_number="123-456-7890",
            address="123 Main St",
            country=Country.USA
        )
        mock_create_person.return_value = mock_person

        # Send a POST request to create a person
        response = self.client.post('/api/persons', json=[{
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "email": "john.doe@example.com",
            "phone_number": "123-456-7890",
            "address": "123 Main St",
            "country": Country.USA.value
        }])

        # Assert the response
        self.assertEqual(response.status_code, 201)
        self.assertIn("John", response.json[0]["first_name"])

    @patch('application.use_cases.person_use_cases.PersonUseCases.get_person')
    def test_get_person(self, mock_get_person):
        # Create a mock Person object
        mock_person = Person(
            person_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            email="john.doe@example.com",
            phone_number="123-456-7890",
            address="123 Main St",
            country=Country.USA
        )
        mock_get_person.return_value = mock_person

        # Send a GET request to retrieve a person
        response = self.client.get('/api/persons/123e4567-e89b-12d3-a456-426614174000')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("John", response.json["first_name"])

    @patch('application.use_cases.person_use_cases.PersonUseCases.update_person')
    def test_update_person(self, mock_update_person):
        # Create a mock Person object
        mock_person = Person(
            person_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            first_name="Jane",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            email="john.doe@example.com",
            phone_number="123-456-7890",
            address="123 Main St",
            country=Country.USA
        )
        mock_update_person.return_value = mock_person

        # Send a PUT request to update a person
        response = self.client.put('/api/persons/123e4567-e89b-12d3-a456-426614174000', json={"first_name": "Jane"})

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertIn("Jane", response.json["first_name"])

    @patch('application.use_cases.person_use_cases.PersonUseCases.delete_person')
    def test_delete_person(self, mock_delete_person):
        # Mock the delete_person method
        mock_delete_person.return_value = True

        # Send a DELETE request to delete a person
        response = self.client.delete('/api/persons/123e4567-e89b-12d3-a456-426614174000')

        # Assert the response
        self.assertEqual(response.status_code, 204)

    @patch('application.use_cases.person_use_cases.PersonUseCases.list_persons')
    def test_list_persons(self, mock_list_persons):
        # Create a mock Person object
        mock_person = Person(
            person_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            email="john.doe@example.com",
            phone_number="123-456-7890",
            address="123 Main St",
            country=Country.USA
        )
        mock_list_persons.return_value = [mock_person]

        # Send a GET request to list persons
        response = self.client.get('/api/persons')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)


if __name__ == '__main__':
    unittest.main()
