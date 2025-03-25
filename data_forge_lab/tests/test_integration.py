import random
import unittest
from uuid import uuid4
from datetime import date

from domain.models.person import Person
from domain.models.habit import Habit
from domain.models.event import HabitEvent
from domain.services.habit_service import HabitService
from domain.services.person_service import PersonService
from domain.services.event_service import HabitEventService
from infrastructure.persistence.in_memory import HabitRepositoryImpl, HabitEventRepositoryImpl, PersonRepositoryImpl


class TestIntegration(unittest.TestCase):

    def setUp(self):
        # Initialize in-memory repositories
        self.person_repository = PersonRepositoryImpl()
        self.habit_repository = HabitRepositoryImpl()
        self.event_repository = HabitEventRepositoryImpl()

        # Initialize services
        self.person_service = PersonService(self.person_repository)
        self.habit_service = HabitService(self.habit_repository)
        self.event_service = HabitEventService(self.event_repository)

        # Create test data
        self.persons = [
            Person(person_id=uuid4(), first_name="Liz", last_name="Rey", date_of_birth=date(1994, 7, 19), email="liz@example.com", phone_number="123-456-7890", address="123 Main St"),
            Person(person_id=uuid4(), first_name="Max", last_name="Gli", date_of_birth=date(1992, 2, 9), email="max@example.com", phone_number="098-765-4321", address="456 Oak Ave")
        ]

        self.habits = [
            Habit(person_id=self.persons[0].person_id, name="Exercise", goal="Daily", category="Health"),
            Habit(person_id=self.persons[0].person_id, name="Reading", goal="Weekly", category="Personal Development"),
            Habit(person_id=self.persons[1].person_id, name="Meditation", goal="Daily", category="Health"),
            Habit(person_id=self.persons[1].person_id, name="Learn Spanish", goal="Monthly", category="Personal Development"),
            Habit(person_id=self.persons[1].person_id, name="Hydration", goal="Daily", category="Health")
        ]

        self.habit_events = []
        for habit in self.habits:
            num_events = random.randint(5, 20)
            for _ in range(num_events):
                event = HabitEvent(person_id=habit.person_id, habit_id=habit.habit_id, notes="Event note")
                self.habit_events.append(event)

    def test_create_persons_habits_events(self):
        # Save persons to the repository
        for person in self.persons:
            self.person_service.create_person(
                first_name=person.first_name,
                last_name=person.last_name,
                date_of_birth=person.date_of_birth,
                email=person.email,
                phone_number=person.phone_number,
                address=person.address,
                person_id=person.person_id
            )

        # Save habits to the repository
        for habit in self.habits:
            self.habit_service.create_habit(
                person_id=habit.person_id,
                name=habit.name,
                goal=habit.goal,
                category=habit.category,
                habit_id=habit.habit_id
            )

        # Save habit events to the repository
        for event in self.habit_events:
            self.event_service.log_event(
                person_id=event.person_id,
                habit_id=event.habit_id,
                notes=event.notes
            )

        # Verify persons are created correctly
        created_persons = self.person_repository.find_all()
        self.assertEqual(len(created_persons), len(self.persons))

        # Verify habits are created correctly
        created_habits = self.habit_repository.find_all()
        self.assertEqual(len(created_habits), len(self.habits))

        # Verify habit events are created correctly
        created_events = self.event_repository.find_all()
        self.assertEqual(len(created_events), len(self.habit_events))


if __name__ == '__main__':
    unittest.main()
