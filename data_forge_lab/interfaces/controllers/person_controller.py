import logging
from uuid import UUID
from flask import Blueprint, request, jsonify
from application.use_cases.person_use_cases import PersonUseCases
from domain.services.person_service import PersonService

logger = logging.getLogger('data_forge_lab')


class PersonController:
    def __init__(self, person_use_cases: PersonUseCases):
        self.person_use_cases = person_use_cases
        self.person_blueprint = Blueprint('persons', __name__)
        self.setup_routes()

    def setup_routes(self):
        self.person_blueprint.route('/persons', methods=['POST'])(self.create_person)
        self.person_blueprint.route('/persons/<uuid:person_id>', methods=['GET'])(self.get_person)
        self.person_blueprint.route('/persons/<uuid:person_id>', methods=['PUT'])(self.update_person)
        self.person_blueprint.route('/persons/<uuid:person_id>', methods=['DELETE'])(self.delete_person)
        self.person_blueprint.route('/persons', methods=['GET'])(self.list_persons)

    def create_person(self):
        logger.info("create person")
        data = request.get_json()
        person = self.person_use_cases.create_person(
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=data['date_of_birth'],
            email=data['email'],
            phone_number=data['phone_number'],
            address=data['address'],
            gender=data.get('gender'),
            notification_preferences=data.get('notification_preferences'),
            language_preference=data.get('language_preference', "English")
        )
        return jsonify(person), 201

    def get_person(self, person_id):
        person = self.person_use_cases.get_person(person_id)
        if not person:
            return jsonify({"error": "Person not found"}), 404
        return jsonify(person), 200

    def update_person(self, person_id):
        data = request.get_json()
        person = self.person_use_cases.update_person(person_id, **data)
        if not person:
            return jsonify({"error": "Person not found"}), 404
        return jsonify(person), 200

    def delete_person(self, person_id):
        success = self.person_use_cases.delete_person(person_id)
        if not success:
            return jsonify({"error": "Person not found"}), 404
        return '', 204

    def list_persons(self):
        persons = self.person_use_cases.list_persons()
        return jsonify(persons), 200


# Initialize the controller with dependencies
def init_person_controller(person_repo):
    person_service = PersonService(person_repo)
    person_use_cases = PersonUseCases(person_service)
    return PersonController(person_use_cases)
