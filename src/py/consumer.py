from ingestor.ingestor import Ingestor
import messenger
import os
import processor
import signal
import traceback

"""
This is the main consumer class for the data pipeline. This class polls/ingests a message from
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

    with Ingestor(os.environ['BOOTSTRAP_SERVER'], os.environ['CONSUMER_GROUP_ID'], os.environ['AUTO_OFFSET_RESET'], os.environ['USER_LOGIN_TOPIC']) as ingstr:
        while running:
            # Ingest message from ingestor
            message = ingstr.consume_message()
            print(message)

            # Send message to processor for processing

            # Store processed message in new topic with messenger

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