from kafka import KafkaConsumer
import json
import logging

from application.domain.models.event import HabitEventCreatedMessage


logger = logging.getLogger("data_forge_lab")


class KafkaEventConsumer:
    """Kafka Event Consumer to listen for HabitEventCreated messages."""

    def __init__(self, topic: str, bootstrap_servers: str = "localhost:9092", group_id: str = "habit-event-consumers"):
        self.topic = topic
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",  # or "latest" depending on your needs
            enable_auto_commit=True,
        )

    def consume_events(self):
        logger.info(f"Starting Kafka consumer for topic: {self.topic}")
        for message in self.consumer:
            try:
                event_data = message.value
                self.handle_event(event_data)
            except Exception as e:
                logger.error(f"Failed to process message: {e}")

    def handle_event(self, event_data: dict):
        """Handle incoming events."""
        event_type = event_data.get("type")
        payload = event_data.get("payload")

        if event_type == "HabitEventCreated":
            self.process_habit_event_created(payload)
        else:
            logger.warning(f"Received unknown event type: {event_type}")

    def process_habit_event_created(self, payload: dict):
        """Process a HabitEventCreatedMessage event."""
        message = HabitEventCreatedMessage(**payload)
        logger.info(f"[Kafka] HabitEventCreatedMessage received: {message}")
        # Here you could add real logic: update stats, trigger notifications, etc.
