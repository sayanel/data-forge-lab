import unittest
from datetime import date
from uuid import uuid4
from application.domain.services.person_service import PersonService
from application.domain.models.person import Person, Country
from infrastructure.persistence.in_memory import InMemoryPersonRepository


class TestPersonService(unittest.TestCase):

    def setUp(self):
        # Initialize the in-memory repository
        self.person_repo = InMemoryPersonRepository()
        self.person_service = PersonService(self.person_repo)

    def test_create_person_with_id(self):
        # Arrange
        person_id = uuid4()
        person_data = {
            "person_id": person_id,
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": date(1990, 1, 1),
            "email": "john.doe@example.com",
            "phone_number": "123-456-7890",
            "address": "123 Main St",
            "country": Country.USA
        }

        # Act
        result = self.person_service.create_person(
            person_id=person_id,
            first_name=person_data["first_name"],
            last_name=person_data["last_name"],
            date_of_birth=person_data["date_of_birth"],
            email=person_data["email"],
            phone_number=person_data["phone_number"],
            address=person_data["address"],
            country=person_data["country"]
        )

        # Assert
        self.assertEqual(result.person_id, person_id)
        self.assertEqual(result.first_name, "John")
        self.assertEqual(result.date_of_birth, date(1990, 1, 1))

    def test_create_person_without_id(self):
        # Arrange
        person_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "date_of_birth": date(1992, 2, 2),
            "email": "jane.smith@example.com",
            "phone_number": "987-654-3210",
            "address": "456 Elm St",
            "country": Country.UK
        }

        # Act
        result = self.person_service.create_person(
            first_name=person_data["first_name"],
            last_name=person_data["last_name"],
            date_of_birth=person_data["date_of_birth"],
            email=person_data["email"],
            phone_number=person_data["phone_number"],
            address=person_data["address"],
            country=person_data["country"]
        )

        # Assert
        self.assertIsNotNone(result.person_id)
        self.assertEqual(result.first_name, "Jane")
        self.assertEqual(result.date_of_birth, date(1992, 2, 2))

    def test_get_person(self):
        # Arrange
        person_id = uuid4()
        person = Person(
            person_id=person_id,
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            email="john.doe@example.com",
            phone_number="123-456-7890",
            address="123 Main St",
            country=Country.USA
        )
        self.person_repo.save(person)

        # Act
        result = self.person_service.get_person(person_id)

        # Assert
        self.assertEqual(result.person_id, person_id)
        self.assertEqual(result.first_name, "John")

    def test_update_person(self):
        # Arrange
        person_id = uuid4()
        person = Person(
            person_id=person_id,
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            email="john.doe@example.com",
            phone_number="123-456-7890",
            address="123 Main St",
            country=Country.USA
        )
        self.person_repo.save(person)

        updated_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": date(1990, 1, 1),
            "email": "jane.doe@example.com",
            "phone_number": "123-456-7890",
            "address": "123 Main St",
            "country": Country.UK
        }

        # Act
        result = self.person_service.update_person(person_id, **updated_data)

        # Assert
        self.assertEqual(result.person_id, person_id)
        self.assertEqual(result.first_name, "Jane")
        self.assertEqual(result.email, "jane.doe@example.com")

    def test_delete_person(self):
        # Arrange
        person_id = uuid4()
        person = Person(
            person_id=person_id,
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            email="john.doe@example.com",
            phone_number="123-456-7890",
            address="123 Main St",
            country=Country.USA
        )
        self.person_repo.save(person)

        # Act
        result = self.person_service.delete_person(person_id)

        # Assert
        self.assertTrue(result)
        self.assertIsNone(self.person_repo.get_by_id(person_id))

    def test_list_persons(self):
        # Arrange
        person1 = Person(
            person_id=uuid4(),
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            email="john.doe@example.com",
            phone_number="123-456-7890",
            address="123 Main St",
            country=Country.USA
        )
        person2 = Person(
            person_id=uuid4(),
            first_name="Jane",
            last_name="Smith",
            date_of_birth=date(1992, 2, 2),
            email="jane.smith@example.com",
            phone_number="987-654-3210",
            address="456 Elm St",
            country=Country.UK
        )
        self.person_repo.save(person1)
        self.person_repo.save(person2)

        # Act
        result = self.person_service.list_persons()

        # Assert
        self.assertEqual(len(result), 2)
        self.assertTrue(any(person.first_name == "John" for person in result))
        self.assertTrue(any(person.first_name == "Jane" for person in result))


if __name__ == '__main__':
    unittest.main()
