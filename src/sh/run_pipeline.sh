# Exit Code
exit_code=1

# Define a function to handle a stop signal
handle_stop_signal() {
    exit_code=0
    echo "Stop signal recieved. Gracefully shutting down..."
    exit $exit_code
}

# Define a function to handle error signal
handle_error() {
    exit_code=$?
    echo "Unexpected error during pipeline sh script run..."
    exit $exit_code
}

# Define a function to handle exit signal
handle_exit() {
    # Run docker compose down script
    bash ./docker_compose_down.sh
    cd ../..
    exit $exit_code
}

# Register the handle_stop_signal function for the stop signals
trap handle_stop_signal SIGINT SIGTERM

# Register the handle_error function for error signals
trap handle_error ERR

# Register the handle_exit function for exit signals
trap handle_exit EXIT

# Set location to sh script directory
cd src/sh
# Run docker compose up script
bash ./docker_compose_up.sh
# Determine operating system and use appropriate terminal for consumer data logging
os=$(uname)
working_dir=$(pwd)
if [[ "$os" == "Linux" ]]; then
    # Launch gnome-terminal for linux users
    gnome-terminal -- bash -c "docker compose logs -f my-python-consumer; exec bash"
elif [[ "$os" == "Darwin" ]]; then
    # Launch termional through osascript for mac users
    osascript -e "tell application \"Terminal\" to do script \"cd $working_dir; docker compose logs -f my-python-consumer; exec bash\""
else
    # Unsupported os for this script
    exit 1
fi

echo "Pipeline successfully started, waiting for user stop signal..."
while true; do
    # Sleep until sigint or sigterm comes in from user
    sleep 1
done