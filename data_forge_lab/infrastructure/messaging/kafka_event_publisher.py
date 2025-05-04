import os
import json
from kafka import KafkaProducer, KafkaAdminClient
from application.domain.models.event import HabitEventCreatedMessage
from interfaces.event_publisher import EventPublisher


class KafkaEventPublisher(EventPublisher):
    def __init__(self, topic: str, bootstrap_servers: str = None):
        if bootstrap_servers is None:
            bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        
        try:
            # Health check
            admin = KafkaAdminClient(bootstrap_servers=self.bootstrap_servers)
            admin.list_topics()

            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
        except Exception as e:
            print(f"Kafka connection failed: {e}")
            raise

    def publish(self, event: HabitEventCreatedMessage) -> None:
        payload = {
            "type": event.__class__.__name__,
            "payload": event.to_dict()
        }
        self.producer.send(self.topic, payload)
        self.producer.flush()
