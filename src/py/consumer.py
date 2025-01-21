from ingestor.ingestor import Ingestor
from messenger.messenger import Messenger
from processor.processor import Processor
import logging
import os
import signal
import traceback

"""
This is the main looping block for the data pipeline. This module polls/ingests a message from
a kafka broker, processes the message, and then stores the processed message in a new topic.
"""

# Flag to control the main loop
running = True

# Setup logger with console handler and formatting
logger = logging.getLogger("consumer")
logger.setLevel(os.environ["LOGGER_LEVEL"])
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s | %(name)s] %(asctime)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

def signal_handler(sig, frame):
    """
    Handle termination signals to allow graceful shutdown.
    """
    global running
    logger.info("Received termination signal. Shutting down...")
    running = False

def main():
    """
    Main program loop for running the consumer.
    """

    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    with (Ingestor(logger, os.environ["CONSUMER_BOOTSTRAP_SERVER"], os.environ["CONSUMER_GROUP_ID"], os.environ["CONSUMER_AUTO_OFFSET_RESET"], os.environ["CONSUMER_KAFKA_TOPIC"]) as ingstr,
          Messenger(logger, os.environ["PRODUCER_BOOTSTRAP_SERVER"], os.environ["PRODUCER_CLIENT_ID"], os.environ["PRODUCER_KAFKA_TOPIC"]) as msngr,
          Processor(logger) as prcsr):
        while running:
            # Ingest message from ingestor
            logger.debug("Ingesting messages from kafka...")
            messages = ingstr.consume_messages(int(os.environ["CONSUMER_MESSAGE_LIMIT"]), float(os.environ["CONSUMER_WAIT_TIME"]))

            if messages:
                # Send message to processor for processing
                logger.debug(f"Processing {len(messages)} ingested messages...")
                processed_messages = prcsr.process_messages_and_report_findings(messages)

                # Store processed message in new topic with messenger
                logger.debug(f"Sending {len(processed_messages)} processed messages to kafka...")
                msngr.produce_messages(processed_messages, float(os.environ["PRODUCER_WAIT_TIME"]))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical("An exception occurred...")
        logger.critical(f"Type: {type(e).__name__}")
        logger.critical(f"Message: {e}")
        logger.critical(f"Arguments: {e.args}")
        logger.critical("Traceback:")
        traceback.print_exc()