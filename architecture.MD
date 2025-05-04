
Domain Services (domain/services)
Purpose: Domain services contain the core business logic and rules of your application. They encapsulate behaviors that involve multiple domain entities or complex business processes that don't naturally fit within a single entity.

Characteristics:

Business Logic: They contain the essential business rules and logic that define how your application operates.
Entity Interaction: They often interact with domain entities (e.g., Habit, Person) to perform operations.
Independent of External Systems: Domain services should not depend on external systems like databases or APIs. They should be pure business logic.
Example: A domain service might calculate the streak of a habit, determine if a goal has been met, or update the status of a habit based on certain conditions.

Application Use Cases (application/use_cases)
Purpose: Application use cases orchestrate the flow of data and operations to fulfill specific user stories or application features. They define how the application responds to user inputs and interacts with the domain layer.

Characteristics:

Orchestration: They coordinate the use of domain services and repositories to achieve a specific application goal.
Application-Specific Logic: They contain logic that is specific to the application's use cases, such as handling user input, managing workflows, and coordinating interactions between different parts of the system.
Depend on Domain Services: Use cases often depend on domain services to perform business logic but may also interact with repositories to retrieve or persist data.


Interaction between domain services and repositories:
Key Principles
Dependency Inversion:

The domain layer should not depend directly on the implementation details of data access (e.g., databases). Instead, it should depend on abstractions (interfaces) defined in the domain layer or an adjacent layer.
Abstraction:

Repositories are typically defined as interfaces in the domain layer or an adjacent layer (like interfaces). These interfaces define the contract for data access operations without specifying how these operations are implemented.
Implementation in Outer Layers:

The actual implementation of these repository interfaces resides in the outer layers (e.g., infrastructure), where the details of data access are handled.
How It Works
Domain Layer: Contains the core business logic and defines repository interfaces. These interfaces specify the methods that the domain services need to interact with data, but they do not provide implementations.

Infrastructure Layer: Implements the repository interfaces defined in the domain layer. This layer handles the actual data access logic, such as database queries.


## Hierarchy
data_forge_lab
├── application
│   ├── use_cases
│   │   ├── habit_event_use_cases.py
│   │   ├── habit_use_cases.py
│   │   └── person_use_cases.py
│   ├── domain
│   │   ├── models
│   │   │   ├── event.py
│   │   │   ├── habit.py
│   │   │   └── person.py
│   │   └── services
│   │       ├── habit_event_service.py
│   │       ├── habit_service.py
│   │       └── person_service.py
├── infrastructure
│   ├── config
│   │   ├── habit_categories.py
│   │   └── mongo_config.py
│   ├── persistence
│   │   ├── mongodb
│   │   │   ├── habit.py
│   │   │   ├── habit_event.py
│   │   │   └── person.py
│   │   ├── in_memory.py
├── interfaces
│   ├── controllers
│   │   ├── habit_controller.py
│   │   ├── habit_event_controller.py
│   │   └── person_controller.py
│   └── repositories
│       ├── habit_event_repository.py
│       ├── habit_repository.py
│       └── person_repository.py
├── tests
├── .env
├── app.py
├── containers.py
└── frontend
└── microservices
└── venv