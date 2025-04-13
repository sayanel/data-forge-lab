from dependency_injector import containers, providers
from dotenv import load_dotenv
import os

# MongoDB repositories
from infrastructure.config.mongo_config import get_mongo_collections
from infrastructure.persistence.mongodb.person import MongoPersonRepository
from infrastructure.persistence.mongodb.habit import MongoHabitRepository
from infrastructure.persistence.mongodb.habit_event import MongoHabitEventRepository

# In-memory repositories
from infrastructure.persistence.in_memory import InMemoryPersonRepository
from infrastructure.persistence.in_memory import InMemoryHabitRepository
from infrastructure.persistence.in_memory import InMemoryHabitEventRepository


load_dotenv()


class RepositoryContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app"])

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

    else:
        person_repo = providers.Singleton(InMemoryPersonRepository)
        habit_repo = providers.Singleton(InMemoryHabitRepository)
        habit_event_repo = providers.Singleton(InMemoryHabitEventRepository)
