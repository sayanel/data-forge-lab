import requests
import random
import time
from faker import Faker

# todo:
# - Add a reset_db function to clear the database before running the simulation, create API endpoint.
# - Send a signal to refresh UI
# - randomize the country for each user creation
# - habits shouldn't be fake but get from API, like Country. So we stay consistent with the names.
# - Make it faster, maybe start a microservice per user
# - Convert to GO


API_URL = "http://localhost:5000/api"
fake = Faker()


def reset_db():
    # todo
    pass


def create_random_users(n):
    users = []
    for _ in range(n):
        user = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "address": fake.address(),
            "country": "USA"  # or random.choice([...])
        }
        users.append(user)
    resp = requests.post(f"{API_URL}/persons", json=users)
    print(f"[INFO] Created {n} users: {resp.status_code}")
    return resp.json()


def get_users():
    resp = requests.get(f"{API_URL}/persons")
    return resp.json()


def get_habits(person_id):
    resp = requests.get(f"{API_URL}/persons/{person_id}/habits")
    return resp.json()


def create_random_habit(person_id):
    categories = ["Health", "Personal Development", "Productivity", "Social", "Financial"]
    category = random.choice(categories)
    habit = {
        "person_id": person_id,
        "name": fake.word().capitalize(),
        "category": category,
        "goal": random.choice(["Daily", "Weekly", "Monthly"])
    }
    resp = requests.post(f"{API_URL}/habits", json=habit)
    print(f"[INFO] Created habit for user {person_id}: {resp.status_code}")
    return resp.json()


def create_random_habit_event(person_id, habit_id):
    event = {
        "person_id": person_id,
        "habit_id": habit_id,
        "notes": fake.sentence(),
        "event_type": "Completion",
        "timestamp": fake.date_time_this_year().isoformat()
    }
    resp = requests.post(f"{API_URL}/habit_events", json=event)
    print(f"[INFO] Created habit event for user {person_id}, habit {habit_id}: {resp.status_code}")
    return resp.json()


def delete_random_habit(person_id):
    habits = get_habits(person_id)
    if not habits:
        return
    habit = random.choice(habits)
    habit_id = habit["habit_id"]
    resp = requests.delete(f"{API_URL}/habits/{habit_id}")
    print(f"[INFO] Deleted habit {habit_id} for user {person_id}: {resp.status_code}")


def simulate_day(users):
    for user in users:
        action = random.choices(["add_habit", "add_event", "delete_habit"], weights=[0.2, 0.7, 0.1])[0]
        if action == "add_habit":
            create_random_habit(user["person_id"])
        elif action == "add_event":
            habits = get_habits(user["person_id"])
            if habits:
                habit = random.choice(habits)
                create_random_habit_event(user["person_id"], habit["habit_id"])
        elif action == "delete_habit":
            delete_random_habit(user["person_id"])
        time.sleep(0.1)  # avoid spamming the API


def main():
    print("--- Habit Simulation Script ---")
    reset = input("Reset DB and create new users? (y/n): ").strip().lower() == "y"
    if reset:
        reset_db()
        n_users = int(input("How many users to create?: "))
        users = create_random_users(n_users)
    else:
        users = get_users()
    days = input("How many days to simulate? (leave blank for interactive): ").strip()
    if days:
        days = int(days)
        for day in range(days):
            print(f"\n[SIM] Simulating day {day+1}/{days}")
            simulate_day(users)
    else:
        day = 1
        while True:
            print(f"\n[SIM] Simulating day {day}")
            simulate_day(users)
            cont = input("Simulate another day? (y/n): ").strip().lower()
            if cont != "y":
                break
            day += 1


if __name__ == "__main__":
    main()
