from confluent_kafka import Consumer, Message
from typing import List, Optional

class Ingestor:
    """
    Ingestion class for consuming messages from a kafka cluster into another system.

    Args:
        bootstrap_server (str): The desired kafka broker to connect to.
        group_id (str): The group identifier for this ingestor.
        auto_offset_reset (str): Offset location for the ingestor to begin reading messages from if no offset is found.

    Attributes:
        consumer (Consumer): The internal kafka message consumer.
        topic_name (str): The name of the topic to read from.
    """
    def __init__(self, bootstrap_server: str, group_id: str, auto_offset_reset: str, topic_name: str):
        # Create kafka consumer and store topic
        consumer_config = {
            'bootstrap.servers': bootstrap_server,
            'group.id': group_id,
            'auto.offset.reset': auto_offset_reset
        }

        self.consumer = Consumer(consumer_config)
        self.topic_name = topic_name

    def __enter__(self):
        # Subscribe consumer to topic
        self.consumer.subscribe([self.topic_name])
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        # Close connection to cluster and cleanup consumer
        self.consumer.close()

    def consume_message(self, message_limit: int = 1, wait_time: float = 1.0) -> Optional[List[str]]:
        """
        Consumes messages from the kafka cluster.

        Args:
            message_limit (int, optional): The specified limit on number of messages to return. Default limit is 1 message.
            wait_time (float, optional): The specified time in seconds to wait when message_limit has not been hit and there are no messages to consume. Default time is 1.

        Returns:
            Optional[List[str]]: A list of messages, as strings, of all error free messages consumed. None if no messages are available.
        """
        try:
            consumed_messages = self.consumer.consume(num_messages=message_limit, timeout=wait_time)
            if consumed_messages:
                return self.__get_unerrored_messages(consumed_messages)
            else:
                return None
        except Exception as e:
            print(f"Fatal error consuming messages in ingestor: {e}")
            raise

    def __get_unerrored_messages(self, consumed_messages: List[Message]) -> List[str]:
        """
        Private helper method for getting unerrored messages.

        Args:
            consumed_messages (List[Message]): The list of messages consumed.

        Returns:
            List[str]: A list of unerrored messages as strings.
        """
        unerrored_messages = []
        for msg in consumed_messages:
            # Check for individual message errors
            if msg.error():
                print(f"Error consuming message {msg.value().decode('utf-8')}: {msg.error()}")
            else:
                unerrored_messages.append(msg.value().decode('utf-8'))
        return unerrored_messages