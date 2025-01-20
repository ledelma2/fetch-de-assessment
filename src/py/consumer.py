from ingestor.ingestor import Ingestor
from messenger.messenger import Messenger
import os
import processor
import signal
import traceback

"""
This is the main looping block for the data pipeline. This module polls/ingests a message from
a kafka broker, processes the message, and then stores the processed message in a new topic.
"""

# Flag to control the main loop
running = True

def signal_handler(sig, frame):
    """
    Handle termination signals to allow graceful shutdown.
    """
    global running
    print("Received termination signal. Shutting down...")
    running = False


def main():
    """
    Main program loop for running the consumer.
    """

    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    with (Ingestor(os.environ["CONSUMER_BOOTSTRAP_SERVER"], os.environ["CONSUMER_GROUP_ID"], os.environ["CONSUMER_AUTO_OFFSET_RESET"], os.environ["CONSUMER_KAFKA_TOPIC"]) as ingstr,
          Messenger(os.environ["PRODUCER_BOOTSTRAP_SERVER"], os.environ["PRODUCER_CLIENT_ID"], os.environ["PRODUCER_KAFKA_TOPIC"]) as msngr):
        while running:
            # Ingest message from ingestor
            message = ingstr.consume_message(int(os.environ["CONSUMER_MESSAGE_LIMIT"]), float(os.environ["CONSUMER_WAIT_TIME"]))

            if message:
                # Send message to processor for processing

                # Store processed message in new topic with messenger
                msngr.produce_message(message, float(os.environ["PRODUCER_WAIT_TIME"]))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An exception occurred...")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        print(f"Arguments: {e.args}")
        print("Traceback:")
        traceback.print_exc()