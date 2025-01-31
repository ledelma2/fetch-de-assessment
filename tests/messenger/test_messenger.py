from unittest import TestCase
from unittest.mock import MagicMock, patch
from logging import Logger
from src.py.messenger.messenger import Messenger
from confluent_kafka import KafkaError, Message, Producer

def test_initialization():
    # Arrange
    logger_mock = MagicMock(spec=Logger)
    with patch("src.py.messenger.messenger.Producer") as MockProducer:
        # Act
        _sut = Messenger(logger_mock, "broker:9092", "test-client-id", "test-topic")

    # Assert
    MockProducer.assert_called_once_with({
        "bootstrap.servers": "broker:9092",
        "client.id": "test-client-id"
    })
    assert _sut.topic_name == "test-topic"
    assert _sut.logger == logger_mock.getChild("messenger")

def test_messenger_context_manager():
    # Arrange
    logger = Logger("consumer")
    producer_mock = MagicMock(spec=Producer)
    with patch("src.py.messenger.messenger.Producer", return_value=producer_mock):
        # Act
        with Messenger(logger, "broker:9092", "test-client-id", "test-topic") as _sut:
            # Assert
            producer_mock.flush.assert_called_once()
        producer_mock.purge.assert_called_once()
        producer_mock.flush.call_count == 2

class TestProduceMessageAndCallback(TestCase):
    def test_produce_message_and_callback(self):
        # Arrange
        logger = Logger("consumer")
        messages = [{"key": "value"}]
        wait_time = 1.1
        producer_mock = MagicMock(spec=Producer)
        success_message_mock = MagicMock(spec=Message)
        success_message_mock.value.return_value = str({"key": "value"}).encode("utf-8")
        success_message_mock.topic.return_value = "test-topic"
        success_message_mock.partition.return_value = 0
        with patch("src.py.messenger.messenger.Producer", return_value=producer_mock):
            _sut = Messenger(logger, "broker:9092", "test-client-id", "test-topic")
            with self.assertLogs(_sut.logger, level="DEBUG") as lcm:
                # Act
                _sut.produce_messages(messages, wait_time)
                _sut.callback(None, success_message_mock)
                # Assert
                self.assertTrue("DEBUG:consumer.messenger:Message '{'key': 'value'}' successfully delivered to topic test-topic and partition 0" in lcm.output)
        producer_mock.poll.assert_called_once_with(1.1)
        producer_mock.produce.assert_called_once_with("test-topic", str({"key": "value"}).encode("utf-8"), callback=_sut.callback)
        producer_mock.flush.assert_called_once()

    def test_produce_message_raises(self):
        # Arrange
        logger = Logger("consumer")
        messages = [{"key": "value"}]
        wait_time = 1.1
        producer_mock = MagicMock(spec=Producer)
        producer_mock.produce.side_effect = Exception("Some fatal error")
        with patch("src.py.messenger.messenger.Producer", return_value=producer_mock):
            _sut = Messenger(logger, "broker:9092", "test-client-id", "test-topic")
            with (self.assertLogs(_sut.logger, level="ERROR") as lcm,
                  self.assertRaises(Exception) as ecm):
                # Act
                _sut.produce_messages(messages, wait_time)
            # Assert
            self.assertEqual(["CRITICAL:consumer.messenger:Fatal error producing messages in messenger: Some fatal error"], lcm.output)
            self.assertEqual("Some fatal error", str(ecm.exception))

    def test_callback_errored_message(self):
        # Arrange
        logger = Logger("consumer")
        producer_mock = MagicMock(spec=Producer)
        fail_message_mock = MagicMock(spec=Message)
        fail_message_mock.value.return_value = str({"key": "value"}).encode("utf-8")
        fail_message_mock.topic.return_value = "test-topic"
        fail_message_mock.partition.return_value = 0
        kafka_error_mock = MagicMock(spec=KafkaError)
        kafka_error_mock.str.return_value = "Some error"
        kafka_error_mock.fatal.return_value = False
        with patch("src.py.messenger.messenger.Producer", return_value=producer_mock):
            _sut = Messenger(logger, "broker:9092", "test-client-id", "test-topic")
            with self.assertLogs(_sut.logger, level="ERROR") as lcm:
                # Act
                _sut.callback(kafka_error_mock, fail_message_mock)
                # Assert
                self.assertEqual(["ERROR:consumer.messenger:Failed to deliver message '{'key': 'value'}' to topic test-topic and partition 0: Some error"], lcm.output)

    def test_callback_errored_message_raises(self):
        # Arrange
        logger = Logger("consumer")
        producer_mock = MagicMock(spec=Producer)
        fail_message_mock = MagicMock(spec=Message)
        fail_message_mock.value.return_value = str({"key": "value"}).encode("utf-8")
        fail_message_mock.topic.return_value = "test-topic"
        fail_message_mock.partition.return_value = 0
        kafka_error_mock = MagicMock(spec=KafkaError)
        kafka_error_mock.str.return_value = "Some fatal error"
        kafka_error_mock.fatal.return_value = True
        with patch("src.py.messenger.messenger.Producer", return_value=producer_mock):
            _sut = Messenger(logger, "broker:9092", "test-client-id", "test-topic")
            with (self.assertLogs(_sut.logger, level="ERROR") as lcm,
                  self.assertRaises(Exception) as ecm):
                # Act
                _sut.callback(kafka_error_mock, fail_message_mock)
            # Assert
            self.assertEqual(["ERROR:consumer.messenger:Failed to deliver message '{'key': 'value'}' to topic test-topic and partition 0: Some fatal error"], lcm.output)
            self.assertEqual("Some fatal error", str(ecm.exception))