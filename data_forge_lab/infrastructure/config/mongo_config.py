import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_mongo_collections():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DB")]

    return {
        "person": db[os.getenv("MONGO_PERSON_COLLECTION")],
        "habit": db[os.getenv("MONGO_HABIT_COLLECTION")],
        "habit_event": db[os.getenv("MONGO_HABIT_EVENT_COLLECTION")]
    }
