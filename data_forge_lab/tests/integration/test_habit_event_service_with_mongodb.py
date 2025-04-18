import pytest
from uuid import uuid4
from datetime import datetime

from application.domain.services.habit_event_service import HabitEventService
from application.domain.models.event import HabitEvent
from infrastructure.persistence.mongodb.habit_event import MongoHabitEventRepository
from tests.utils.mongo_test_config import get_test_collection


@pytest.fixture(scope="module")
def mongo_collection():
    collection = get_test_collection("test_habit_events")
    collection.delete_many({})
    yield collection
    collection.delete_many({})


@pytest.fixture
def habit_event_service(mongo_collection):
    repo = MongoHabitEventRepository(mongo_collection)
    return HabitEventService(repo)


def test_create_and_get_event(habit_event_service):
    person_id = uuid4()
    habit_id = uuid4()

    event = habit_event_service.create_habit_event(person_id, habit_id, notes="First log")
    assert event.notes == "First log"

    fetched = habit_event_service.get_habit_event(event.event_id)
    assert fetched is not None
    assert fetched.person_id == person_id


def test_update_event(habit_event_service):
    person_id = uuid4()
    habit_id = uuid4()
    event = habit_event_service.create_habit_event(person_id, habit_id)

    updated = habit_event_service.update_habit_event(
        event.event_id,
        status="completed",
        notes="Done early"
    )

    assert updated.status == "completed"
    assert updated.notes == "Done early"


def test_find_all_events(habit_event_service):
    all_events = habit_event_service.habit_event_repo.find_all()
    assert isinstance(all_events, list)


def test_delete_event(habit_event_service):
    person_id = uuid4()
    habit_id = uuid4()
    event = habit_event_service.create_habit_event(person_id, habit_id)

    deleted = habit_event_service.delete_habit_event(event.event_id)
    assert deleted is True
    assert habit_event_service.get_habit_event(event.event_id) is None


def test_list_habit_events(habit_event_service):
    person_id = uuid4()
    habit_id = uuid4()
    for i in range(3):
        habit_event_service.create_habit_event(person_id, habit_id, notes=f"Note {i}")

    events = habit_event_service.list_habit_events(habit_id)
    assert len(events) >= 3
    assert all(isinstance(e, HabitEvent) for e in events)


def test_get_nonexistent_event(habit_event_service):
    fake_event_id = uuid4()
    event = habit_event_service.get_habit_event(fake_event_id)
    assert event is None


def test_update_nonexistent_event(habit_event_service):
    fake_event_id = uuid4()
    result = habit_event_service.update_habit_event(fake_event_id, notes="Should fail", status="completed")
    assert result is None


def test_delete_nonexistent_event(habit_event_service):
    fake_event_id = uuid4()
    deleted = habit_event_service.delete_habit_event(fake_event_id)
    assert deleted is False


def test_create_event_missing_notes(habit_event_service):
    person_id = uuid4()
    habit_id = uuid4()
    event = habit_event_service.create_habit_event(person_id, habit_id)
    assert event.notes is None
    assert event.status == "pending"


def test_update_event_invalid_field_is_ignored(habit_event_service):
    person_id = uuid4()
    habit_id = uuid4()
    event = habit_event_service.create_habit_event(person_id, habit_id, notes="original")

    # Try updating a non-existent attribute — should not crash or apply
    updated = habit_event_service.update_habit_event(event.event_id, foo="bar")
    assert updated is not None
    assert not hasattr(updated, "foo")
