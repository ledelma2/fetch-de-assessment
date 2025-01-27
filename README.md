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