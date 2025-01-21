import ast
from logging import Logger

class Processor:
    """
    Processor class for parsing/cleaning messages and making analytical insights.

    Args:
        logger (Logger): The logger instance used to convey information for this class.

    Attributes:
        users (list[str]): List of users denoted by a unique user_id.
        user_logins (list[Tuple<int, datetime>]): List of tuples denoting total user logins and most recent login.
        devices (list[list[str]]): List of devices, as strings, mapped to each user in the user list.
    """
    def __init__(self, logger: Logger):
        self.users = []
        self.user_logins = []
        self.devices = []
        self.logger = logger.getChild("processor")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def process_messages_and_report_findings(self, messages: list[str]) -> list[dict[str, str]]:
        """
        Processes raw messages from kafka and reports some relevant findings based on the messages' contents.

        Args:
            messages (list[str]): A list of messages, as strings, to be processed.

        Returns:
            list[dict[str, str]]: A list of processed messages as dictionaries.
        """
        processed_messages = []
        self.logger.info(f"Attempting to process {len(messages)} messages...")
        for message in messages:
            processed_message = self.__process_message(message)
            self.__compile_statistics(processed_message)
            processed_messages.append(processed_message)
        self.__report_findings()
        return processed_messages
    
    def __process_message(self, message: str) -> dict[str, str]:
        """
        Private helper method for processing raw messages from kafka.

        Args:
            message (str): The message to be processed.

        Returns:
            dict[str, str]: A dictionary of strings, representing the message content.
        """
        self.logger.debug(f"Processing message: {message}")
        return ast.literal_eval(message)
    
    def __compile_statistics(self, processed_message: dict[str, str]):
        """
        Private helper method for processing raw messages from kafka.

        Args:
            processed_message (dict[str, str]): A dictionary of strings, representing a processed message's content.
        """
        if processed_message["user_id"] not in self.users:
            self.users.append(processed_message["user_id"])

    def __report_findings(self):
        """
        Private helper method for outputting statistical insights via the class's logger.
        """
        self.logger.info(f"There are {len(self.users)} unique users in the system...")