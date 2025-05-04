# data-forge-lab
DataForgeLab is an experimental platform designed to explore and master data engineering concepts. This project aims to simulate real-world data processing scenarios.
This project is a personal data management and productivity tracker that allows users to log habits, events, and self-development metrics. It's built using Onion Architecture and a microservice-friendly design.

# Tech Stack:
- Frontend: React
- Backend: Python (Flask)
- Database: MongoDB (also supports in-memory repo)
- Microservices: Go (notifications, analytics)
- Messaging: Kafka (event publishing + consumption)

# Key Concepts:
- Person: A user entity
- Habit: A recurring activity
- HabitEvent: A tracked occurrence of a habit
- HabitEventCreatedMessage: A Kafka DTO published when a habit event is logged

# Architecture summary:
- application/
    - domain/ → core models → business entities
    - domain / → services → business logic/rules
    - use_cases/ → orchestrates domain services and repo
- infrastructure/ → adapters
    - persistence/ → MongoDB + in-memory adapters
    - messaging/ → Kafka publisher/consumer
    - config/ → system-level setup
- interfaces/ → framework adapters
    - controllers/ → API layer → REST entry points with Flask
    - repositories/ → interfaces for persistence (used by services)
- microservices/
    - analytics, notifications, etc.


# Kafka
Requirements:
- WSL installed and working
- Kafka downloaded and extracted inside ~/kafka/kafka_2.13-4.0.0 inside WSL
- All commands assume Kafka default port localhost:9092