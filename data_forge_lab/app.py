import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_cors import CORS

from containers import RepositoryContainer

from interfaces.controllers.habit_controller import init_habit_controller
from interfaces.controllers.person_controller import init_person_controller
from interfaces.controllers.habit_event_controller import init_habit_event_controller


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

    # Initialize the container and repositories
    container = RepositoryContainer()
    person_repo = container.person_repo()
    habit_repo = container.habit_repo()
    habit_event_repo = container.habit_event_repo()

    # Initialize controllers with the repositories
    person_controller = init_person_controller(person_repo)
    habit_controller = init_habit_controller(habit_repo)
    habit_event_controller = init_habit_event_controller(habit_event_repo)

    # Register blueprints
    app.register_blueprint(person_controller.person_blueprint, url_prefix='/api')
    app.register_blueprint(habit_controller.habit_blueprint, url_prefix='/api')
    app.register_blueprint(habit_event_controller.habit_event_blueprint, url_prefix='/api')

    return app


if __name__ == '__main__':
    logger.info("Start data-forge-lab.")

    app = create_app()
    app.run(debug=True, port=5000)
