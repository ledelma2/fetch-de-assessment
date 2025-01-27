#!/bin/bash
source config_helper.sh

compose_file_path="../../compose.yml"
config_file_path="../config/config.json"
env_file_path="../config/.env"
timeout_key="ComposeUpTimeout"
timeout=$(read_json_value "$config_file_path" "$timeout_key")

if [[ $? -eq 0 ]]; then
    echo "Running docker compose up with custom timeout $timeout"
    docker compose -f $compose_file_path --env-file $env_file_path up -d -t $timeout
else
    echo "Running docker compose up with default timeout..."
    docker compose -f $compose_file_path --env-file $env_file_path up -d
fi