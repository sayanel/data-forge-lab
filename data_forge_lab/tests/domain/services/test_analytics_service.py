import unittest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime, timedelta
from application.domain.services.analytics_service import AnalyticsService
from application.domain.models.habit import Habit
from application.domain.models.event import HabitEvent
from application.domain.models.person import Person


class TestAnalyticsService(unittest.TestCase):
    def setUp(self):
        self.person_repo = MagicMock()
        self.habit_repo = MagicMock()
        self.habit_event_repo = MagicMock()
        self.analytics = AnalyticsService(
            person_repo=self.person_repo,
            habit_repo=self.habit_repo,
            habit_event_repo=self.habit_event_repo
        )
        self.person_id = uuid4()
        self.habit_id = uuid4()
        self.habit = Habit(
            person_id=self.person_id,
            name="Exercise",
            goal="Daily",
            category="Health",
            habit_id=self.habit_id
        )
        self.event1 = HabitEvent(
            person_id=self.person_id,
            habit_id=self.habit_id,
            timestamp=datetime.now() - timedelta(days=1),
            status="completed"
        )
        self.event2 = HabitEvent(
            person_id=self.person_id,
            habit_id=self.habit_id,
            timestamp=datetime.now(),
            status="missed"
        )

    def test_get_completion_rates(self):
        self.habit_repo.find_by_person_id.return_value = [self.habit]
        self.habit_event_repo.find_by_habit_id.return_value = [self.event1, self.event2]
        rates = self.analytics.get_completion_rates(self.person_id)
        self.assertIn(str(self.habit_id), rates)
        self.assertAlmostEqual(rates[str(self.habit_id)]["completion_rate"], 50.0)

    def test_get_consistency(self):
        self.habit_repo.find_by_person_id.return_value = [self.habit]
        self.habit_event_repo.find_by_habit_id.return_value = [self.event1, self.event2]
        result = self.analytics.get_consistency(self.person_id)
        self.assertIn("consistency", result)
        self.assertAlmostEqual(result["consistency"], 50.0)

    def test_get_distribution(self):
        self.habit_repo.find_by_person_id.return_value = [self.habit]
        dist = self.analytics.get_distribution(self.person_id)
        self.assertIn("Health", dist)
        self.assertEqual(dist["Health"], 1)

    def test_get_habit_popularity(self):
        self.habit_repo.find_all.return_value = [self.habit]
        result = self.analytics.get_habit_popularity()
        self.assertTrue(any(h["habit_name"] == "Exercise" for h in result))

    def test_get_time_of_day_heatmap(self):
        self.habit_event_repo.find_by_person_id.return_value = [
            HabitEvent(person_id=self.person_id, habit_id=self.habit_id, timestamp=datetime(2024, 1, 1, 8, 0), status="completed"),
            HabitEvent(person_id=self.person_id, habit_id=self.habit_id, timestamp=datetime(2024, 1, 1, 8, 30), status="completed"),
            HabitEvent(person_id=self.person_id, habit_id=self.habit_id, timestamp=datetime(2024, 1, 1, 9, 0), status="missed")
        ]
        heatmap = self.analytics.get_time_of_day_heatmap(self.person_id)
        self.assertEqual(heatmap["08:00"], 2)
        self.assertEqual(heatmap["09:00"], 1)

    def test_get_drop_off_rates(self):
        self.habit_repo.find_all.return_value = [self.habit]
        self.habit_event_repo.find_by_habit_id.return_value = [
            HabitEvent(person_id=self.person_id, habit_id=self.habit_id, timestamp=datetime.now() - timedelta(days=2), status="completed"),
            HabitEvent(person_id=self.person_id, habit_id=self.habit_id, timestamp=datetime.now(), status="completed")
        ]
        drop_off = self.analytics.get_drop_off_rates(days_threshold=1)
        self.assertIn(str(self.habit_id), drop_off)
        self.assertIn("drop_off_rate", drop_off[str(self.habit_id)])

    def test_get_first_week_success(self):
        self.habit_repo.find_all.return_value = [self.habit]
        self.habit_event_repo.find_by_habit_id.return_value = [
            HabitEvent(person_id=self.person_id, habit_id=self.habit_id, timestamp=datetime.now(), status="completed"),
            HabitEvent(person_id=self.person_id, habit_id=self.habit_id, timestamp=datetime.now(), status="missed")
        ]
        result = self.analytics.get_first_week_success()
        self.assertIn(str(self.habit_id), result)
        self.assertIn("success_rate", result[str(self.habit_id)])

    def test_get_engagement_metrics(self):
        self.person_repo.find_all.return_value = [MagicMock(person_id=self.person_id)]
        self.habit_repo.find_all.return_value = [self.habit]
        self.habit_event_repo.find_all.return_value = [
            HabitEvent(person_id=self.person_id, habit_id=self.habit_id, timestamp=datetime.now(), status="completed")
        ]
        metrics = self.analytics.get_engagement_metrics()
        self.assertIn("active_users", metrics)
        self.assertIn("avg_habits_per_user", metrics)

    def test_get_geographic_trends(self):
        person = MagicMock(person_id=self.person_id, country=MagicMock(value="USA"))
        self.person_repo.find_all.return_value = [person]
        self.habit_repo.find_all.return_value = [self.habit]
        self.habit_event_repo.find_by_person_id.return_value = [
            HabitEvent(person_id=self.person_id, habit_id=self.habit_id, timestamp=datetime.now(), status="completed")
        ]
        trends = self.analytics.get_geographic_trends()
        self.assertIn("USA", trends)
        self.assertIn("total_habits", trends["USA"])


if __name__ == "__main__":
    unittest.main()
