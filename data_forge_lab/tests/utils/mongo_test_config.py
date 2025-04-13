from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv(dotenv_path="../.env.test")


def get_test_collection(collection_name: str):
    print("MONGO_TEST_URI:", os.getenv("MONGO_TEST_URI"))
    print("MONGO_TEST_DB:", os.getenv("MONGO_TEST_DB"))

    client = MongoClient(os.getenv("MONGO_TEST_URI"))
    db_name = os.getenv("MONGO_TEST_DB")
    print("Loaded DB:", os.getenv("MONGO_TEST_DB"))

    if not db_name:
        raise ValueError("MONGO_TEST_DB is not set or .env.test failed to load")
    db = client[db_name]

    return db[collection_name]
