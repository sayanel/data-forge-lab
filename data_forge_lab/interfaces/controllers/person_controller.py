import logging
from datetime import datetime
from uuid import UUID
from flask import Blueprint, request, jsonify
from application.use_cases.person_use_cases import PersonUseCases
from application.domain.services.person_service import PersonService
from application.domain.models.person import Country

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
        self.person_blueprint.route('/countries', methods=['GET'])(self.get_countries)


    def create_person(self):
        created_persons = []
        data = request.get_json()

        for person_to_create in data:
            try:
                logger.info(f"create person: {person_to_create}")

                date_of_birth = datetime.strptime(person_to_create['date_of_birth'], '%Y-%m-%d').date()

                person = self.person_use_cases.create_person(
                    first_name=person_to_create['first_name'],
                    last_name=person_to_create['last_name'],
                    date_of_birth=date_of_birth,
                    email=person_to_create['email'],
                    phone_number=person_to_create['phone_number'],
                    address=person_to_create['address'],
                    country=Country(person_to_create['country']),
                    gender=person_to_create.get('gender'),
                    notification_preferences=person_to_create.get('notification_preferences'),
                    language_preference=person_to_create.get('language_preference', "English")
                )
                created_persons.append(person.to_dict())
            except Exception as e:
                logger.error(f"Error creating person: {e}")
                return jsonify({"error": f"Failed to create person: {person_to_create}", "details": str(e)}), 500

        return jsonify(created_persons), 201

    def get_person(self, person_id):
        person = self.person_use_cases.get_person(person_id)
        if not person:
            return jsonify({"error": "Person not found"}), 404

        return jsonify(person.to_dict()), 200

    def update_person(self, person_id):
        data = request.get_json()
        person = self.person_use_cases.update_person(person_id, **data)
        if not person:
            return jsonify({"error": "Person not found"}), 404

        return jsonify(person.to_dict()), 200

    def delete_person(self, person_id):
        success = self.person_use_cases.delete_person(person_id)
        if not success:
            return jsonify({"error": "Person not found"}), 404
        return '', 204

    def list_persons(self):
        persons = self.person_use_cases.list_persons()
        persons_dict = list(map(lambda person: person.to_dict(), persons))
        return jsonify(persons_dict), 200

    def get_countries(self):
        """Get list of available countries."""
        try:
            countries = [{"name": country.name, "value": country.value} for country in Country]
            return jsonify(countries), 200
        except Exception as e:
            logger.error(f"Error getting countries: {e}")
            return jsonify({"error": "Failed to get countries", "details": str(e)}), 500


# Initialize the controller with dependencies
def init_person_controller(person_repo):
    person_service = PersonService(person_repo)
    person_use_cases = PersonUseCases(person_service)
    return PersonController(person_use_cases)
