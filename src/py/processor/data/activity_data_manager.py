from logging import Logger

class ActivityDataManager:
    """
    Class for compiling and managing data related to system activity.

    Args:
        logger (Logger): The logger instance used to convey information for this class.

    Attributes:
        version_activity (dict[str, dict[str, int]]): Dictionary of app versions and the total number of logins for each.
        locale_activity (dict[str, dict[str, int]]): Dictionary of locales and the total number of logins for each.
    """
    def __init__(self, logger: Logger):
        self.version_activity: dict[str, dict[str, int]] = {}
        self.locale_activity: dict[str, dict[str, int]] = {}
        self.logger = logger.getChild("activity_metric_manager")

    def compile_activity_data(self, device_type: str, app_version: str, locale: str):
        """
        Method for compiling general activity data in the system.

        Args:
            device_type (str): The type of the device being used.
            app_version (str): The version of the app being used on the device.
            locale (str): The locale of the device from the login attempt.
        """
        self.__compile_version_activity(device_type, app_version)
        self.__compile_locale_activity(device_type, locale)

    def __compile_version_activity(self, device_type: str, app_version: str):
        """
        Private helper method for compiling app version specific activity data in the system.

        Args:
            device_type (str): The type of the device being used.
            app_version (str): The version of the app being used on the device.
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

    def __compile_locale_activity(self, device_type: str, locale: str):
        """
        Private helper method for compiling specific locale activity data in the system.

        Args:
            device_type (str): The type of the device being used.
            locale (str): The locale of the device from the login attempt.
        """
        if locale not in self.locale_activity:
            # Initialize new dictionary with current device type entry at locale
            self.locale_activity[locale] = {device_type: 1}
        elif device_type not in self.locale_activity[locale]:
            # Create new device type entry at locale
            self.locale_activity[locale][device_type] = 1
        else:
            # Update device type entry at locale
            self.locale_activity[locale][device_type] = self.locale_activity[locale][device_type] + 1
