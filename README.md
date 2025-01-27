# fetch-de-assessment
 Data Engineer Assessment Project for Fetch Rewards

# Instructions

## General Setup
- Clone the repository to a local directory
- Download and install the latest version of Docker Desktop
    - Optionally, the standalone Docker Engine and Docker Compose Tool can be used instead of the Desktop app, though additional setup/debugging may be required 
- Verify the Docker CLI commands have been added to your system PATH
    - This can be done with the `docker help` command from a terminal window
- Download and install the latest version of Python 3
- Verify the Python CLI commands have been added to your system PATH
    - For windows users, this can be done with the `python -h` command from a terminal window
    - For Mac/Linux users, this can be done with the `python3 -h` command from a terminal window

## Additional Setup for Non-Windows Users
- Verify the `jq` package is installed and accesible through the command line
- If running on linux verify `gnome-terminal` is installed and accesible through the command line

## Running the Pipeline
- Start the Docker Engine by launching the Docker Desktop app or running the command `sudo systemctl start docker` from a terminal window
- Verify the docker engine is up, running, and accessible with the `docker info` command
- With administrator priveleges open a terminal, command prompt, or powershell window and navigate to the cloned repository
- Run the `run_pipeline.py` python script to begin enviornment setup
    - For Windows the command is `python run_pipeline.py`
    - For Mac/Linux the command is `python3 run_pipeline.py`

## TODO
- [x] Create single point of entry script
    - Python3
    - [x] Runs the setup for Windows
    - [x] Runs the setup for other OS's
    - [x] Shifts control to specific OS shell script
- [x] Add automation for enviornment setup
    - CLI Scripts with config files and enviornment variables
    - Bash for linux/mac
    - Powershell for windows
    - [x] docker-compose.networks.yml
        - [x] kafka-zookeeper-network
        - [x] kafka-producer-network
        - [x] kafka-consumer-network
    - [x] docker-compose.zookeeper.yml
        - [x] Add health check
    - [x] docker-compose.kafka.yml
        - [x] Add health check
        - [x] Create topics
            - [x] user-login
            - [x] processed-user-logins
    - [x] docker-compose.producer.yml
        - [x] Add service_healthy requirements
    - [x] docker-compose.consumer.yml
        - [x] Build and tag consumer image
        - [x] Add service_healthy requirements
- [x] Create consumer app
    - [x] Ingest consumed messages from the topic "user-login"
    - [x] Process the messages and output metrics/stats
    - [x] Send processed messages to the topic "processed-user-logins"
- [x] Create ingestor app
    - Python 3
    - [x] Set up kafka consumer member using confluent-kafka-python
    - [x] Consume messages from a topic
    - [x] Graceful teardown on error/exit
- [x] Create processor app
    - Python 3
    - [x] "Process" the messages
    - [x] Clean the data
    - [x] Compile statistics
    - [x] Report findings
    - [x] Make stat gathering async
    - [x] Allow for concurrent message processing
- [x] Create messenger app
    - Python 3
    - [x] Set up kafka producer member using confluent-kafka-python
    - [x] Ingest messages into a topic
    - [x] Graceful teardown on error/exit
- [x] Add automation for environment teardown
    - CLI Scripts with config files and enviornment variables
    - Bash for linux/mac
    - Powershell for windows
    - [x] Error handling
    - [x] Docker compose down script