import logging
from uuid import UUID
from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from application.use_cases.analytics_use_cases import AnalyticsUseCases

logger = logging.getLogger('data_forge_lab')


class AnalyticsController:
    def __init__(self, analytics_use_cases: AnalyticsUseCases):
        self.analytics_use_cases = analytics_use_cases
        self.analytics_blueprint = Blueprint('analytics', __name__)
        self.setup_routes()

    def setup_routes(self):
        self.analytics_blueprint.route('/analytics/streaks', methods=['GET'])(self.get_habit_streaks)
        self.analytics_blueprint.route('/analytics/completion-rates', methods=['GET'])(self.get_completion_rates)
        self.analytics_blueprint.route('/analytics/time-heatmap', methods=['GET'])(self.get_time_heatmap)
        self.analytics_blueprint.route('/analytics/habit-popularity', methods=['GET'])(self.get_habit_popularity)
        self.analytics_blueprint.route('/analytics/drop-off-rates', methods=['GET'])(self.get_drop_off_rates)
        self.analytics_blueprint.route('/analytics/first-week-success', methods=['GET'])(self.get_first_week_success)
        self.analytics_blueprint.route('/analytics/engagement', methods=['GET'])(self.get_engagement_metrics)
        self.analytics_blueprint.route('/analytics/geographic-trends', methods=['GET'])(self.get_geographic_trends)

    def get_habit_streaks(self):
        try:
            person_id = request.args.get('person_id')
            result = self.analytics_use_cases.get_habit_streaks(UUID(person_id) if person_id else None)
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error getting habit streaks: {e}")
            return jsonify({"error": "Failed to get habit streaks", "details": str(e)}), 500

    def get_completion_rates(self):
        try:
            person_id = request.args.get('person_id')
            result = self.analytics_use_cases.get_completion_rates(UUID(person_id) if person_id else None)
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error getting completion rates: {e}")
            return jsonify({"error": "Failed to get completion rates", "details": str(e)}), 500

    def get_time_heatmap(self):
        try:
            person_id = request.args.get('person_id')
            result = self.analytics_use_cases.get_time_of_day_heatmap(UUID(person_id) if person_id else None)
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error getting time heatmap: {e}")
            return jsonify({"error": "Failed to get time heatmap", "details": str(e)}), 500

    def get_habit_popularity(self):
        try:
            result = self.analytics_use_cases.get_most_least_completed_habits()
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error getting habit popularity: {e}")
            return jsonify({"error": "Failed to get habit popularity", "details": str(e)}), 500

    def get_drop_off_rates(self):
        try:
            days_threshold = request.args.get('days', default=7, type=int)
            result = self.analytics_use_cases.get_drop_off_rates(days_threshold)
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error getting drop-off rates: {e}")
            return jsonify({"error": "Failed to get drop-off rates", "details": str(e)}), 500

    def get_first_week_success(self):
        try:
            result = self.analytics_use_cases.get_first_week_success()
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error getting first week success: {e}")
            return jsonify({"error": "Failed to get first week success", "details": str(e)}), 500

    def get_engagement_metrics(self):
        try:
            result = self.analytics_use_cases.get_engagement_metrics()
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error getting engagement metrics: {e}")
            return jsonify({"error": "Failed to get engagement metrics", "details": str(e)}), 500

    def get_geographic_trends(self):
        try:
            result = self.analytics_use_cases.get_geographic_trends()
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error getting geographic trends: {e}")
            return jsonify({"error": "Failed to get geographic trends", "details": str(e)}), 500 