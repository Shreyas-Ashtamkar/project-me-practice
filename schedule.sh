#!/bin/bash

# Check if required files exist
files=(".env" ".venv" "main.py" "run.sh")
missing=()

for file in "${files[@]}"; do
    if [[ ! -e "$file" ]]; then
        missing+=("$file")
    fi
done

if [[ ${#missing[@]} -gt 0 ]]; then
    echo "Error: Missing files: ${missing[*]}"
    exit 1
fi

echo "All required files exist, starting scheduling..."

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Add cron job to run run.sh every 10 minutes
CRON_JOB="*/10 * * * * cd $SCRIPT_DIR && ./run.sh"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "cd $SCRIPT_DIR && ./run.sh"; then
    echo "Cron job already registered."
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "New cron job registered to run every 10 minutes."
fi

echo "Scheduling complete."
exit 0