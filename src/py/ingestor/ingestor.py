from confluent_kafka import Consumer, Message
from logging import Logger

class Ingestor:
    """
    Ingestion class for consuming messages from a kafka cluster into another system.

    Args:
        logger (Logger): The logger instance used to convey information for this class.
        bootstrap_server (str): The desired kafka broker to connect to.
        group_id (str): The group identifier for this ingestor.
        auto_offset_reset (str): Offset location for the ingestor to begin reading messages from if no offset is found.

    Attributes:
        consumer (Consumer): The internal kafka message consumer.
        topic_name (str): The name of the topic to read from.
    """
    def __init__(self, logger: Logger, bootstrap_server: str, group_id: str, auto_offset_reset: str, topic_name: str):
        # Create kafka consumer and store topic
        consumer_config = {
            "bootstrap.servers": bootstrap_server,
            "group.id": group_id,
            "auto.offset.reset": auto_offset_reset
        }

        self.consumer = Consumer(consumer_config)
        self.topic_name = topic_name
        self.logger = logger.getChild("ingestor")

    def __enter__(self):
        # Subscribe consumer to topic
        self.logger.info(f"Subscribing to topic {self.topic_name}...")
        self.consumer.subscribe([self.topic_name])
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Close connection to cluster and cleanup consumer
        self.logger.info("Closing consumer kafka connection...")
        self.consumer.close()

    def consume_messages(self, message_limit: int = 1, wait_time: float = 1.0) -> list[str] | None:
        """
        Consumes messages from the kafka cluster.

        Args:
            message_limit (int, optional): The specified limit on number of messages to return. Default limit is 1 message.
            wait_time (float, optional): The specified time in seconds to wait when message_limit has not been hit and there are no messages to consume. Default time is 1.

        Returns:
            list[str]: A list of messages, as strings, of all error free messages consumed. 
            None: If no messages are available.
        """
        try:
            consumed_messages = self.consumer.consume(num_messages=message_limit, timeout=wait_time)
            if consumed_messages:
                self.logger.info(f"Consumed {len(consumed_messages)} messages from topic {self.topic_name}...")
                return self.__get_unerrored_messages(consumed_messages)
            else:
                return None
        except Exception as e:
            self.logger.critical(f"Fatal error consuming messages in ingestor: {e}")
            raise

    def __get_unerrored_messages(self, consumed_messages: list[Message]) -> list[str]:
        """
        Private helper method for getting unerrored messages.

        Args:
            consumed_messages (list[Message]): The list of messages consumed.

        Returns:
            list[str]: A list of unerrored messages as strings.
        """
        unerrored_messages = []
        for msg in consumed_messages:
            # Check for individual message errors
            if msg.error():
                err_msg = f"Error consuming message {msg.value().decode("utf-8")}: {msg.error().str()}"
                self.logger.error(err_msg)
                if msg.error().fatal():
                    # Raise an exception for the fatal error
                    raise Exception(err_msg)
            else:
                unerrored_messages.append(msg.value().decode("utf-8"))
        return unerrored_messages