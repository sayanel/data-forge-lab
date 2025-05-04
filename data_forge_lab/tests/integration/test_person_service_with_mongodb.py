import pytest
from uuid import uuid4
from datetime import date
from random import randint, choice
from string import ascii_letters

from application.domain.models.person import Person, Country
from application.domain.services.person_service import PersonService
from infrastructure.persistence.mongodb.person import MongoPersonRepository

from tests.utils.mongo_test_config import get_test_collection


def random_string(length=6):
    return ''.join(choice(ascii_letters) for _ in range(length))


@pytest.fixture(scope="module")
def mongo_collection():
    collection = get_test_collection("test_persons")
    collection.delete_many({})
    yield collection
    collection.delete_many({})


@pytest.fixture
def person_service(mongo_collection):
    repo = MongoPersonRepository(mongo_collection)
    return PersonService(repo)


def test_create_and_get_person(person_service):
    person = Person(
        first_name="Alice",
        last_name="Smith",
        date_of_birth=date(1990, 5, 14),
        email="alice@example.com",
        phone_number="123-456-7890",
        address="123 Main St",
        gender="Female",
        country=Country.USA
    )

    # Save
    saved = person_service.create_person(**person.to_creation_dict())
    assert saved.first_name == "Alice"

    # Fetch
    fetched = person_service.get_person(saved.person_id)
    assert fetched is not None
    assert fetched.email == "alice@example.com"


def test_update_person(person_service):
    person = Person(
        first_name="Bob",
        last_name="Brown",
        date_of_birth=date(1985, 3, 10),
        email="bob@example.com",
        phone_number="555-555-5555",
        address="456 Side St",
        gender="Male",
        country=Country.UK
    )

    person_service.create_person(**person.to_creation_dict())
    update_fields = {
        "address": "789 New Address",
        "phone_number": "999-999-9999"
    }

    updated = person_service.update_person(person.person_id, **update_fields)

    assert updated is not None
    assert updated.address == "789 New Address"
    assert updated.phone_number == "999-999-9999"


def test_delete_person(person_service):
    person = Person(
        first_name="Carol",
        last_name="Danvers",
        date_of_birth=date(1992, 12, 1),
        email="carol@example.com",
        phone_number="111-111-1111",
        address="987 Hidden Rd",
        gender="Female",
        country=Country.FRANCE
    )

    person_service.create_person(**person.to_creation_dict())
    deleted = person_service.delete_person(person.person_id)
    assert deleted is True

    assert person_service.get_person(person.person_id) is None


def test_list_all(person_service):
    # Insert multiple persons
    for _ in range(3):
        p = Person(
            first_name=random_string(),
            last_name=random_string(),
            date_of_birth=date(1991, 1, randint(1, 28)),
            email=f"{random_string()}@example.com",
            phone_number="000-000-0000",
            address="Some address",
            gender="Other",
            country=choice(list(Country))
        )
        person_service.create_person(**p.to_creation_dict())

    all_persons = person_service.list_persons()
    assert isinstance(all_persons, list)
    assert len(all_persons) >= 3


def test_create_person_missing_fields(person_service):
    with pytest.raises(TypeError):
        # Missing required fields like last_name, email, etc.
        person_service.create_person(first_name="MissingFields")


def test_get_nonexistent_person(person_service):
    random_id = uuid4()
    person = person_service.get_person(random_id)
    assert person is None


def test_update_nonexistent_person(person_service):
    random_id = uuid4()
    result = person_service.update_person(random_id, address="No one lives here")
    assert result is None


def test_delete_nonexistent_person(person_service):
    random_id = uuid4()
    result = person_service.delete_person(random_id)
    assert result is False


def test_get_person_invalid_uuid_type(person_service):
    with pytest.raises(ValueError):
        # Not a UUID, but string or number
        person_service.get_person("not-a-uuid")


def test_update_person_country(person_service):
    person = Person(
        first_name="David",
        last_name="Wilson",
        date_of_birth=date(1988, 7, 15),
        email="david@example.com",
        phone_number="222-222-2222",
        address="321 Oak St",
        gender="Male",
        country=Country.USA
    )

    person_service.create_person(**person.to_creation_dict())
    update_fields = {
        "country": Country.GERMANY
    }

    updated = person_service.update_person(person.person_id, **update_fields)

    assert updated is not None
    assert updated.country == Country.GERMANY
