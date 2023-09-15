#!/usr/bin/env bash

# Change to the parent directory
cd ..

# Check if act is installed
if ! [ -f ./bin/act ]; then
    echo "act not found, downloading and installing..."
    # Download and install act
    curl https://raw.githubusercontent.com/nektos/act/master/install.sh | bash
else
    echo "act is already installed"
fi

# Create .actrc file with default configuration
echo "-P ubuntu-latest=catthehacker/ubuntu:act-22.04" > .actrc

# Execute act
./bin/act 2>&1 | tee log.txt