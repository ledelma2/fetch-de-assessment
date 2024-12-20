# fetch-de-assessment
 Data Engineer Assessment Project for Fetch Rewards

# Steps to Run Pipeline
- Clone the repository to a local directory
- Verify Docker Desktop and Python3 have been installed with commands added to your system PATH
- Verify the docker engine is up, running, and accessible
- Open a terminal/command prompt/powershell window and navigate to the repository you cloned
- Run the `run_pipeline.py` python script to begin enviornment setup
- When finished running the pipeline press any key in the terminal/command prompt/powershell window and the enviornment will teardown

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
        - [ ] Verify cluster and container startup
        - [ ] Verify network startup
        - [ ] Create topics
            - [ ] user-login
            - [ ] \[tbd\]
    - [ ] Compose up docker-compose-producer-cluster.yml
        - [ ] Verify cluster and container startup
        - [ ] Check topic message receipt in kafka cluster
    - [ ] Compose up docker-compose-consumer-cluster.yml
        - [ ] Build and tag consumer image\(s\)
        - [ ] Verify cluster and container startup
        - [ ] Heartbeat/Initial Health Check
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
- [ ] Container Orchestration
    - [ ] Scaling
        - [ ] Dynamic Scaling
            - [ ] Kafka Cluster Containers
            - [ ] Consumer Cluster Containers
                - One cluster per consumer?
                - Have each consumer service get a cluster?
        - [ ] Manual Scaling
            - [ ] Producer Cluster
            - [ ] Kafka Topic Partitions
    - [ ] Balancing/Scheduling
        - [ ] Kafka Cluster Containers
        - [ ] Consumer Cluster Containers
    - Docker Swarm?