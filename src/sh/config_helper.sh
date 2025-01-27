# Define function for reading values from json configf files
read_json_value() {
    local file_path="$1"
    local key="$2"

    # Check if jq cli tool is installed
    if ! validate_json "$file_path"; then
        echo "Error running config-helper.sh: Unable to validate json config..."
        return 1
    fi

    local value=$(jq -r --arg key "$key" '.[$key]' "$file_path")
    if [[ $? -ne 0 ]]; then
        echo "Error running config-helper.sh: Failed to parse json config..."
        return 1
    fi

    if [[ "$value" == "null" ]]; then
        echo "Error running config-helper.sh: Key $key not found in json config..."
        return 1
    else
        echo "$value"
        return 0
    fi
}

# Define function for validating file
validate_json() {
    local file_path="$1"
    
    # Check if jq cli tool is installed
    if ! command -v jq &> /dev/null; then
        echo "Error running config-helper.sh: jq not installed..."
        return 2
    fi

    # Check for file existence
    if [[ ! -f "$file_path" ]]; then
        echo "Error running config-helper.sh: '$file_path' does not exist..."
        return 1
    fi

    # Validate json contents
    if jq empty "$file_path" &> /dev/null; then
        return 0
    else
        echo "File '$file_path' is not a valid json config..."
        return 1
    fi
}