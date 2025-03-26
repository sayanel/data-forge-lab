import logging
from uuid import UUID
from flask import Blueprint, request, jsonify
from application.use_cases.habit_event_use_cases import HabitEventUseCases
from domain.services.habit_event_service import HabitEventService

logger = logging.getLogger('data_forge_lab')


class HabitEventController:
    def __init__(self, habit_event_use_cases: HabitEventUseCases):
        self.habit_event_use_cases = habit_event_use_cases
        self.habit_event_blueprint = Blueprint('habit_events', __name__)
        self.setup_routes()

    def setup_routes(self):
        self.habit_event_blueprint.route('/habit_events', methods=['POST'])(self.create_habit_event)
        self.habit_event_blueprint.route('/habit_events/<uuid:event_id>', methods=['GET'])(self.get_habit_event)
        self.habit_event_blueprint.route('/habit_events/<uuid:event_id>', methods=['PUT'])(self.update_habit_event)
        self.habit_event_blueprint.route('/habit_events/<uuid:event_id>', methods=['DELETE'])(self.delete_habit_event)
        self.habit_event_blueprint.route('/habits/<uuid:habit_id>/events', methods=['GET'])(self.list_habit_events)

    def create_habit_event(self):
        logger.info("create habit event")
        data = request.get_json()
        event = self.habit_event_use_cases.create_habit_event(
            person_id=UUID(data['person_id']),
            habit_id=UUID(data['habit_id']),
            notes=data['notes']
        )
        return jsonify(event), 201

    def get_habit_event(self, event_id):
        event = self.habit_event_use_cases.get_habit_event(event_id)
        if not event:
            return jsonify({"error": "Habit event not found"}), 404
        return jsonify(event), 200

    def update_habit_event(self, event_id):
        data = request.get_json()
        event = self.habit_event_use_cases.update_habit_event(event_id, **data)
        if not event:
            return jsonify({"error": "Habit event not found"}), 404
        return jsonify(event), 200

    def delete_habit_event(self, event_id):
        success = self.habit_event_use_cases.delete_habit_event(event_id)
        if not success:
            return jsonify({"error": "Habit event not found"}), 404
        return '', 204

    def list_habit_events(self, habit_id):
        events = self.habit_event_use_cases.list_habit_events(habit_id)
        return jsonify(events), 200


# Initialize the controller with dependencies
def init_habit_event_controller(habit_event_repo):
    habit_event_service = HabitEventService(habit_event_repo)
    habit_event_use_cases = HabitEventUseCases(habit_event_service)
    return HabitEventController(habit_event_use_cases)
