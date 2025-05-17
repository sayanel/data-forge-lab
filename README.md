# ⚙️data-forge-lab
DataForgeLab is an experimental platform designed to explore and master data engineering concepts. This project aims to simulate real-world data processing scenarios.
This project is a personal data management and productivity tracker that allows users to log habits, events, and self-development metrics. It's built using Onion Architecture and a microservice-friendly design.

# ⚠️ Disclaimer

This project is currently **under active development** and serves primarily as a personal sandbox for experimentation and learning.

- Many components are not production-ready.
- The codebase may lack standard production features such as input validation, error handling, and security hardening.
- Some architectural choices may evolve or be restructured.

Feedback and contributions are welcome as the project matures!

# 🚀 Tech Stack:
- Frontend: React
- Backend: Python (Flask)
- Database: MongoDB (also supports in-memory repo)
- Microservices: Go (notifications, analytics)
- Messaging: Kafka (event publishing + consumption)

# 🧰 How to get started:

To get the project up and running, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/sayanel/data-forge-lab
    cd data-forge-lab
    ```

2.  **Set up the Python virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS and Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install backend dependencies:**
    With the virtual environment activated, install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    - Edit the `.env` file with your specific configuration. Most likely you will just have to replace the IP to reach Kafka, that is running in wsl2.
    - Go through the batch file in the bin directory and potentially change paths to mongo and kafka.

5.  **Run the application:**
    Navigate to the bin directory.
    Start:
      - start_mongo.bat
      - kafka/start_kafka.bat
      - start_app.bat
      - start_front.bat
      - start_microservices.bat (optional)

---
# 🧱 Project Architecture Overview


## 🧠 Key Concepts:
- Person: A user entity
- Habit: A recurring activity
- HabitEvent: A tracked occurrence of a habit
- HabitEventCreatedMessage: A Kafka DTO published when a habit event is logged

    
## 🗺️ Hierarchy
This project is structured using a **clean, layered architecture** based on principles from **Onion** and **Hexagonal Architecture**. The goal is to keep the core logic independent from external concerns like databases, APIs, or frameworks, making the application modular, testable, and maintainable.

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


## 🧭 Responsibilities

### `application/domain/models` - **Domain Models**

**Purpose:**  
These are the core entities of the system - like `Habit`, `Person`, and `HabitEvent`. They represent real-world concepts and are central to the business logic.

**Characteristics:**
- Pure Python classes or dataclasses
- Represent state and simple behavior
- No dependencies on infrastructure or frameworks

---

### `application/domain/services` - **Domain Services**

**Purpose:**  
Encapsulate core business logic and rules that span multiple entities.

**Characteristics:**
- Contains essential logic (e.g., calculating a streak)
- Interacts with domain models
- No direct dependencies on databases, APIs, or external systems

**Example:**  
Updating habit status, checking if a goal has been achieved, or publishing an event.

---

### `application/use_cases` - **Application Use Cases**

**Purpose:**  
Orchestrate domain services and repositories to fulfill a specific application-level goal (i.e., user stories).

**Characteristics:**
- Define workflows (e.g., create habit event, get user habits)
- Coordinate between domain and infrastructure
- Handle application-specific decisions

---

### `interfaces/repositories` - **Repository Interfaces**

**Purpose:**  
Abstract the data access layer so the domain logic doesn't need to know how data is stored or retrieved.

**Example:**
```python
class HabitRepository(Protocol):
    def save(self, habit: Habit) -> Habit: ...
    def get(self, habit_id: UUID) -> Habit: ...
```

---

### `infrastructure/persistence` - **Data Layer Implementations**

**Purpose:**  
Implements the repository interfaces using actual persistence technologies like MongoDB or in-memory storage.

**Characteristics:**
- Swappable (e.g., test vs prod)
- Isolated from business logic
- Bound via dependency injection

---

### `interfaces/controllers` - **API Layer (Flask)**

**Purpose:**  
Expose application features via RESTful APIs. It receives HTTP requests, translates them into use case calls, and returns responses.

**Responsibilities:**
- Input/output transformation
- Calls into the application layer
- Stateless and thin - no business logic

---

### `infrastructure/messaging` - **Kafka Messaging (Pub/Sub)**

**Purpose:**  
Handle asynchronous events with Kafka. Used for emitting and consuming domain events (like `HabitEventCreated`).

**Components:**
- **Publisher:** Emits messages to Kafka topics
- **Consumer:** Listens to topics and reacts (e.g., triggers a notification)

**Why here:**  
Messaging is infrastructure - we isolate it from core logic and inject it via interfaces.

---

### `infrastructure/config` - **Configuration Layer**

**Purpose:**  
System-wide setup: MongoDB config, Kafka topics, environment variable bindings, etc.

**Characteristics:**
- Keeps config centralized
- Keeps other layers clean and decoupled

---

### `microservices/` - **Event-Driven Sidecar Services**

**Purpose:**  
Independent microservices that listen to Kafka and perform specific actions like notifications or analytics.

**Examples:**
- `simulate`: Simulates user behavior for testing
- `notifications`: Sends alerts when certain events occur
- `analytics`: Gathers and processes behavioral metrics

---

## 🔄 Layer Interactions

**Key Design Principles:**

- **Dependency Inversion:**  
  The core domain doesn't depend on infrastructure. Instead, it defines abstract interfaces (e.g., repository contracts).

- **Abstraction:**  
  Repositories are interfaces defined in the domain or adjacent layers, with implementations in `infrastructure`.

- **Separation of Concerns:**  
  Each layer has a clearly defined role, making the system easier to test, maintain, and extend.

---


## 📁 Project Directory Structure

```plaintext
data_forge_lab/
├── application/
│   ├── use_cases/
│   │   ├── habit_event_use_cases.py
│   │   ├── habit_use_cases.py
│   │   └── person_use_cases.py
│   ├── domain/
│   │   ├── models/
│   │   │   ├── event.py
│   │   │   ├── habit.py
│   │   │   └── person.py
│   │   └── services/
│   │       ├── habit_event_service.py
│   │       ├── habit_service.py
│   │       └── person_service.py
├── infrastructure/
│   ├── config/
│   │   ├── habit_categories.py
│   │   └── mongo_config.py
│   ├── persistence/
│   │   ├── mongodb/
│   │   │   ├── habit.py
│   │   │   ├── habit_event.py
│   │   │   └── person.py
│   │   └── in_memory.py
│   └── messaging/        # Kafka-related publisher/consumer logic
├── interfaces/
│   ├── controllers/
│   │   ├── habit_controller.py
│   │   ├── habit_event_controller.py
│   │   └── person_controller.py
│   └── repositories/
│       ├── habit_event_repository.py
│       ├── habit_repository.py
│       └── person_repository.py
├── microservices/        # Event-driven side services
├── frontend/             # React-based UI
├── tests/                # Unit and integration tests
├── .env                  # Environment configuration
├── app.py                # Main entry point (Flask)
├── containers.py         # Dependency Injection setup
└── venv/                 # Virtual environment
````

# 📬 Kafka
Requirements:
- WSL installed and working
- Kafka downloaded and extracted inside ~/kafka/kafka_2.13-4.0.0 inside WSL
- All commands assume Kafka default port localhost:9092
Domain Services (domain/services)


Purpose: Domain services contain the core business logic and rules of your application. They encapsulate behaviors that involve multiple domain entities or complex business processes that don't naturally fit within a single entity.
