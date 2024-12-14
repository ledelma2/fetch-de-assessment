# fetch-de-assessment
 Data Engineer Assessment Project for Fetch Rewards

# Steps to Run Pipeline
- Clone the repository to a local directory
- Verify Docker and Python3 have been installed with commands added to your system PATH
- Verify the docker engine is up, running, and accessible
- Open a terminal/command prompt/powershell window and navigate to the repository you cloned
- Run the `run_pipeline.py` python script to begin enviornment setup
- When finished running the pipeline press any key in the terminal/command prompt/powershell window and the enviornment will teardown

## TODO
- [x] Create single point of entry script
    - Python3
    - [x] Runs the pipeline for Windows
    - [x] Runs the pipeline for other OS's
- [ ] Add automation for enviornment setup
    - CLI Scripts with config files
    - Bash for linux/mac
    - Powershell for windows
    - [x] Compose up docker-compose.yml
    - [ ] Create network if it doesn't exist
    - [ ] Start zookeeper
    - [ ] Start kafka and broker(s)
    - [ ] Verify installations
    - [ ] Create topics
        - [ ] user-login
        - [ ] \[tbd\]
    - [ ] Begin message generator app
    - Scaler?
    - Balancer?
    - Scheduler?
- [ ] Create ingestor app
    - Python 3
    - [ ] Ingest the messages from the producer topic "user-login"
    - [ ] Send the messages to the processor app
- [ ] Create processor app
    - Python 3
    - [ ] "Process" the messages
        - Send metrics to dashboards?
        - Clean the data?
    - [ ] Send the data to the messenger app
- [ ] Create messenger app
    - Python 3
    - [ ] Send the messages to the sink topic "\[tbd\]"
- [ ] Add automation for environment teardown
    - CLI Scripts with config files
    - Bash for linux/mac
    - Powershell for windows
    - [ ] Error handling
    - [ ] Delete containers
    - [ ] Compose down docker-compose.yml
