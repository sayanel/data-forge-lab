import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime

from application.domain.services.habit_event_service import HabitEventService
from application.domain.models.event import HabitEventCreatedMessage


@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def mock_publisher():
    return Mock()


@pytest.fixture
def habit_event_service(mock_repo, mock_publisher):
    return HabitEventService(habit_event_repo=mock_repo, event_publisher=mock_publisher)


def test_health_check():
    from kafka.admin import KafkaAdminClient

    try:
        admin = KafkaAdminClient(bootstrap_servers="172.26.201.78:9092")
        topics = admin.list_topics()
        print(f"topics: {topics}")
        print("Kafka is reachable!")
    except Exception as e:
        print(f"Kafka connection failed: {e}")


def test_create_habit_event_publishes_event(habit_event_service, mock_repo, mock_publisher):
    # Arrange
    person_id = uuid4()
    habit_id = uuid4()
    mock_event = Mock()
    mock_event.person_id = person_id
    mock_event.habit_id = habit_id
    mock_event.event_id = uuid4()
    mock_event.timestamp = datetime.now()
    mock_event.to_event_created.return_value = HabitEventCreatedMessage(
        person_id=str(person_id),
        habit_id=str(habit_id),
        event_id=str(mock_event.event_id),
        timestamp=mock_event.timestamp
    )

    mock_repo.save.return_value = mock_event

    # Act
    result = habit_event_service.create_habit_event(person_id, habit_id, notes="Did yoga")

    # Assert
    mock_repo.save.assert_called_once()
    mock_publisher.publish.assert_called_once_with(mock_event.to_event_created())
    assert result == mock_event


def test_update_habit_event_success(habit_event_service, mock_repo):
    # Arrange
    event_id = uuid4()
    original_event = Mock()
    original_event.event_id = event_id
    original_event.notes = "Old note"
    original_event.status = "pending"

    updated_event = Mock()
    updated_event.event_id = event_id
    updated_event.notes = "Updated note"
    updated_event.status = "completed"

    mock_repo.get_by_id.return_value = original_event
    mock_repo.save.return_value = updated_event

    # Act
    result = habit_event_service.update_habit_event(event_id, notes="Updated note", status="completed")

    # Assert
    mock_repo.get_by_id.assert_called_once_with(event_id)
    mock_repo.save.assert_called_once_with(original_event)
    assert result == updated_event
    assert result.notes == "Updated note"
    assert result.status == "completed"


def test_update_habit_event_not_found(habit_event_service, mock_repo):
    # Arrange
    missing_id = uuid4()
    mock_repo.get_by_id.return_value = None

    # Act
    result = habit_event_service.update_habit_event(missing_id, notes="Something")

    # Assert
    mock_repo.get_by_id.assert_called_once_with(missing_id)
    mock_repo.save.assert_not_called()
    assert result is None
