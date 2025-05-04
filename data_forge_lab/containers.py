"""containers.py

This module defines the RepositoryContainer for managing the application's dependency injection using the
`dependency_injector` library.

Dependency Injector is a popular Python framework for automatic dependency wiring. It allows better separation
of concerns, easier testing, configuration management, and ensures that object lifecycles (singleton vs factory)
are explicitly controlled.

This container:
- Switches automatically between MongoDB repositories and in-memory repositories based on an environment variable.
- Initializes an `EventPublisher` as either a real Kafka publisher or a no-op publisher depending on the environment.
- Uses `Singleton` providers to ensure one instance per application lifecycle (e.g., repositories, publishers).
- Uses `Factory` providers when multiple independent instances are needed (e.g., services or controllers).

Benefits of this architecture:
- Loose coupling between components (repositories, services, controllers).
- Easy to swap implementations (e.g., real database vs mock database) without changing application logic.
- Centralized, transparent configuration of dependencies.
- Testability: easy to mock any part of the system for unit or integration tests.

"""

import os
from dotenv import load_dotenv
from dependency_injector import containers, providers

# MongoDB repositories
from infrastructure.config.mongo_config import get_mongo_collections
from infrastructure.persistence.mongodb.person import MongoPersonRepository
from infrastructure.persistence.mongodb.habit import MongoHabitRepository
from infrastructure.persistence.mongodb.habit_event import MongoHabitEventRepository

# In-memory repositories
from infrastructure.persistence.in_memory import InMemoryPersonRepository
from infrastructure.persistence.in_memory import InMemoryHabitRepository
from infrastructure.persistence.in_memory import InMemoryHabitEventRepository

# Kafka publisher
from infrastructure.messaging.kafka_event_publisher import KafkaEventPublisher
from interfaces.event_publisher import EventPublisher

from application.domain.services.habit_service import HabitService
from application.domain.services.habit_event_service import HabitEventService
from application.domain.services.person_service import PersonService
from application.domain.services.analytics_service import AnalyticsService

from application.use_cases.habit_use_cases import HabitUseCases
from application.use_cases.habit_event_use_cases import HabitEventUseCases
from application.use_cases.person_use_cases import PersonUseCases
from application.use_cases.analytics_use_cases import AnalyticsUseCases

from interfaces.controllers.habit_controller import HabitController
from interfaces.controllers.habit_event_controller import HabitEventController
from interfaces.controllers.person_controller import PersonController
from interfaces.controllers.analytics_controller import AnalyticsController
from interfaces.controllers.system_controller import SystemController


load_dotenv()


class RepositoryContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app"])

    # Repositories
    repo_type = os.getenv("REPO_TYPE", "memory")
    if repo_type == "mongo":
        mongo_collections = providers.Singleton(get_mongo_collections)

        person_repo = providers.Singleton(
            MongoPersonRepository,
            collection=mongo_collections.provided["person"]
        )
        habit_repo = providers.Singleton(
            MongoHabitRepository,
            collection=mongo_collections.provided["habit"]
        )
        habit_event_repo = providers.Singleton(
            MongoHabitEventRepository,
            collection=mongo_collections.provided["habit_event"]
        )

        event_publisher = providers.Singleton(
            KafkaEventPublisher,
            topic="habit-events",
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        )
    else:
        person_repo = providers.Singleton(InMemoryPersonRepository)
        habit_repo = providers.Singleton(InMemoryHabitRepository)
        habit_event_repo = providers.Singleton(InMemoryHabitEventRepository)

        class NoOpEventPublisher(EventPublisher):
            def publish(self, event): pass

        event_publisher = providers.Singleton(NoOpEventPublisher)

    # Services
    person_service = providers.Factory(PersonService, person_repo=person_repo)
    habit_service = providers.Factory(HabitService, habit_repo=habit_repo, habit_event_repo=habit_event_repo)
    habit_event_service = providers.Factory(HabitEventService, habit_event_repo=habit_event_repo, event_publisher=event_publisher)
    analytics_service = providers.Factory(AnalyticsService, person_repo=person_repo, habit_repo=habit_repo, habit_event_repo=habit_event_repo)

    # Use Cases
    person_use_cases = providers.Factory(PersonUseCases, person_service=person_service)
    habit_use_cases = providers.Factory(HabitUseCases, habit_service=habit_service)
    habit_event_use_cases = providers.Factory(HabitEventUseCases, habit_event_service=habit_event_service)
    analytics_use_cases = providers.Factory(AnalyticsUseCases, analytics_service=analytics_service)

    # Controllers
    person_controller = providers.Factory(PersonController, person_use_cases=person_use_cases)
    habit_controller = providers.Factory(HabitController, habit_use_cases=habit_use_cases)
    habit_event_controller = providers.Factory(HabitEventController, habit_event_use_cases=habit_event_use_cases)
    analytics_controller = providers.Factory(AnalyticsController, analytics_use_cases=analytics_use_cases)
    system_controller = providers.Singleton(SystemController, person_repo=person_repo, event_publisher=event_publisher)