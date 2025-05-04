"""app.py

This module defines the entry point for the Data Forge Lab Flask web application.

The application:
- Initializes the web server (`Flask`) and CORS configuration.
- Initializes logging (both console and rotating file logging).
- Loads repositories, services, and controllers via the dependency injection container (`RepositoryContainer`).
- Registers the API controllers as Flask blueprints under the `/api` URL prefix.

Key Points:
- **Dependency Injection**: Repositories and services are not instantiated manually but retrieved from the container.
- **Separation of Concerns**: This file only wires high-level components together; all detailed implementations
  (repositories, event publishers, services) are handled by the container.
- **CORS**: Cross-Origin Resource Sharing is enabled to allow the frontend to communicate with this backend.
- **Logging**: Rotating file logs are used to prevent uncontrolled log file growth, while also logging to console
  for real-time feedback during development.

Benefits of this architecture:
- Clear, modular structure that isolates concerns (web server vs business logic).
- Easier to change/replace technologies (e.g., swap Flask for another framework in the future).
- Unified way to register blueprints/controllers.
- Centralized and consistent logging setup.
- Improved testability and maintainability.

"""

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_cors import CORS

from containers import RepositoryContainer


def init_logger():
    # Create a logger object
    logger = logging.getLogger('data_forge_lab')
    logger.setLevel(logging.DEBUG)  # Set the logger level to DEBUG

    # Create a console handler to display logs on the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create a file handler to write logs to a file
    file_handler = RotatingFileHandler(
        r'C:\Users\maximilien\Dev\data-forge-lab\logs\app.log',
        maxBytes=5*1024*1024,  # 5 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = init_logger()


def create_app():
    app = Flask(__name__)
    # CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    container = RepositoryContainer()

    person_controller = container.person_controller()
    habit_controller = container.habit_controller()
    habit_event_controller = container.habit_event_controller()
    analytics_controller = container.analytics_controller()
    system_controller = container.system_controller()

    app.register_blueprint(person_controller.person_blueprint, url_prefix='/api')
    app.register_blueprint(habit_controller.habit_blueprint, url_prefix='/api')
    app.register_blueprint(habit_event_controller.habit_event_blueprint, url_prefix='/api')
    app.register_blueprint(analytics_controller.analytics_blueprint, url_prefix='/api')
    app.register_blueprint(system_controller.system_blueprint, url_prefix='/api')

    return app


if __name__ == '__main__':
    logger.info("Start data-forge-lab.")

    app = create_app()
    app.run(debug=True, port=5000)
