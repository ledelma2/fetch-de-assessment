from confluent_kafka import Producer
from logging import Logger

class Messenger:
    """
    Messenger class for producing messages and sending them to the kafka cluster.

    Args:
        bootstrap_server (str): The desired kafka broker to connect to.
        client_id (str): The client identifier for this messenger.

    Attributes:
        producer (Producer): The internal kafka message producer.
        topic_name (str): The name of the topic to send messages to.
    """
    def __init__(self, logger: Logger, bootstrap_server: str, client_id: str, topic_name: str):
        producer_config = {
            "bootstrap.servers": bootstrap_server,
            "client.id": client_id,
        }

        self.producer = Producer(producer_config)
        self.topic_name = topic_name
        self.logger = logger.getChild("messenger")

    def __enter__(self):
        # Wait for callbacks on any messages still waiting
        self.logger.debug("Setting up producer...")
        self.producer.flush()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Deliver any straggler messages that haven't been sent
        self.logger.debug("Shutting down producer...")
        self.producer.purge()
        self.producer.flush()

    def callback(self, err, msg):
        """
        Callback function upon message delivery acknowledgement.

        Args:
            err: Any error that might occur during message delivery.
            msg: The message associated with this specific callback.
        """
        if err is not None:
            self.logger.warning(f"Failed to deliver message {msg} due to error {err}")
        else:
            self.logger.debug(f"Message successfully delivered to topic {msg.topic()} and partition {msg.partition()}")

    def produce_messages(self, messages: list[dict[str, str]], wait_time: float = 0.1):
        """
        Produces messages to a kafka topic.

        Args:
            messages (list[dict[str, str]]): A list of dictionaries of strings, with each list item representing a message to be produced.
            wait_time (float): A time in seconds describing how long to block when waiting for callbacks on message production.
        """
        try:
            self.logger.info(f"Attempting to produce {len(messages)} processed messages to topic {self.topic_name}...")
            for message in messages:
                # Trigger any available callbacks from previous message delivery
                self.logger.debug(f"Polling for callbacks with wait time {wait_time}")
                self.producer.poll(wait_time)

                # Produce the message with callback
                self.logger.debug(f"Attempting to produce message {message} to topic {self.topic_name}")
                self.producer.produce(self.topic_name, str(message).encode("utf-8"), callback=self.callback)
            self.producer.flush()
        except Exception as e:
            self.logger.critical(f"Fatal error producing messages in messenger: {e}")
            raise