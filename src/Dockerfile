# Use the latest python:slim image as this base is more lightweight than a full python image
FROM python:slim

# Install required libraries and dependencies
RUN apt-get update && apt-get install -y \
    librdkafka-dev gcc g++ && \
    pip install --no-cache-dir confluent-kafka && \
    apt-get remove -y gcc g++ && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /usr/src

# Copy pipeline source code
COPY py .

# Run the consumer
CMD ["python3", "data_pipeline.py"]

# Metadata
LABEL maintainer="Liam Edelman"
LABEL version="latest"
LABEL description="Image for running fetch-de-assessment-consumer"