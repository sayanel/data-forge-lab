import logging
from uuid import UUID
from flask import Blueprint, request, jsonify
from application.use_cases.habit_use_cases import HabitUseCases
from domain.services.habit_service import HabitService

logger = logging.getLogger('data_forge_lab')


class HabitController:
    def __init__(self, habit_use_cases: HabitUseCases):
        self.habit_use_cases = habit_use_cases
        self.habit_blueprint = Blueprint('habits', __name__)
        self.setup_routes()

    def setup_routes(self):
        self.habit_blueprint.route('/habits', methods=['POST'])(self.create_habit)
        self.habit_blueprint.route('/habits/<uuid:habit_id>', methods=['PUT'])(self.update_habit)
        self.habit_blueprint.route('/habits/<uuid:habit_id>', methods=['GET'])(self.get_habit)
        self.habit_blueprint.route('/persons/<uuid:person_id>/habits', methods=['GET'])(self.list_habits)
        self.habit_blueprint.route('/habits/<uuid:habit_id>', methods=['DELETE'])(self.delete_habit)

    def create_habit(self):
        logger.info("create habit")
        data = request.get_json()
        person_id = UUID(data.get('person_id'))
        if not person_id:
            person_id = UUID('12345678-1234-1234-1234-123456789abc')

        name = data['name']
        goal = data['goal']
        category = data['category']
        habit = self.habit_use_cases.create_habit(person_id=person_id, name=name, goal=goal, category=category)
        return jsonify(habit.to_dict()), 201

    def update_habit(self, habit_id):
        data = request.get_json()
        habit = self.habit_use_cases.update_habit(habit_id, **data)
        if not habit:
            return jsonify({"error": "Habit not found"}), 404
        return jsonify(habit.to_dict()), 200

    def get_habit(self, habit_id):
        habit = self.habit_use_cases.get_habit(habit_id)
        if not habit:
            return jsonify({"error": "Habit not found"}), 404
        return jsonify(habit.to_dict()), 200

    def list_habits(self, person_id):
        habits = self.habit_use_cases.list_habits(person_id)
        habits_dict = list(map(lambda habit: habit.to_dict(), habits))
        return jsonify(habits_dict), 200

    def delete_habit(self, habit_id):
        success = self.habit_use_cases.delete_habit(habit_id)
        if not success:
            return jsonify({"error": "Habit not found"}), 404
        return '', 204


# Initialize the controller with dependencies
def init_habit_controller(habit_repo):
    habit_service = HabitService(habit_repo)
    habit_use_cases = HabitUseCases(habit_service)
    return HabitController(habit_use_cases)
