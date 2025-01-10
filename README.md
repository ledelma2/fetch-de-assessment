# fetch-de-assessment
 Data Engineer Assessment Project for Fetch Rewards

# Steps to Run Pipeline
- Clone the repository to a local directory
- Verify Docker Desktop and Python3 have been installed with commands added to your system PATH
- Verify the docker engine is up, running, and accessible
- Open a terminal, command prompt, or powershell window and navigate to the cloned repository
- Run the `run_pipeline.py` python script to begin enviornment setup
    - For Windows the command is `python run_pipeline.py`
    - For Mac/Linux the command is `python3 run_pipeline.py`

## TODO
- [x] Create single point of entry script
    - Python3
    - [x] Runs the setup for Windows
    - [x] Runs the setup for other OS's
- [ ] Add automation for enviornment setup
    - CLI Scripts with config files and enviornment variables
    - Bash for linux/mac
    - Powershell for windows
    - [ ] Compose up docker-compose-kafka-cluster.yml
        - [ ] Parse through running containers to verify cluster and container startup
        - [x] Verify network startup
        - [ ] Create topics
            - [ ] user-login
            - [ ] \[tbd\]
    - [ ] Compose up docker-compose-producer-cluster.yml
        - [ ] Verify cluster and container startup
        - [ ] Check topic message receipt in kafka cluster
    - [ ] Compose up docker-compose-consumer-cluster.yml
        - [ ] Build and tag consumer image\(s\)
        - [ ] Verify cluster and container startup
            - [ ] Ingestor
            - [ ] Processor
            - [ ] Messenger
- [ ] Create ingestor app
    - Python 3 or Java
    - [ ] Ingest the messages from the producer topic "user-login"
    - [ ] Send the messages to the processor app
- [ ] Create processor app
    - Python 3 or Java
    - [ ] "Process" the messages
    - [ ] Send the data to the messenger app
    - Send metrics to dashboards?
    - Clean the data?
- [ ] Create messenger app
    - Python 3 or Java
    - [ ] Send the messages to the sink topic "\[tbd\]"
- [ ] Add automation for environment teardown
    - CLI Scripts with config files and enviornment variables
    - Bash for linux/mac
    - Powershell for windows
    - [ ] Error handling
    - [ ] Compose down docker-compose-kafka-cluster.yml
        - [ ] Verify cluster and container shutdown
    - [ ] Compose down docker-compose-producer-cluster.yml
        - [ ] Verify cluster and container shutdown
    - [ ] Compose down docker-compose-consumer-cluster.yml
        - [ ] Verify cluster and container shutdown