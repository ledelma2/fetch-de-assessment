from confluent_kafka import Message
from typing import List

class Processor:
    """
    Processor class for parsing/cleaning messages and making analytical insights.

    Attributes:
        users (List[str]): List of users denoted by a unique user_id.
        user_logins (List[Tuple<int, datetime>]): List of tuples denoting total user logins and most recent login.
        devices (List[List[str]]): List of devices, as strings, mapped to each user in the user list.
    """
    def __init__(self):
        self.users = []
        self.user_logins = []
        self.devices = []

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def process_messages(self, messages: List[Message]) -> List[Message]:
        processed_messages = []
        for message in messages:
            print(f"Processing message: {message}")
            processed_messages.append(message)

        return processed_messages