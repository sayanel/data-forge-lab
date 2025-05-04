from pymongo import MongoClient
from data_forge_lab.application.domain.models.person import Country
import random


def migrate_persons_country():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['data_forge_lab']
    persons_collection = db['persons']

    # Get all persons without a country field
    persons_without_country = persons_collection.find({"country": {"$exists": False}})
    
    # Get list of available countries
    available_countries = list(Country)
    
    # Update each person with a random country
    for person in persons_without_country:
        random_country = random.choice(available_countries)
        persons_collection.update_one(
            {"_id": person["_id"]},
            {"$set": {"country": random_country.value}}
        )
        print(f"Updated person {person['_id']} with country {random_country.value}")

    print("Migration completed!")


if __name__ == "__main__":
    migrate_persons_country()
