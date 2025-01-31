from src.py.constants import message_keys
from logging import Logger

class DeviceDataManager:
    """
    Class for compiling and managing data related to devices.

    Args:
        logger (Logger): The logger instance used to convey information for this class.

    Attributes:
        devices (dict[str, dict[str, str]]): Dictionary of dictionaries denoting device information, with the device id as the key.
    """
    def __init__(self, logger: Logger):
        self.devices: dict[str, dict[str, str]] = {}
        self.logger = logger.getChild("device_metric_manager")

    async def compile_device_data_async(self, device_id: str, device_type: str, app_version: str, ip_address: str,  locale: str):
        """
        Mehtod for compiling general device data into the system.

        Args:
            device_id (str): The identifier for the device.
            device_type (str): The type of the device being used.
            app_version (str): The version of the app being used on the device.
            ip_address (str): The ip address of the device's from the login attempt.
            locale (str): The locale of the device from the login attempt.
        """
        # Add or update device data based on if device exists
        if device_id not in self.devices:
            self.__add_new_device_data(device_id, device_type, app_version, ip_address, locale)
        else:
            self.__update_device_data(device_id, device_type, app_version, ip_address, locale)

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