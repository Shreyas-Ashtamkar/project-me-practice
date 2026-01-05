#!/usr/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed" >&2
    exit 1
fi

# Verify .env and .venv exist
if [[ ! -f .env ]] || [[ ! -d .venv ]]; then
    echo "Error: BAD CONFIG or NOT INSTALLED. Please run install.sh first" >&2
    exit 1
fi

# Verify Python in venv is working
if ! .venv/bin/python3 -c "import sys" &> /dev/null; then
    echo "Error: Python in .venv is not working. Please run install.sh first" >&2
    exit 1
fi

# Verify required packages are installed
if ! .venv/bin/python3 -m pip show email_me_anything &> /dev/null; then
    echo "Error: Required packages not installed. Please run install.sh first" >&2
    exit 1
fi

# Check if the main script exists
if [[ ! -f main.py ]]; then
    echo "Error: main.py not found, this installation is broken, please fetch from the official repository" >&2
    exit 1
fi

# Execute the main script and log errors
.venv/bin/python3 main.py 2> fatal.log

# Delete fatal.log if it's empty
[[ ! -s fatal.log ]] && rm fatal.log

exit 0
