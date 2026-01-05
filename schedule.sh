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

# Add cron job to run run.sh every week
CRON_JOB="30 7 * * 6 cd $SCRIPT_DIR && ./run.sh"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "cd $SCRIPT_DIR && ./run.sh"; then
    existing_job=$(crontab -l 2>/dev/null | grep "cd $SCRIPT_DIR && ./run.sh")
    if [[ "$existing_job" == "$CRON_JOB" ]]; then
        echo "Cron job already registered with same schedule."
    else
        (crontab -l 2>/dev/null | grep -v "cd $SCRIPT_DIR && ./run.sh"; echo "$CRON_JOB") | crontab -
        echo "Cron job updated to new schedule."
    fi
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "New cron job registered to run every week."
fi

echo "Scheduling complete."
exit 0