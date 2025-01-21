from confluent_kafka import Message
from typing import List
import logging

class Processor:
    """
    Processor class for parsing/cleaning messages and making analytical insights.

    Attributes:
        users (List[str]): List of users denoted by a unique user_id.
        user_logins (List[Tuple<int, datetime>]): List of tuples denoting total user logins and most recent login.
        devices (List[List[str]]): List of devices, as strings, mapped to each user in the user list.
    """
    def __init__(self, logger: logging.Logger):
        self.users = []
        self.user_logins = []
        self.devices = []
        self.logger = logger.getChild("processor")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def process_messages(self, messages: List[Message]) -> List[Message]:
        processed_messages = []
        self.logger.info(f"Attempting to process {len(messages)} messages...")
        for message in messages:
            self.logger.debug(f"Processing message: {message}")
            processed_messages.append(message)
        return processed_messages