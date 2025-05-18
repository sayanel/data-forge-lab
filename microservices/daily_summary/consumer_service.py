import logging
from datetime import date
from pprint import pformat
from collections import defaultdict

from infrastructure.messaging.kafka_event_consumer import KafkaEventConsumer

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("daily_tracker")


daily_events_by_day = defaultdict(list)


def track_event(event: dict):
    today = date.today().isoformat()
    daily_events_by_day[today].append(event)
    logger.info(f"Tracked habit event: {event}")


def generate_summary():
    today = date.today().isoformat()
    events = daily_events_by_day.get(today, [])

    summary = f"""
    ================================
    📊 Daily Habit Event Summary
    📅 Date: {today}
    🧾 Total Events: {len(events)}
    -------------------------------
    {pformat(events)}
    ================================
    """

    logger.info(summary)
    return summary


def clear_today():
    today = date.today().isoformat()
    daily_events_by_day[today] = []


class DailySummaryConsumer(KafkaEventConsumer):
    def process_habit_event_created(self, payload: dict):
        track_event(payload)
        generate_summary()


def main():
    consumer = DailySummaryConsumer(topic="habit-events")
    consumer.consume_events()


if __name__ == "__main__":
    main()
