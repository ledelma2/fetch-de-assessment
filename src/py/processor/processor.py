import ast
from constants import message_keys
from datetime import datetime
from logging import Logger

class Processor:
    """
    Processor class for parsing/cleaning messages and making analytical insights.

    Args:
        logger (Logger): The logger instance used to convey information for this class.

    Attributes:
        user_logins (dict[str, list[int]]): Dictionary of lists denoting total user logins as the first item and most recent login as the second, with the user_id as the key.
        users_and_devices (dict[str, list[str]]): Dictionary of lists denoting user devices, with the user_id as the key.
        devices (dict[str, dict[str, str]]): Dictionary of dictionaries denoting device information, with the device id as the key.
        ip_logins (dict[str, list[int]]): Dictionary of lists denoting total logins from an ip address as the first item and most recent login as the second, with the ip as the key.
        version_activity (dict[str, dict[str, int]]): Dictionary of app versions and the total number of logins for each.
        locale_activity (dict[str, dict[str, int]]): Dictionary of locales and the total number of logins for each.
    """
    def __init__(self, logger: Logger):
        self.user_logins: dict[str, list[int, int]] = {}
        self.users_and_devices: dict[str, list[str]] = {}
        self.devices: dict[str, dict[str, str]] = {}
        self.ip_logins: dict[str, list[int, int]] = {}
        self.version_activity: dict[str, dict[str, int]] = {}
        self.locale_activity: dict[str, dict[str, int]] = {}
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
            processed_message = self.process_message(message)
            self.compile_statistics(processed_message)
            processed_messages.append(processed_message)
        self.report_findings()
        return processed_messages
    
    def process_message(self, message: str) -> dict[str, str]:
        """
        Helper method for processing raw messages from kafka.

        Args:
            message (str): The message to be processed.

        Returns:
            dict[str, str]: A dictionary of strings, representing the message content.
        """
        processed_message = {}
        self.logger.debug(f"Processing message: {message}")

        # Convert message into dictionary
        processed_message = ast.literal_eval(message)

        # Check for missing device type
        if message_keys.DEVICE_TYPE not in processed_message:
            processed_message[message_keys.DEVICE_TYPE] = "unknown device"

        # Check for missing locale
        if message_keys.LOCALE not in processed_message:
            processed_message[message_keys.LOCALE] = "unknown locale"

        # Check for missing app version
        if message_keys.APP_VERSION not in processed_message:
            processed_message[message_keys.APP_VERSION] = "unknown app version"

        return processed_message
    
    def compile_statistics(self, processed_message: dict[str, str]):
        """
        Helper method for processing raw messages from kafka.

        Args:
            processed_message (dict[str, str]): A dictionary of strings, representing a processed message's content.
        """
        user_id = processed_message[message_keys.USER_ID]
        timestamp = int(processed_message[message_keys.TIMESTAMP])
        device_id = processed_message[message_keys.DEVICE_ID]
        device_type = processed_message[message_keys.DEVICE_TYPE]
        app_version = processed_message[message_keys.APP_VERSION]
        ip_address = processed_message[message_keys.IP_ADDRESS]
        locale = processed_message[message_keys.LOCALE]
        # Compile user statistics
        if user_id not in self.users_and_devices:
            self.__add_new_user_data(user_id, timestamp, device_id)
        else:
            self.__update_user_data(user_id, timestamp, device_id)

        # Compile device statistics
        if device_id not in self.devices:
            self.__add_new_device_data(device_id, device_type, app_version, ip_address, locale)
        else:
            self.__update_device_data(device_id, device_type, app_version, ip_address, locale)

        # Compile ip statistics
        if ip_address not in self.ip_logins:
            self.__add_new_ip_data(ip_address, timestamp)
        else:
            self.__update_ip_data(ip_address, timestamp)

        # Compile activity data
        self.__compile_activity_data(device_type, app_version, locale)

    def report_findings(self):
        """
        Helper method for outputting statistical insights via the class's logger.
        """
        # Report total unique users in the system
        self.logger.info(f"There are {len(self.users_and_devices)} unique users in the system...")

        # Report 10 most active users
        active_user_msg = f"Most active users in the system:\n"
        most_active_users = dict(sorted(self.user_logins.items(), key=lambda item: item[1][0], reverse=True)[:10])
        for user, login_data in most_active_users.items():
            active_user_msg = active_user_msg + f"\tUser: {user}\n"
            active_user_msg = active_user_msg + f"\t\tTotal Logins: {login_data[0]}\n"
            active_user_msg = active_user_msg + f"\t\tLast Login: {datetime.fromtimestamp(login_data[1])}\n"
        self.logger.info(active_user_msg)

        # Report 10 most active ip's
        active_ip_msg = f"Most active ip's in the system:\n"
        most_active_ips = dict(sorted(self.ip_logins.items(), key=lambda item: item[1][0], reverse=True)[:10])
        for locale, login_data in most_active_ips.items():
            active_ip_msg = active_ip_msg + f"\IP Address: {locale}\n"
            active_ip_msg = active_ip_msg + f"\t\tTotal Logins: {login_data[0]}\n"
            active_ip_msg = active_ip_msg + f"\t\tLast Login: {datetime.fromtimestamp(login_data[1])}\n"
        self.logger.info(active_ip_msg)

        # Report version activity
        self.logger.info(f"App version activity: {self.version_activity}")

        # Report locale activity
        self.logger.info(f"Locale activity: {self.locale_activity}")

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

    def __add_new_device_data(self, device_id: str, device_type: str, app_version: str, ip_address: str,  locale: str):
        """
        Private helper method for adding new device data to the system.

        Args:
            device_id (str): The identifier for the device.
            device_type (str): The type of the device being used.
            app_version (str): The version of the app being used on the device.
            ip_address (str): The ip address of the device's from the login attempt.
            locale (str): The locale of the device from the login attempt.
        """
        device_data = {message_keys.DEVICE_TYPE: device_type, 
                       message_keys.APP_VERSION: app_version,
                       message_keys.IP_ADDRESS: ip_address,
                       message_keys.LOCALE: locale}
        self.devices[device_id] = device_data

    def __update_device_data(self, device_id: str, device_type: str, app_version: str, ip_address: str,  locale: str):
        """
        Private helper method for updating device data in the system.

        Args:
            device_id (str): The identifier for the device.
            device_type (str): The type of the device being used.
            app_version (str): The version of the app being used on the device.
            ip_address (str): The ip address of the device's from the login attempt.
            locale (str): The locale of the device from the login attempt.
        """
        if self.devices[device_id][message_keys.DEVICE_TYPE] is not device_type:
            self.devices[device_id][message_keys.DEVICE_TYPE] = device_type

        if self.devices[device_id][message_keys.APP_VERSION] is not app_version:
            self.devices[device_id][message_keys.APP_VERSION] = app_version

        if self.devices[device_id][message_keys.IP_ADDRESS] is not ip_address:
            self.devices[device_id][message_keys.IP_ADDRESS] = ip_address

        if self.devices[device_id][message_keys.LOCALE] is not locale:
            self.devices[device_id][message_keys.LOCALE] = locale

    def __add_new_ip_data(self, ip_address: str, timestamp: int):
        """
        Private helper method for adding new ip address data in the system.

        Args:
            ip_address (str): The ip address from the login attempt.
            timestamp (int): The timestamp of the login attempt.
        """
        self.ip_logins[ip_address] = [1, timestamp]

    def __update_ip_data(self, ip_address: str, timestamp: int):
        """
        Private helper method for updating ip address data in the system.

        Args:
            ip_address (str): The ip address from the login attempt.
            timestamp (int): The timestamp of the login attempt.
        """
        # Update ip address login total and, if needed, most recent login
        self.user_logins[ip_address][0] = self.user_logins[ip_address][0] + 1
        if timestamp > self.user_logins[ip_address][1]:
            self.user_logins[ip_address][1] = timestamp

    def __compile_activity_data(self, device_type: str, app_version: str, locale: str):
        """
        Private helper method for compiling general activity data in the system.

        Args:
            device_type (str): The type of the device being used.
            app_version (str): The version of the app being used on the device.
            locale (str): The locale of the device from the login attempt.
        """
        if app_version not in self.version_activity:
            # Initialize new dictionary with current device type entry at app version
            self.version_activity[app_version] = {device_type: 1}
        elif device_type not in self.version_activity[app_version]:
            # Create new device type entry at app version
            self.version_activity[app_version][device_type] = 1
        else:
            # Update device type entry at app version
            self.version_activity[app_version][device_type] = self.version_activity[app_version][device_type] + 1

        if locale not in self.locale_activity:
            # Initialize new dictionary with current device type entry at locale
            self.locale_activity[locale] = {device_type: 1}
        elif device_type not in self.locale_activity[locale]:
            # Create new device type entry at locale
            self.locale_activity[locale][device_type] = 1
        else:
            # Update device type entry at locale
            self.locale_activity[locale][device_type] = self.locale_activity[locale][device_type] + 1