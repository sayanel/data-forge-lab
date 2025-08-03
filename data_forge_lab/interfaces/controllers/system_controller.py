import logging
from flask import Blueprint, jsonify

logger = logging.getLogger('data_forge_lab')


class SystemController:
    def __init__(self, person_repo, event_publisher):
        self.person_repo = person_repo
        self.event_publisher = event_publisher
        self.system_blueprint = Blueprint('system', __name__)
        self.system_blueprint.route('/system/status', strict_slashes=False, methods=['GET'])(self.get_status)

    def get_status(self):
        """Health check for MongoDB, Kafka, and Flask."""
        status = {"mongo": False, "kafka": False, "flask": False}

        # MongoDB check
        try:
            if self.person_repo and hasattr(self.person_repo, 'collection'):
                self.person_repo.collection.find_one({})
                status["mongo"] = True
        except Exception as e:
            logger.error(f"MongoDB health check failed: {e}")

        # Kafka check
        try:
            if self.event_publisher and hasattr(self.event_publisher, 'producer'):
                self.event_publisher.producer.partitions_for('test')
                status["kafka"] = True
        except Exception as e:
            logger.error(f"Kafka health check failed: {e}")

        # Flask check: if this endpoint is hit, Flask is running
        status["flask"] = True

        return jsonify(status), 200 
