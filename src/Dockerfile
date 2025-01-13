# Use the latest alpine image as the base since alpine is super lightweight
FROM alpine:latest

# Install python and pip
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /usr/src

# Copy pipeline source code
COPY py .