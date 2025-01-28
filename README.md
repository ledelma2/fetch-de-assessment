# fetch-de-assessment
Data Engineer Assessment Project for Fetch Rewards

# Design Overview
The main drivers behind my design decisions were scalability and speed. Ideally, in a production enviornment, every major piece of the `consumer.py` class would be containerized and free to scale independantly. However, for the purposes of this assessment, I decided to make the classes a little more tightly coupled to simplify I/O and control flow.

## Enviornment Setup and Teardown
Enviornment setup and teardown is fairly straightforward. The main technology behind both is Docker, specifically the `docker compose` command. These compose commands are executed through shell scripts, either powershell or bash depending on the user's OS, which are in turn called by a singular "entry" python script.

The initial driving force of setup and teardown starts with a single python script at the top level of the repository. This single point of entry determines the user's operating system and calls the appropriate shell script to begin actual execution. A fair amount of thought was put into this specific design decision, as there was a strong argument to ditch the shell scripts and leverage python directly. I, however, felt it was more appropriate to execute cli commands through native OS scripting as it presented the oppurtunity for a more robust solution. Why overcomplicate control flow when there's a nice, simple solution already available? In addition, I also felt that the shell script method could better assist with deployment at scale, as one could hypothetically ditch the "entry" python script entirely in place of the appropriate shell scripts for the specific OS's of the VM's being used.

Beyond the scripts, the enviornment setup and teardown solution also significantly utilizes configuration of `compose.yml` files. For starters, I was able to break apart the original compose file provided into multiple, service level files and reference them all in a single location. Needless to say, this not only decoupled most of the configuration logic, it also allowed for better scaling in the event that more powerful orchestration tools are implemented later on. Next, I decided to implement specific configurations to reference a local `dockerfile` and build the `consumer.py` image on-the-fly to further simplify setup. This small, yet powerful, change allows users to quickly modify and test the consumer source code without having to build and reference the image manually, it's all automated by docker. Lastly, I added some quality of life configurations such as health checks, startup dependency ordering, and configurable enviornment variables to further improve the solution's fault tolerance and scalability according to the user's needs.

## The Consumer
Following setup of the enviornment the main loop of control is found in the `consumer.py` script. This script serves as a sort of data control plane for the pipeline. It is coded up entirely in python, specifically python 3, due to the language's simplicity, readability, and the ability for it to integrate with kafka through the `confluent_kafka` library. The consumer first starts by setting up some logging and a signal handler, for graceful shutdown when the user directs it to, in addition to initializing the `ingestor.py`, `processor.py`, and `messenger.py` property classes. Following this setup the consumer directs the ingestor to poll for messages, which then sends any found messages to the processor for cleaning and metric compilation. After recieving the proccessed messages the consumer finally gives the data to the messenger for writing to a destination kafka topic. The consumer will loop through these commands until the user sends an interrupt signal (ctrl+c). Once the signal is recieved the main program loop ends, the processor reports the metrics it compiled during the run of the pipeline, and memory is freed up.

### The Ingestor
For the same reasons explained in the consumer section, the `ingestor.py` class is also written in python. This class's function is to ingest messages into the system after being consumed from a kafka topic. The ingestor is fairly straightforward with its functionality. When initialized a logger context is set and a `Consumer` property is created from the library `confluent_kafka`. The consumer is then subscribed to a specified topic and upon call of the `consume_messages` function, messages will be consumed. This consumption can be done in batches, if a higher throughput is desired, and with a user defined wait time, to prevent throttling on the kafka cluster or network. When messages have been consumed, the ingestor examines each for errors as a precaution against ingesting bad data. If all goes well, and there are no critical errors, the ingestor will then return a list of unerrored messages it has consumed. Upon teardown the ingestor will close the consumer's connection to the kafka cluster.

### The Processor

### The Messenger

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