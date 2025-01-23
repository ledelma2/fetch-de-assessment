from logging import Logger

class UserDataManager:
    """
    Class for compiling and managing data related to users.

    Args:
        logger (Logger): The logger instance used to convey information for this class.

    Attributes:
        user_logins (dict[str, list[int]]): Dictionary of lists denoting total user logins as the first item and most recent login as the second, with the user_id as the key.
        users_and_devices (dict[str, list[str]]): Dictionary of lists denoting user devices, with the user_id as the key.
    """
    def __init__(self, logger: Logger):
        self.user_logins: dict[str, list[int, int]] = {}
        self.users_and_devices: dict[str, list[str]] = {}
        self.logger = logger.getChild("user_metric_manager")

    async def compile_user_data_async(self, user_id: str, timestamp: int, device_id: str):
        """
        Method for compiling user data into the system.

        Args:
            user_id (str): The identifier for the user.
            timestamp (int): The timestamp of the login attempt.
            device_id (str): The identifier for the device used in the login attempt.
        """
        # Add or update user data based on if user exists
        if user_id not in self.users_and_devices:
            self.__add_new_user_data(user_id, timestamp, device_id)
        else:
            self.__update_user_data(user_id, timestamp, device_id)

    def __add_new_user_data(self, user_id: str, timestamp: int, device_id: str):
        """
        Private helper method for adding new user data to the system.

        Args:
            user_id (str): The identifier for the user.
            timestamp (int): The timestamp of the login attempt.
            device_id (str): The identifier for the device used in the login attempt.
        """
        # Create a user_logins entry
        self.user_logins[user_id] = [1, timestamp]

        # Create a user_and_devices entry
        self.users_and_devices[user_id] = [device_id]

    def __update_user_data(self, user_id: str, timestamp: int, device_id: str):
        """
        Private helper method for updating user data in the system.

        Args:
            user_id (str): The identifier for the user.
            timestamp (int): The timestamp of the login attempt.
            device_id (str): The identifier for the device used in the login attempt.
        """
        # Update user login total and, if needed, most recent login
        self.user_logins[user_id][0] = self.user_logins[user_id][0] + 1
        if timestamp > self.user_logins[user_id][1]:
            self.user_logins[user_id][1] = timestamp

        # Check for new user device
        if device_id not in self.users_and_devices[user_id]:
            self.users_and_devices[user_id].append(device_id)