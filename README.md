# fetch-de-assessment
Data Engineer Assessment Project for Fetch Rewards

# Design Overview
The main drivers behind my design decisions were scalability and speed. Ideally, in a production enviornment, every major piece of the `consumer.py` class would be containerized and free to scale independantly. However, for the purposes of this assessment, I decided to make the classes a little more tightly coupled to simplify I/O and control flow.

## Enviornment Setup and Teardown
Enviornment setup and teardown is fairly straightforward. The main technology behind both is Docker, specifically the `docker compose` command. These compose commands are executed through shell scripts, either powershell or bash depending on the user's OS, which are in turn called by a singular "entry" python script.

The initial driving force of setup and teardown starts with a single python script at the top level of the repository. This single point of entry determines the user's operating system and calls the appropriate shell script to begin actual execution. A fair amount of thought was put into this specific design decision, as there was a strong argument to ditch the shell scripts and leverage python directly. I, however, felt it was more appropriate to execute cli commands through native OS scripting as it presented the oppurtunity for a more robust solution. Why overcomplicate control flow when there's a nice, simple solution already available? In addition, I also felt that the shell script method could better assist with deployment at scale, as one could hypothetically ditch the "entry" python script entirely in place of the appropriate shell scripts for the specific OS's of the VM's being used.

Beyond the scripts, the enviornment setup and teardown solution also significantly utilizes configuration of `compose.yml` files. For starters, I was able to break apart the original compose file provided into multiple, service level files and reference them all in a single location. Needless to say, this not only decoupled most of the configuration logic, it also allowed for better scaling in the event that more powerful orchestration tools are implemented later on. Next, I decided to implement specific configurations to reference a local `dockerfile` and build the `consumer.py` image on-the-fly to further simplify setup. This small, yet powerful, change allows users to quickly modify and test the consumer source code without having to build and reference the image manually, it's all automated by docker. Lastly, I added some quality of life configurations such as health checks, startup dependency ordering, and configurable enviornment variables to further improve the solution's fault tolerance and scalability according to the user's needs.

## The Consumer
Following setup of the enviornment the main loop of control is found in the `consumer.py` script. This script serves as a sort of data control plane for the pipeline. This portion of the pipeline is coded up entirely in python, specifically python 3, due to the language's simplicity, readability, and ease of kafka integration through the `confluent_kafka` library. The consumer first starts by setting up some logging and a signal handler, for graceful shutdown when the user directs it to, in addition to initializing the `ingestor.py`, `processor.py`, and `messenger.py` property classes. Following this setup the consumer directs the ingestor to poll for messages, which then sends any found messages to the processor for cleaning and metric compilation. After recieving the proccessed messages the consumer finally gives the data to the messenger for writing to a destination kafka topic. The consumer will loop through these commands until the user sends an interrupt signal (ctrl+c). Once the signal is recieved the main program loop ends, the processor reports the metrics it compiled during the run of the pipeline, and memory is freed up.

### The Ingestor
This class's function is to ingest messages into the system after being consumed from a kafka topic. The ingestor is fairly straightforward with its functionality. When initialized a logger context is set and a `Consumer` property is created from the library `confluent_kafka`. The consumer is then subscribed to a specified topic and upon call of the `consume_messages` function, messages will be consumed. This consumption can be done in batches, if a higher throughput is desired, and with a user defined wait time, to prevent throttling on the kafka cluster or network. When messages have been consumed, the ingestor examines each for errors as a precaution against ingesting bad data. If all goes well, and there are no critical errors, the ingestor will then return a list of unerrored messages it has consumed - keep in mind this list can be empty. Upon teardown the ingestor will close the consumer's connection to the kafka cluster.

### The Processor
Following message ingestion the `processor.py` class takes over and begins work on processing messages. On initialization of the class a new logger context is set, after which several internal data managers, and their corresponding asynchronous locks, are created to handle async metric compilation. When the function `process_messages_async` is called, the processor begins to process each message in the message list passed in. In order to speed up the processing, the class leverages python's `concurrent.futures` library to allow for concurrent message processing. The `ProcessPoolExecutor` class is used for this multiprocessing, as oppossed to the `ThreadPoolExecutor`, due to the function `process_message` not requiring any shared state which allows for true concurrency and better performance. Bear in mind, if the user chooses _not_ to batch messages, this multiprocessing functionality loses all value. Message processing consists of converting each message into a dictionary and cleaning any improperly formatted pieces of the message. After the list of processed messages is completed the class then leverages python's `asyncio` library to create a list of tasks for each processed message to asynchronously compile metrics. Each task calls the function `compile_statistics_async`. This function asynchronously waits for locks to each data manager resource. Upon acquiring a lock, the appropriate data manager executes its exposed metric compilation function. The decision to leverage async behavior over multiprocessing for this step came down to each task needing to access the shared internal managers, and therefore a shared state. Ideally, these internal managers would be replaced with an external metric collection service, such as new relic or splunk, which would alleviate the shared state and further improve performance. After gathering the results of all metric compilation tasks, the processor then returns the list of processed messages. Upon termination of the pipeline `report_findings` is called and some insights are then calculated and reported through the logger.

### The Messenger
Lastly, after the messages have been ingested and processed, the `messenger.py` class executes. On initialization, this class sets a new logger context and a `Producer` property is created from the library `confluent_kafka`. The producer then calls its `flush` function to serve the designated callback for previous messages, just in case any failed to be delievered during a past run. When `produce_messages` is called the messenger will poll for any callbacks, waiting for the user defined `wait_time` if a callback is not triggered. The messenger then utilizes its producer member's `produce` function to actually produce a message to the outgoing kafka topic, looping through this functionality until all messages in the input list have been produced to the topic. After exiting the loop `flush` is called again to serve any callbacks that may be waiting. The `callback` function is very straightforward, as the messenger just checks to see if the produced message had any errors. Ideally some retry logic would be implemented to this callback for errored messages, as transient errors may occur, but for the purposes of the assessment just logging the error seemed to suffice. On shutdown of the pipeline all messages in the producer message queue are purged and the callbacks are serviced.

---

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
- With administrator priveleges open a terminal, if running on mac/linux, or powershell, if running on windows, and navigate to the cloned repository
- Run the `run_pipeline.py` python script to begin enviornment setup
    - For Windows the command is `python run_pipeline.py`
    - For Mac/Linux the command is `python3 run_pipeline.py`
- The window will display some diagnostic information for building the consumer image and setting up the pipeline's dependencies in docker
- When the pipeline is all setup a new terminal/powershell window will launch displaying logs from the consumer
    - Do not close the first terminal/powershell window as this will be used for pipeline control later
- In the new terminal/powershell window, verify that messages are being consumed, processed, and produced
- When you are satisfied with the pipeline execution, navigate back to the original terminal/powershell
    - Do not close the consumer window as diagnostic data will be displayed here after everything shuts down
- Send an interupt signal (ctrl+c) to end execution of the pipeline
- More diagnostic information will be produced to the original window while usage stats should appear on the second