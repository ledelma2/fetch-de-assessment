import ingestor
import messenger
import processor

"""
This is the main consumer class for the data pipeline. This class polls/ingests a message from
a kafka broker, processes the message, and then stores the processed message in a new topic.
"""

#ingest message from ingestor

#send message to processor for processing

#store processed message in new topic with messenger