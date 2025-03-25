import logging
from datetime import date
from flask import Blueprint, request, jsonify
from application.use_cases.person_use_cases import PersonUseCases

logger = logging.getLogger('data_forge_lab')

# Instantiate the repositories
habit_repository = HabitRepositoryImpl()
event_repository = HabitEventRepositoryImpl()

# Instantiate the use case with the repositories
habit_service = HabitService(habit_repository, event_repository)
habit_use_cases = HabitUseCases(habit_service)

person_blueprint = Blueprint('person', __name__)


@person_blueprint.route('/persons', methods=['POST'])
def create_person():
    data = request.get_json()
    person = PersonUseCases.create_person(
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=date.fromisoformat(data['date_of_birth']),
        email=data['email'],
        phone_number=data['phone_number'],
        address=data['address'],
        gender=data.get('gender'),
        notification_preferences=data.get('notification_preferences'),
        language_preference=data.get('language_preference', "English")
    )
    return jsonify(person), 201


@person_blueprint.route('/persons/<uuid:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.get_json()
    person = PersonUseCases.update_person(person_id, **data)
    if not person:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person), 200


@person_blueprint.route('/persons/<uuid:person_id>', methods=['GET'])
def get_person(person_id):
    person = PersonUseCases.get_person(person_id)
    if not person:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person), 200


@person_blueprint.route('/persons', methods=['GET'])
def list_persons():
    persons = PersonUseCases.list_persons()
    return jsonify(persons), 200


@person_blueprint.route('/persons/<uuid:person_id>', methods=['DELETE'])
def delete_person(person_id):
    success = PersonUseCases.delete_person(person_id)
    if not success:
        return jsonify({"error": "Person not found"}), 404
    return '', 204
