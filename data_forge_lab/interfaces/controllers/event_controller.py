from flask import Blueprint, request, jsonify
from uuid import UUID
from application.use_cases.event_use_cases import HabitEventUseCases

event_blueprint = Blueprint('event', __name__)

@event_blueprint.route('/habits/<uuid:habit_id>/events', methods=['POST'])
def log_event(habit_id):
    data = request.get_json()
    person_id = UUID(data['person_id'])
    notes = data.get('notes')
    event = HabitEventUseCases.log_event(person_id, habit_id, notes)
    return jsonify(event), 201

@event_blueprint.route('/events/<uuid:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    event = HabitEventUseCases.update_event(event_id, **data)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event), 200

@event_blueprint.route('/events/<uuid:event_id>', methods=['GET'])
def get_event(event_id):
    event = HabitEventUseCases.get_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event), 200

@event_blueprint.route('/habits/<uuid:habit_id>/events', methods=['GET'])
def list_events(habit_id):
    events = HabitEventUseCases.list_events(habit_id)
    return jsonify(events), 200

@event_blueprint.route('/events/<uuid:event_id>', methods=['DELETE'])
def delete_event(event_id):
    success = HabitEventUseCases.delete_event(event_id)
    if not success:
        return jsonify({"error": "Event not found"}), 404
    return '', 204
