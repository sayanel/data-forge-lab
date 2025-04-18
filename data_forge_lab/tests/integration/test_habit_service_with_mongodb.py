import pytest
from uuid import uuid4
from random import choice
from string import ascii_letters

from application.domain.services.habit_service import HabitService
from infrastructure.persistence.mongodb.habit import MongoHabitRepository
from tests.utils.mongo_test_config import get_test_collection


def random_string(length=8):
    return ''.join(choice(ascii_letters) for _ in range(length))


@pytest.fixture(scope="module")
def mongo_collection():
    collection = get_test_collection("test_habits")
    collection.delete_many({})
    yield collection
    collection.delete_many({})


@pytest.fixture
def habit_service(mongo_collection):
    repo = MongoHabitRepository(mongo_collection)
    return HabitService(repo)


def test_create_and_get_habit(habit_service):
    person_id = uuid4()
    habit = habit_service.create_habit(
        person_id=person_id,
        name="Exercise",
        goal="3 times a week",
        category="Fitness"
    )

    assert habit.name == "Exercise"
    assert habit.person_id == person_id

    fetched = habit_service.get_habit(habit.habit_id)
    assert fetched is not None
    assert fetched.name == "Exercise"


def test_update_habit(habit_service):
    person_id = uuid4()
    habit = habit_service.create_habit(
        person_id=person_id,
        name="Read",
        goal="1 book/month",
        category="Education"
    )

    updated = habit_service.update_habit(
        habit.habit_id,
        name="Read More",
        goal="2 books/month"
    )

    assert updated is not None
    assert updated.name == "Read More"
    assert updated.goal == "2 books/month"


def test_find_all_habits(habit_service):
    all_habits = habit_service.habit_repo.find_all()
    assert isinstance(all_habits, list)


def test_delete_habit(habit_service):
    person_id = uuid4()
    habit = habit_service.create_habit(
        person_id=person_id,
        name="Meditate",
        goal="Every day",
        category="Mindfulness"
    )

    deleted = habit_service.delete_habit(habit.habit_id)
    assert deleted is True
    assert habit_service.get_habit(habit.habit_id) is None


def test_list_habits(habit_service):
    person_id = uuid4()
    for _ in range(3):
        habit_service.create_habit(
            person_id=person_id,
            name=random_string(),
            goal="Once daily",
            category="Routine"
        )

    habits = habit_service.list_habits(person_id)
    assert isinstance(habits, list)
    assert len(habits) >= 3
