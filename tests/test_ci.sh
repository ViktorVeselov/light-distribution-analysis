#!/usr/bin/env bash

# Search for the target directory upwards
search_for_directory() {
    local target_dir="$1"
    local max_attempts="$2"
    local current_dir="$PWD"
    local attempts=0

    while [[ $attempts -lt $max_attempts ]]; do
        if [[ -d "$current_dir/$target_dir" ]]; then
            echo "Found $target_dir at $current_dir"
            cd "$current_dir/$target_dir"
            return 0
        fi

        # Move up one directory
        current_dir=$(dirname "$current_dir")
        ((attempts++))
    done

    echo "$target_dir not found after $max_attempts attempts."
    return 1
}

# Search for the directory and change to it if found
search_for_directory "light-distribution-analysis" 10

# Check if act is installed
if ! [ -f ./bin/act ]; then
    echo "act not found, downloading and installing..."
    # Download and install act
    curl https://raw.githubusercontent.com/nektos/act/master/install.sh | bash
else
    echo "act is already installed"
fi

# Create .actrc file with default configuration
echo "-P ubuntu-latest=nektos/act-environments-ubuntu:18.04" > .actrc

# Execute act
./bin/act 2>&1 | tee log.txt
