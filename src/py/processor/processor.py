import ast
import asyncio
from concurrent.futures import ProcessPoolExecutor
from constants import message_keys
from .data.activity_data_manager import ActivityDataManager
from .data.device_data_manager import DeviceDataManager
from .data.ip_data_manager import IpDataManager
from .data.user_data_manager import UserDataManager
from datetime import datetime
from logging import Logger

class Processor:
    """
    Processor class for parsing/cleaning messages and making analytical insights.

    Args:
        logger (Logger): The logger instance used to convey information for this class.

    Attributes:
        activity_data_manager (ActivityDataManager): The data manager for managing activity data.
        device_data_manager (DeviceDataManager): The data manager for managing device data.
        ip_data_manager (IpDataManager): The data manager for managing ip data.
        user_data_manager (UserDataManager): The data manager for managing user data.
    """
    def __init__(self, logger: Logger):
        self.logger = logger.getChild("processor")
        self.activity_data_manager = ActivityDataManager(self.logger)
        self.device_data_manager = DeviceDataManager(self.logger)
        self.ip_data_manager = IpDataManager(self.logger)
        self.user_data_manager = UserDataManager(self.logger)
        self.activity_manager_async_lock = asyncio.Lock()
        self.device_manager_async_lock = asyncio.Lock()
        self.ip_manager_async_lock = asyncio.Lock()
        self.user_manager_async_lock = asyncio.Lock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    async def process_messages_and_report_findings_async(self, messages: list[str]) -> list[dict[str, str]]:
        """
        Asynchronously and concurrently processes raw messages from kafka and reports some relevant findings based on the messages' contents.

        Args:
            messages (list[str]): A list of messages, as strings, to be processed.

        Returns:
            list[dict[str, str]]: A list of processed messages as dictionaries.
        """
        self.logger.info(f"Attempting to process {len(messages)} messages...")
        processed_messages = []

        # Process messages quickly with multiprocessing
        with ProcessPoolExecutor() as executor:
            processed_messages = list(executor.map(self.process_message, messages))

        # Create tasks to run concurrently in background
        compile_stat_tasks = []
        for processed_message in processed_messages:
            compile_stat_tasks.append(asyncio.create_task(self.compile_statistics_async(processed_message)))

        await asyncio.gather(*compile_stat_tasks)

        self.report_findings()
        return processed_messages
    
    def process_message(self, message: str) -> dict[str, str]:
        """
        Method for processing a single raw message from kafka.

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
    
    async def compile_statistics_async(self, processed_message: dict[str, str]):
        """
        Asynchronously compiles statistics for the ingested the processed message.

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

        # Wait for resource to unlock, then compile user statistics
        async with self.user_manager_async_lock:
            await self.user_data_manager.compile_user_data_async(user_id, timestamp, device_id)

        # Wait for resource to unlock, then compile device statistics
        async with self.device_manager_async_lock:
            await self.device_data_manager.compile_device_data_async(device_id, device_type, app_version, ip_address, locale)

        # Wait for resource to unlock, then compile ip statistics
        async with self.ip_manager_async_lock:
            await self.ip_data_manager.compile_ip_data_async(ip_address, timestamp)

        # Wait for resource to unlock, then compile activity statistics
        async with self.activity_manager_async_lock:
            await self.activity_data_manager.compile_activity_data_async(device_type, app_version, locale)

    def report_findings(self):
        """
        Method for outputting statistical insights via the class's internal logger.
        """
        # Report total unique users in the system
        self.logger.info(f"There are {len(self.user_data_manager.users_and_devices)} unique users in the system...")

        # Report total unique devices in the system
        self.logger.info(f"There are {len(self.device_data_manager.devices)} unique devices in the system...")

        # Report 10 most active users
        active_user_msg = f"Most active users in the system:\n"
        most_active_users = dict(sorted(self.user_data_manager.user_logins.items(), key=lambda item: item[1][0], reverse=True)[:10])
        for user, login_data in most_active_users.items():
            active_user_msg = active_user_msg + f"\tUser: {user}\n"
            active_user_msg = active_user_msg + f"\t\tTotal Logins: {login_data[0]}\n"
            active_user_msg = active_user_msg + f"\t\tLast Login: {datetime.fromtimestamp(login_data[1])}\n"
        self.logger.info(active_user_msg)

        # Report 10 most active ip's
        active_ip_msg = f"Most active ip's in the system:\n"
        most_active_ips = dict(sorted(self.ip_data_manager.ip_logins.items(), key=lambda item: item[1][0], reverse=True)[:10])
        for locale, login_data in most_active_ips.items():
            active_ip_msg = active_ip_msg + f"\tIP Address: {locale}\n"
            active_ip_msg = active_ip_msg + f"\t\tTotal Logins: {login_data[0]}\n"
            active_ip_msg = active_ip_msg + f"\t\tLast Login: {datetime.fromtimestamp(login_data[1])}\n"
        self.logger.info(active_ip_msg)

        # Report version activity
        self.logger.info(f"App version activity: {self.activity_data_manager.version_activity}")

        # Report locale activity
        self.logger.info(f"Locale activity: {self.activity_data_manager.locale_activity}")