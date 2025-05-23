from uuid import UUID
from typing import Dict, Any, Optional
from application.domain.services.analytics_service import AnalyticsService


class AnalyticsUseCases:
    def __init__(self, analytics_service: AnalyticsService):
        self.analytics_service = analytics_service

    def get_completion_rates(self, person_id: Optional[UUID] = None) -> Dict[str, float]:
        """Get completion rates for a specific person or all users."""
        return self.analytics_service.get_completion_rates(person_id)

    def get_consistency(self, person_id: Optional[UUID] = None):
        return self.analytics_service.get_consistency(person_id)
    
    def get_distribution(self, person_id: Optional[UUID] = None):
        return self.analytics_service.get_distribution(person_id)
    
    def get_habit_popularity(self):
        return self.analytics_service.get_habit_popularity()
    
    def get_time_of_day_heatmap(self, person_id: Optional[UUID] = None) -> Dict[str, int]:
        """Get time-of-day heatmap data for a specific person or all users."""
        return self.analytics_service.get_time_of_day_heatmap(person_id)

    def get_drop_off_rates(self, days_threshold: int = 7) -> Dict[str, float]:
        """Get drop-off rates for habits after a specified number of days."""
        return self.analytics_service.get_drop_off_rates(days_threshold)

    def get_first_week_success(self) -> Dict[str, float]:
        """Get success rates in the first week of habit creation."""
        return self.analytics_service.get_first_week_success()

    def get_engagement_metrics(self) -> Dict[str, Any]:
        """Get engagement metrics for the application."""
        return self.analytics_service.get_engagement_metrics()

    def get_geographic_trends(self) -> Dict[str, Dict[str, int]]:
        """Get geographic trends for habits and users."""
        return self.analytics_service.get_geographic_trends() 

    def get_category_distribution(self, person_id: Optional[UUID] = None):
        return self.analytics_service.get_category_distribution(person_id)
