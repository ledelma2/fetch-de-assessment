from unittest import TestCase
from unittest.mock import MagicMock, patch
from logging import Logger
from src.py.ingestor.ingestor import Ingestor
from confluent_kafka import Consumer, KafkaError, Message

def test_ingestor_initialization():
    # Arrange
    logger = MagicMock(spec=Logger)
    with patch("src.py.ingestor.ingestor.Consumer") as MockConsumer:
        # Act
        _sut = Ingestor(logger, "broker:9092", "test-group", "earliest", "test-topic")
        # Assert
        MockConsumer.assert_called_once_with({
            "bootstrap.servers": "broker:9092",
            "group.id": "test-group",
            "auto.offset.reset": "earliest"
        })
        assert _sut.topic_name == "test-topic"
        assert _sut.logger == logger.getChild("ingestor")

def test_ingestor_context_manager():
    # Arrange
    logger = MagicMock(spec=Logger)
    consumer_mock = MagicMock(spec=Consumer)
    with patch("src.py.ingestor.ingestor.Consumer", return_value=consumer_mock):
        # Act
        with Ingestor(logger, "broker:9092", "test-group", "earliest", "test-topic") as _sut:
            # Assert
            consumer_mock.subscribe.assert_called_once_with(["test-topic"])
        consumer_mock.close.assert_called_once()

def test_ingestor_consume_messages():
    # Arrange
    logger = MagicMock(spec=Logger)
    consumer_mock = MagicMock(spec=Consumer)
    message_mock = MagicMock(spec=Message)
    message_mock.value.return_value = b"test message"
    message_mock.error.return_value = None
    with patch("src.py.ingestor.ingestor.Consumer", return_value=consumer_mock):
        _sut = Ingestor(logger, "broker:9092", "test-group", "earliest", "test-topic")
        consumer_mock.consume.return_value = [message_mock]
        # Act
        messages = _sut.consume_messages(message_limit=1)
        # Assert
        consumer_mock.consume.assert_called_once_with(num_messages=1, timeout=1.0)
        assert messages == ["test message"]

class TestErroredConsumeMessages(TestCase):
    def test_ingestor_consume_messages_with_error(self):
        # Arrange
        logger = Logger("consumer")
        consumer_mock = MagicMock(spec=Consumer)
        message_mock = MagicMock(spec=Message)
        message_mock.value.return_value = "corrupted message".encode("utf-8")
        message_mock.error.return_value = KafkaError(KafkaError.MEMBER_ID_REQUIRED, "Some error", fatal=False)
        message_mock.error.str.return_value = "Some error"
        with patch("src.py.ingestor.ingestor.Consumer", return_value=consumer_mock):
            _sut = Ingestor(logger, "broker:9092", "test-group", "earliest", "test-topic")
            consumer_mock.consume.return_value = [message_mock]
            with self.assertLogs(_sut.logger, level="ERROR") as cm:
                # Act
                messages = _sut.consume_messages(message_limit=1)
                # Assert
                consumer_mock.consume.assert_called_once()
                self.assertEqual(cm.output, ["ERROR:consumer.ingestor:Error consuming message corrupted message: Some error"])
                assert messages == []

    def test_ingestor_consume_partial_error_messages(self):
        # Arrange
        logger = Logger("consumer")
        consumer_mock = MagicMock(spec=Consumer)
        success_message_mock = MagicMock(spec=Message)
        success_message_mock.value.return_value = "test message".encode("utf-8")
        success_message_mock.error.return_value = None
        error_message_mock = MagicMock(spec=Message)
        error_message_mock.value.return_value = "corrupted message".encode("utf-8")
        error_message_mock.error.return_value = KafkaError(KafkaError.MEMBER_ID_REQUIRED, "Some error", fatal=False)
        with patch("src.py.ingestor.ingestor.Consumer", return_value=consumer_mock):
            _sut = Ingestor(logger, "broker:9092", "test-group", "earliest", "test-topic")
            consumer_mock.consume.return_value = [success_message_mock, error_message_mock]
            with self.assertLogs(_sut.logger, level="ERROR") as cm:
                # Act
                messages = _sut.consume_messages(message_limit=2)
                # Assert
                consumer_mock.consume.assert_called_once()
                self.assertEqual(cm.output, ["ERROR:consumer.ingestor:Error consuming message corrupted message: Some error"])
                assert messages == ["test message"]

    def test_ingestor_consume_messages_with_fatal_error_raises(self):
            # Arrange
            logger = Logger("consumer")
            consumer_mock = MagicMock(spec=Consumer)
            message_mock = MagicMock(spec=Message)
            message_mock.value.return_value = "corrupted message".encode("utf-8")
            message_mock.error.return_value = KafkaError(KafkaError.MEMBER_ID_REQUIRED, "Some fatal error", fatal=True)
            message_mock.error.str.return_value = "Some fatal error"
            with patch("src.py.ingestor.ingestor.Consumer", return_value=consumer_mock):
                _sut = Ingestor(logger, "broker:9092", "test-group", "earliest", "test-topic")
                consumer_mock.consume.return_value = [message_mock]
                with (self.assertLogs(_sut.logger, level="ERROR") as lcm,
                      self.assertRaises(Exception) as ecm):
                    # Act
                    messages = _sut.consume_messages(message_limit=1)
                    # Assert
                    consumer_mock.consume.assert_called_once()
                self.assertEqual(lcm.output, ["ERROR:consumer.ingestor:Error consuming message corrupted message: Some fatal error", "CRITICAL:consumer.ingestor:Fatal error consuming messages in ingestor: Some fatal error"])
                self.assertEqual("Some fatal error", str(ecm.exception))

    def test_ingestor_consume_partial_fatal_error_messages_raises(self):
        # Arrange
        logger = Logger("consumer")
        consumer_mock = MagicMock(spec=Consumer)
        success_message_mock = MagicMock(spec=Message)
        success_message_mock.value.return_value = "test message".encode("utf-8")
        success_message_mock.error.return_value = None
        error_message_mock = MagicMock(spec=Message)
        error_message_mock.value.return_value = "corrupted message".encode("utf-8")
        error_message_mock.error.return_value = KafkaError(KafkaError.MEMBER_ID_REQUIRED, "Some fatal error", fatal=True)
        with patch("src.py.ingestor.ingestor.Consumer", return_value=consumer_mock):
            _sut = Ingestor(logger, "broker:9092", "test-group", "earliest", "test-topic")
            consumer_mock.consume.return_value = [success_message_mock, error_message_mock]
            with (self.assertLogs(_sut.logger, level="ERROR") as lcm,
                  self.assertRaises(Exception) as ecm):
                # Act
                messages = _sut.consume_messages(message_limit=2)
                # Assert
                consumer_mock.consume.assert_called_once()
            self.assertEqual(lcm.output, ["ERROR:consumer.ingestor:Error consuming message corrupted message: Some fatal error", "CRITICAL:consumer.ingestor:Fatal error consuming messages in ingestor: Some fatal error"])
            self.assertEqual("Some fatal error", str(ecm.exception))
