#!/bin/bash

# Function to display help
show_help() {
    cat << EOF
Usage: schedule.sh [OPTIONS]

Options:
    --register              Register the cron job (default)
    --unregister            Remove the cron job
    --custom <expr>         Set custom cron expression
                           Format: "minute hour day month weekday"
    --help                  Show this help message

Examples:
    schedule.sh --register
    schedule.sh --custom "0 0 * * *"
    schedule.sh --unregister
EOF
}

# Function to validate cron expression
validate_cron_expr() {
    local expr="$1"
    local fields=(${expr})
    
    if [[ ${#fields[@]} -ne 5 ]]; then
        return 1
    fi
    
    return 0
}

# Check if required files exist
files=(".env" ".venv" "main.py" "run.sh")
missing=()

for file in "${files[@]}"; do
    if [[ ! -e "$file" ]]; then
        missing+=("$file")
    fi
done

if [[ ${#missing[@]} -gt 0 ]]; then
    echo "Error: Missing files: ${missing[*]}, have you run the install script?"
    exit 1
fi

# Parse arguments
action="register"
cron_expr="0 7 * * 6"  # Default: weekly

while [[ $# -gt 0 ]]; do
    case "$1" in
        --register)   action="register"; shift ;;
        --unregister) action="unregister"; shift ;;
        --custom)     
            if validate_cron_expr "$2"; then
                cron_expr="$2"
                shift 2
            else
                echo "Error: Invalid cron expression format. Expected: 'minute hour day month weekday'"
                exit 1
            fi
            ;;
        --help)       show_help; exit 0 ;;
        *)            echo "Unknown option: $1"; show_help; exit 1 ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_JOB="$cron_expr cd $SCRIPT_DIR && ./run.sh"

if [[ "$action" == "unregister" ]]; then
    if crontab -l 2>/dev/null | grep -q "cd $SCRIPT_DIR && ./run.sh"; then
        (crontab -l 2>/dev/null | grep -v "cd $SCRIPT_DIR && ./run.sh") | crontab -
        echo "Cron job removed."
    else
        echo "No cron job found to remove."
    fi
else
    if crontab -l 2>/dev/null | grep -q "cd $SCRIPT_DIR && ./run.sh"; then
        (crontab -l 2>/dev/null | grep -v "cd $SCRIPT_DIR && ./run.sh"; echo "$CRON_JOB") | crontab -
        echo "Cron job updated."
    else
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        echo "New cron job registered."
    fi
fi

exit 0