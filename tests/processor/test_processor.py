from unittest import TestCase
from unittest.mock import MagicMock, patch
from logging import Logger
from src.py.processor.processor import Processor
from src.py.constants import message_keys

def test_processor_initialization():
    # Arrange
    logger = MagicMock(spec=Logger)
    # Act
    _sut = Processor(logger)
    # Assert
    assert _sut.logger == logger.getChild("processor")
    assert _sut.activity_data_manager is not None
    assert _sut.activity_manager_async_lock is not None
    assert _sut.device_data_manager is not None
    assert _sut.device_manager_async_lock is not None
    assert _sut.ip_data_manager is not None
    assert _sut.ip_manager_async_lock is not None
    assert _sut.user_data_manager is not None
    assert _sut.user_manager_async_lock is not None