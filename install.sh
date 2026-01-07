#!/usr/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed" >&2
    exit 1
fi

# Verify or create .env
if [[ ! -f .env ]]; then
    if [[ ! -f .env.template ]]; then
        echo "Error: .env.template not found" >&2
        exit 1
    fi

    cp .env.template .env

    echo "Created .env from template. Please fill in the required values:"
    
    read -p "Enable production mode (true/false) [default: false]: " PROD_MODE
    PROD_MODE=${PROD_MODE:-false}
    sed -i "s|PROD_MODE=.*|PROD_MODE=$PROD_MODE|" .env

    if [[ "$PROD_MODE" == "true" ]]; then
        read -p "Enter MailerSend API key: " MAILERSEND_KEY
        sed -i "s|MAILERSEND_API_KEY=.*|MAILERSEND_API_KEY=$MAILERSEND_KEY|" .env
    else
        sed -i "s|MAILERSEND_API_KEY=.*|MAILERSEND_API_KEY=your-mailersend-api-key-here|" .env
    fi

    read -p "Enter email sender name [default: Project Bot]: " EMAIL_SENDER_NAME
    EMAIL_SENDER_NAME=${EMAIL_SENDER_NAME:-Project Bot}
    sed -i "s|EMAIL_SENDER_NAME=.*|EMAIL_SENDER_NAME=$EMAIL_SENDER_NAME|" .env

    read -p "Enter email sender address [default: no-reply@your-domain.com]: " EMAIL_SENDER_ADDRESS
    EMAIL_SENDER_ADDRESS=${EMAIL_SENDER_ADDRESS:-no-reply@your-domain.com}
    sed -i "s|EMAIL_SENDER_ADDRESS=.*|EMAIL_SENDER_ADDRESS=$EMAIL_SENDER_ADDRESS|" .env

    echo ".env configuration complete"
fi

# Create virtual environment if it doesn't exist
if [[ ! -d .venv ]]; then
    python3 -m venv .venv
    if [[ $? -ne 0 ]]; then
        echo "Error: Failed to create virtual environment" >&2
        exit 1
    fi
fi

# Activate virtual environment and install dependencies
source .venv/bin/activate
pip install -r requirements.txt
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to install required packages" >&2
    exit 1
else
    echo "Required packages installed successfully"
fi

# Initialize database if script exists and DATABASE_URL is configured
if [[ -f init_db.py ]] && grep -q "DATABASE_URL=" .env; then
    python init_db.py
    if [[ $? -ne 0 ]]; then
        echo "Error: Database initialization failed" >&2
        exit 1
    else
        echo "Database initialized successfully"
    fi
fi

deactivate
echo "Installation complete. You can now run the application using ./run.sh"

exit 0