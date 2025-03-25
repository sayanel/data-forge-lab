import logging
from uuid import UUID, SafeUUID
from flask import Blueprint, request, jsonify
from application.use_cases.habit_use_cases import HabitUseCases
from domain.services.habit_service import HabitService
from infrastructure.persistence.in_memory import HabitRepositoryImpl
from infrastructure.persistence.in_memory import HabitEventRepositoryImpl


logger = logging.getLogger('data_forge_lab')

# Instantiate the repositories
habit_repository = HabitRepositoryImpl()
event_repository = HabitEventRepositoryImpl()

# Instantiate the use case with the repositories
habit_service = HabitService(habit_repository)
habit_use_cases = HabitUseCases(habit_service)

habit_blueprint = Blueprint('habits', __name__)


@habit_blueprint.route('/habits', methods=['POST'])
def create_habit():
    logger.info("create habit")
    data = request.get_json()
    person_id = UUID(data.get('person_id'))
    if not person_id:
        person_id = UUID('12345678-1234-1234-1234-123456789abc')

    name = data['name']
    goal = data['goal']
    category = data['category']
    habit = habit_use_cases.create_habit(person_id=person_id, name=name, goal=goal, category=category)
    return jsonify(habit), 201


@habit_blueprint.route('/habits/<uuid:habit_id>', methods=['PUT'])
def update_habit(habit_id):
    data = request.get_json()
    habit = HabitUseCases.update_habit(habit_id, **data)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404
    return jsonify(habit), 200


@habit_blueprint.route('/habits/<uuid:habit_id>', methods=['GET'])
def get_habit(habit_id):
    habit = HabitUseCases.get_habit(habit_id)
    if not habit:
        return jsonify({"error": "Habit not found"}), 404
    return jsonify(habit), 200


@habit_blueprint.route('/users/<uuid:person_id>/habits', methods=['GET'])
def list_habits(person_id):
    habits = HabitUseCases.list_habits(person_id)
    return jsonify(habits), 200


@habit_blueprint.route('/habits/<uuid:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    success = HabitUseCases.delete_habit(habit_id)
    if not success:
        return jsonify({"error": "Habit not found"}), 404
    return '', 204
