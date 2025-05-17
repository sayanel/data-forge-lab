from datetime import datetime, timedelta
from typing import List, Dict, Any
from uuid import UUID
from application.domain.models.person import Person, Country
from application.domain.models.habit import Habit
from application.domain.models.event import HabitEvent
from interfaces.repositories.person_repository import PersonRepository
from interfaces.repositories.habit_repository import HabitRepository
from interfaces.repositories.habit_event_repository import HabitEventRepository


class AnalyticsService:
    def __init__(
        self,
        person_repo: PersonRepository,
        habit_repo: HabitRepository,
        habit_event_repo: HabitEventRepository
    ):
        self.person_repo = person_repo
        self.habit_repo = habit_repo
        self.habit_event_repo = habit_event_repo

    def get_completion_rates(self, person_id: UUID = None) -> Dict[str, float]:
        """Calculate completion rates for habits."""
        habits = self.habit_repo.find_by_person_id(person_id) if person_id else self.habit_repo.find_all()
        completion_rates = {}
        
        for habit in habits:
            events = self.habit_event_repo.find_by_habit_id(habit.habit_id)
            total_events = len(events)
            completed_events = sum(1 for e in events if e.status == "completed")
            
            completion_rates[str(habit.habit_id)] = {
                "completion_rate": (completed_events / total_events * 100) if total_events > 0 else 0,
                "habit_name": habit.name
            }
        
        return completion_rates

    def get_consistency(self, person_id: UUID = None):
        # Example: average completion rate across all habits or for a person
        if person_id:
            # Person-specific consistency (e.g., average completion rate)
            rates = self.get_completion_rates(person_id)
            if rates:
                avg = sum(r['completion_rate'] for r in rates.values()) / len(rates)
                return {"consistency": avg}
            return {"consistency": 0.0}
        else:
            # Global average consistency
            rates = self.get_completion_rates()
            if rates:
                avg = sum(r['completion_rate'] for r in rates.values()) / len(rates)
                return {"average_consistency": avg}
            return {"average_consistency": 0.0}
    
    def get_distribution(self, person_id: UUID = None):
        # Example: count of habits per category
        habits = self.habit_repo.find_by_person_id(person_id) if person_id else self.habit_repo.find_all()
        dist = {}
        for habit in habits:
            dist[habit.category] = dist.get(habit.category, 0) + 1
        return dist

    def get_category_distribution(self, person_id: UUID = None):
        # Alias for get_distribution (for now)
        return self.get_distribution(person_id)

    def get_habit_popularity(self):
        # Count number of unique persons that have each habit name
        habits = self.habit_repo.find_all()
        habit_persons = {}
        for habit in habits:
            if habit.name not in habit_persons:
                habit_persons[habit.name] = set()
            habit_persons[habit.name].add(habit.person_id)
        # Build list of {habit_name, user_count}
        habit_counts = [
            {"habit_name": name, "user_count": len(persons)}
            for name, persons in habit_persons.items()
        ]
        sorted_habits = sorted(habit_counts, key=lambda x: x["user_count"], reverse=True)
        return sorted_habits[:5]

    def get_time_of_day_heatmap(self, person_id: UUID = None) -> Dict[str, int]:
        """Generate time-of-day heatmap data."""
        events = self.habit_event_repo.find_by_person_id(person_id) if person_id else self.habit_event_repo.find_all()
        heatmap = {f"{hour:02d}:00": 0 for hour in range(24)}
        
        for event in events:
            hour = event.timestamp.hour
            heatmap[f"{hour:02d}:00"] += 1
        
        return heatmap

    def get_drop_off_rates(self, days_threshold: int = 7) -> Dict[str, float]:
        """Calculate how often users abandon habits after X days."""
        habits = self.habit_repo.find_all()
        drop_off_data = {}
        
        for habit in habits:
            events = sorted(self.habit_event_repo.find_by_habit_id(habit.habit_id), key=lambda x: x.timestamp)
            if not events:
                continue
                
            first_event = events[0]
            last_event = events[-1]
            days_active = (last_event.timestamp - first_event.timestamp).days
            
            drop_off_data[str(habit.habit_id)] = {
                "drop_off_rate": 1 if days_active < days_threshold else 0,
                "habit_name": habit.name,
                "days_active": days_active
            }
        
        return drop_off_data

    def get_first_week_success(self) -> Dict[str, float]:
        """Calculate success rates in the first week of habit creation."""
        habits = self.habit_repo.find_all()
        first_week_data = {}
        
        for habit in habits:
            events = sorted(self.habit_event_repo.find_by_habit_id(habit.habit_id), key=lambda x: x.timestamp)
            if not events:
                continue
                
            first_event = events[0]
            first_week_events = [e for e in events if (e.timestamp - first_event.timestamp).days <= 7]
            completed_in_first_week = sum(1 for e in first_week_events if e.status == "completed")
            
            first_week_data[str(habit.habit_id)] = {
                "success_rate": (completed_in_first_week / len(first_week_events) * 100) if first_week_events else 0,
                "habit_name": habit.name
            }
        
        return first_week_data

    def get_engagement_metrics(self) -> Dict[str, Any]:
        """Calculate engagement metrics."""
        users = self.person_repo.find_all()
        habits = self.habit_repo.find_all()
        events = self.habit_event_repo.find_all()
        
        # Active users per time period
        now = datetime.now()
        active_users = {
            "day": set(),
            "week": set(),
            "month": set()
        }
        
        for event in events:
            event_time = event.timestamp
            if (now - event_time).days == 0:
                active_users["day"].add(str(event.person_id))
            if (now - event_time).days <= 7:
                active_users["week"].add(str(event.person_id))
            if (now - event_time).days <= 30:
                active_users["month"].add(str(event.person_id))
        
        return {
            "active_users": {
                "daily": len(active_users["day"]),
                "weekly": len(active_users["week"]),
                "monthly": len(active_users["month"])
            },
            "avg_habits_per_user": len(habits) / len(users) if users else 0
        }

    def get_geographic_trends(self) -> Dict[str, Dict[str, int]]:
        """Analyze habit popularity by country."""
        users = self.person_repo.find_all()
        habits = self.habit_repo.find_all()
        country_data = {}
        
        # Initialize country data
        for country in Country:
            country_data[country.value] = {
                "total_habits": 0,
                "total_events": 0,
                "active_users": 0
            }
        
        # Count habits and events by country
        for user in users:
            country = user.country.value if user.country else None
            if country and country in country_data:
                user_habits = [h for h in habits if h.person_id == user.person_id]
                user_events = [e for e in self.habit_event_repo.find_by_person_id(user.person_id)]
                country_data[country]["total_habits"] += len(user_habits)
                country_data[country]["total_events"] += len(user_events)
                if user_events:
                    country_data[country]["active_users"] += 1
        
        return country_data
