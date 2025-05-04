import pytest
from kafka import KafkaProducer, KafkaConsumer
from kafka import TopicPartition
from kafka.errors import KafkaError, KafkaTimeoutError, NoBrokersAvailable
import time
import threading


@pytest.fixture(scope="module")
def kafka_config():
    return {
        'bootstrap_servers': 'localhost:9092',
    }


@pytest.fixture
def producer(kafka_config):
    producer = KafkaProducer(**kafka_config)
    yield producer
    producer.close()  # Close the producer after tests


@pytest.fixture
def consumer(kafka_config):
    consumer = KafkaConsumer('test_topic', **kafka_config, group_id='test_group')
    yield consumer
    consumer.close()  # Close the consumer after tests


@pytest.fixture
def test_topic():
    return 'test_topic'


def test_producer_sends_message(producer, test_topic):
    """Test that the producer can send a message to a Kafka topic"""

    # Produce a message to Kafka
    message = "Hello, Kafka!"
    producer.send(test_topic, value=message.encode('utf-8'))
    producer.flush()

    # Allow some time for message delivery
    time.sleep(1)

    # No exceptions, so the message was sent successfully
    # In real cases, you might want to test for the message's delivery callback


def test_consumer_receives_message(producer, consumer, test_topic):
    """Test that the consumer can consume a message from a Kafka topic"""

    def consume_message():
        for message in consumer:
            assert message.value.decode('utf-8') == "Hello, Kafka!"
            consumer.close()
            break

    # Produce a message first
    producer.send(test_topic, value="Hello, Kafka!".encode('utf-8'))
    producer.flush()

    # Start consumer in a separate thread to simulate async consumption
    consumer_thread = threading.Thread(target=consume_message)
    consumer_thread.start()
    consumer_thread.join()


def test_end_to_end_integration(producer, consumer, test_topic):
    """Test end-to-end functionality: producer sends, consumer receives"""

    def consume_message():
        for message in consumer:
            assert message.value.decode('utf-8') == "End-to-End Kafka Test!"
            consumer.close()
            break

    # Produce a message
    producer.send(test_topic, value="End-to-End Kafka Test!".encode('utf-8'))
    producer.flush()

    # Start consumer in a separate thread to simulate async consumption
    consumer_thread = threading.Thread(target=consume_message)
    consumer_thread.start()
    consumer_thread.join()


def test_consumer_handles_no_message(kafka_config, test_topic):
    """Test that the consumer handles the case where no message is available"""
    consumer = KafkaConsumer(**kafka_config,
                             group_id='test_group_no_message',
                             consumer_timeout_ms=3000)  # 3 seconds timeout
    consumer.assign([TopicPartition(test_topic, 0)])
    # If no messages in 3 seconds, it will raise StopIteration
    with pytest.raises(StopIteration):
        next(consumer)
    consumer.close()


def test_error_handling_producer(test_topic):
    """Test producer error handling if Kafka is down"""
    # Change the Kafka configuration to an invalid server
    invalid_kafka_config = {
        'bootstrap_servers': 'localhost:9999',  # Invalid Kafka server
    }

    with pytest.raises(NoBrokersAvailable):
        invalid_producer = KafkaProducer(**invalid_kafka_config)
        invalid_producer.send(test_topic, value="Test message".encode('utf-8'))
        invalid_producer.flush()


def test_error_handling_consumer(test_topic):
    """Test consumer error handling if Kafka is down"""
    invalid_kafka_config = {
        'bootstrap_servers': 'localhost:9999',  # Invalid Kafka server
    }
    with pytest.raises(NoBrokersAvailable):
        invalid_consumer = KafkaConsumer('test_topic', **invalid_kafka_config, group_id='test_group')
        for message in invalid_consumer:
            pass  # This should not succeed as Kafka is down
