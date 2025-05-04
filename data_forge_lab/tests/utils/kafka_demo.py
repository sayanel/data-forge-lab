import time
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from kafka.errors import KafkaError, NoBrokersAvailable

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC_NAME = 'demo_topic'


def simple_producer_demo():
    print("\n--- Simple Producer Demo ---")
    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    message = "Hello from Producer!"
    print(f"Sending message: {message}")
    producer.send(TOPIC_NAME, value=message.encode('utf-8'))
    producer.flush()
    print("Message sent!\n")
    producer.close()


def simple_consumer_demo():
    print("\n--- Simple Consumer Demo ---")
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id='demo_group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        consumer_timeout_ms=5000
    )  # Exit after 5s if no messages

    print("Listening for messages...")
    for message in consumer:
        print(f"Received message: {message.value.decode('utf-8')}")
    print("Consumer finished (no more messages).\n")
    consumer.close()


def end_to_end_demo():
    print("\n--- End-to-End Demo ---")
    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    consumer = KafkaConsumer(TOPIC_NAME,
                              bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                              group_id='end_to_end_group',
                              auto_offset_reset='earliest',
                              enable_auto_commit=True,
                              consumer_timeout_ms=5000)

    # Produce multiple messages
    messages = [f"Message {i}" for i in range(5)]
    for msg in messages:
        print(f"Sending: {msg}")
        producer.send(TOPIC_NAME, value=msg.encode('utf-8'))
    producer.flush()

    print("\nConsuming messages:")
    for message in consumer:
        print(f"Consumed: {message.value.decode('utf-8')}")

    print("End-to-End Demo complete.\n")
    producer.close()
    consumer.close()


def producer_error_demo():
    print("\n--- Producer Error Handling Demo ---")
    invalid_server = 'localhost:9999'
    try:
        producer = KafkaProducer(bootstrap_servers=invalid_server)
        producer.send(TOPIC_NAME, value="This won't work".encode('utf-8'))
        producer.flush()
    except NoBrokersAvailable as e:
        print(f"Producer failed to connect: {e}\n")


def consumer_no_message_demo():
    print("\n--- Consumer No Message Demo ---")
    consumer = KafkaConsumer(TOPIC_NAME,
                              bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                              group_id='no_message_group',
                              auto_offset_reset='latest',
                              enable_auto_commit=True,
                              consumer_timeout_ms=3000)  # Short timeout
    print("Listening for messages (expecting none)...")
    message_received = False
    for message in consumer:
        print(f"Unexpected message: {message.value.decode('utf-8')}")
        message_received = True

    if not message_received:
        print("No messages received as expected.\n")
    consumer.close()


if __name__ == "__main__":
    print("Starting Kafka Demos")

    try:
        simple_producer_demo()
        time.sleep(1)  # Wait a little
        simple_consumer_demo()

        time.sleep(1)
        end_to_end_demo()

        time.sleep(1)
        producer_error_demo()

        time.sleep(1)
        consumer_no_message_demo()

    except NoBrokersAvailable as e:
        print(f"Kafka is not available at {KAFKA_BOOTSTRAP_SERVERS}. Error: {e}")

    print("\nAll demos completed.")
