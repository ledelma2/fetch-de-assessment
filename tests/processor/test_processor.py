import ast
import pytest
from logging import Logger
from src.py.processor.processor import Processor
from src.py.processor.data.activity_data_manager import ActivityDataManager
from src.py.processor.data.device_data_manager import DeviceDataManager
from src.py.processor.data.ip_data_manager import IpDataManager
from src.py.processor.data.user_data_manager import UserDataManager
from unittest.mock import AsyncMock, MagicMock, patch

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

def test_process_message():
    # Arrange
    logger = Logger("consumer")
    raw_message = "{\"user_id\": \"424cdd21-063a-43a7-b91b-7ca1a833afae\", \"app_version\": \"2.3.0\", \"device_type\": \"android\", \"ip\": \"199.172.111.135\", \"locale\": \"RU\", \"device_id\": \"593-47-5928\", \"timestamp\":\"1694479551\"}"
    _sut = Processor(logger)
    # Act
    result = _sut.process_message(raw_message)
    # Assert
    assert ast.literal_eval(raw_message) == result

def test_process_message_with_missing_fields():
    # Arrange
    logger = Logger("consumer")
    raw_message = "{\"user_id\": \"424cdd21-063a-43a7-b91b-7ca1a833afae\", \"ip\": \"199.172.111.135\", \"device_id\": \"593-47-5928\", \"timestamp\":\"1694479551\"}"
    expected_message_raw = "{\"user_id\": \"424cdd21-063a-43a7-b91b-7ca1a833afae\", \"ip\": \"199.172.111.135\", \"device_id\": \"593-47-5928\", \"timestamp\":\"1694479551\", \"device_type\": \"unknown device\", \"locale\": \"unknown locale\", \"app_version\": \"unknown app version\"}"
    _sut = Processor(logger)
    # Act
    result = _sut.process_message(raw_message)
    # Assert
    assert ast.literal_eval(expected_message_raw) == result

@pytest.mark.asyncio
async def test_compile_statistics_async():
    # Arrange
    logger = Logger("consumer")
    activity_manager_mock = AsyncMock(spec=ActivityDataManager)
    device_manager_mock = AsyncMock(spec=DeviceDataManager)
    ip_manager_mock = AsyncMock(spec=IpDataManager)
    user_manager_mock = AsyncMock(spec=UserDataManager)
    processed_message = {"user_id": "424cdd21-063a-43a7-b91b-7ca1a833afae", "app_version": "2.3.0", "device_type": "android", "ip": "199.172.111.135", "locale": "RU", "device_id": "593-47-5928", "timestamp": "1694479551"}
    with (patch("src.py.processor.processor.ActivityDataManager", return_value=activity_manager_mock),
          patch("src.py.processor.processor.DeviceDataManager", return_value=device_manager_mock),
          patch("src.py.processor.processor.IpDataManager", return_value=ip_manager_mock),
          patch("src.py.processor.processor.UserDataManager", return_value=user_manager_mock)):
        _sut = Processor(logger)
        # Act
        await _sut.compile_statistics_async(processed_message)
        # Assert
        user_manager_mock.compile_user_data_async.assert_awaited_once_with("424cdd21-063a-43a7-b91b-7ca1a833afae", 1694479551, "593-47-5928")
        ip_manager_mock.compile_ip_data_async.assert_awaited_once_with("199.172.111.135", 1694479551)
        device_manager_mock.compile_device_data_async.assert_awaited_once_with("593-47-5928", "android", "2.3.0", "199.172.111.135", "RU")
        activity_manager_mock.compile_activity_data_async.assert_awaited_once_with("android", "2.3.0", "RU")

@pytest.mark.asyncio
async def test_process_messages_async():
    # Arrange
    logger = Logger("consumer")
    raw_messages = ["{\"user_id\": \"424cdd21-063a-43a7-b91b-7ca1a833afae\", \"app_version\": \"2.3.0\", \"device_type\": \"android\", \"ip\": \"199.172.111.135\", \"locale\": \"RU\", \"device_id\": \"593-47-5928\", \"timestamp\":\"1694479551\"}",
                    "{\"user_id\": \"test-id\", \"ip\": \"test-ip\", \"device_id\": \"test-device-id\", \"timestamp\":\"111111111\"}"]
    expected = [{"user_id": "424cdd21-063a-43a7-b91b-7ca1a833afae", "app_version": "2.3.0", "device_type": "android", "ip": "199.172.111.135", "locale": "RU", "device_id": "593-47-5928", "timestamp": "1694479551"},
                {"user_id": "test-id", "ip": "test-ip", "device_id": "test-device-id", "timestamp": "111111111", "device_type": "unknown device", "locale": "unknown locale", "app_version": "unknown app version"}]
    _sut = Processor(logger)
    # Act
    result = await _sut.process_messages_async(raw_messages)
    # Assert
    assert result == expected