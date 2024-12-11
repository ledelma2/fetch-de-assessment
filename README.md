# fetch-de-assessment
 Data Engineer Assessment Project for Fetch Rewards
## TODO
- Add automation for enviornment setup
    - CLI Scripts with config files
    - Compose docker-compose.yml
    - Maybe create network if it doesn't exist?
    - Start zookeeper
    - Start kafka and broker(s)
    - Verify installations
    - Create topics
        - user-login
        - \[tbd\]
    - Begin message generator app
    - Scaler?
    - Balancer?
    - Scheduler?
- Create ingestor app
    - Python 3
    - Should ingest the messages from the producer topic "user-login"
    - Send the messages to the processor app
- Create processor app
    - Python 3
    - Should "process" the messages
        - Send metrics to dashboards?
        - Clean the data?
    - Send the data to the messenger app
- Create messenger app
    - Python 3
    - Should send the messages to the sink topic "\[tbd\]"
