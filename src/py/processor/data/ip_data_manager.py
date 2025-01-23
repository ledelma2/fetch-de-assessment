from logging import Logger

class IpDataManager:
    """
    Class for compiling and managing data related to ip addresses.

    Args:
        logger (Logger): The logger instance used to convey information for this class.

    Attributes:
        ip_logins (dict[str, list[int]]): Dictionary of lists denoting total logins from an ip address as the first item and most recent login as the second, with the ip as the key.
    """
    def __init__(self, logger: Logger):
        self.ip_logins: dict[str, list[int, int]] = {}
        self.logger = logger.getChild("ip_metric_manager")

    def compile_ip_data(self, ip_address: str, timestamp: int):
        """
        Method for compiling ip address data in the system.

        Args:
            ip_address (str): The ip address from the login attempt.
            timestamp (int): The timestamp of the login attempt.
        """
        # Add or update ip data based on if ip address exists
        if ip_address not in self.ip_logins:
            self.__add_new_ip_data(ip_address, timestamp)
        else:
            self.__update_ip_data(ip_address, timestamp)

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
        self.ip_logins[ip_address][0] = self.ip_logins[ip_address][0] + 1
        if timestamp > self.ip_logins[ip_address][1]:
            self.ip_logins[ip_address][1] = timestamp