#!/usr/bin/bash

print_help() {
    cat <<'HELP'
Project Me Practice - Installer

Usage:
  ./setup.sh [command] [options]

Commands:
  update [--force|-f] [--dry-run] [--branch <name>]  Update repo and re-run setup
  uninstall                                          Remove .venv, .env and optionally db.sqlite3
  (no args)                                          Run setup (default)

Options:
  --help, -h                                         Show this help and exit

HELP
}

# If no args provided, print a short header and continue
if [[ $# -eq 0 ]]; then
    echo "Project Me Practice setup — run './setup.sh --help' for usage details"
else
    if [[ "$1" == "--help" || "$1" == "-h" ]]; then
        print_help
        exit 0
    fi
fi

# Update option: pulls latest changes and re-runs setup
if [[ "$1" == "update" || "$1" == "--update" ]]; then
    shift

    # Parse options: --force/-f, --dry-run, --branch <name>
    FORCE=no
    DRY_RUN=no
    BRANCH=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --force|-f)
                FORCE=yes
                shift
                ;;
            --dry-run)
                DRY_RUN=yes
                shift
                ;;
            --branch|-b)
                if [[ -n "$2" ]]; then
                    BRANCH="$2"
                    shift 2
                else
                    echo "Error: --branch requires a branch name" >&2
                    exit 1
                fi
                ;;
            --branch=*)
                BRANCH="${1#*=}"
                shift
                ;;
            --help|-h)
                echo "Usage: $0 update [--force] [--dry-run] [--branch <name>]"
                exit 0
                ;;
            *)
                echo "Unknown option: $1" >&2
                exit 1
                ;;
        esac
    done

    echo "Updating repository from git..."

    if ! command -v git &> /dev/null; then
        echo "Error: git is not installed" >&2
        exit 1
    fi

    # Dry-run: show commands and exit
    if [[ "$DRY_RUN" == "yes" ]]; then
        echo "[DRY RUN] git status --porcelain"
        git status --porcelain
        echo "[DRY RUN] git fetch ${BRANCH:+origin $BRANCH}"
        if [[ -n "$BRANCH" ]]; then
            git fetch origin "$BRANCH"
            echo "[DRY RUN] git log --oneline HEAD..origin/$BRANCH"
            git log --oneline HEAD..origin/"$BRANCH" || true
        else
            git fetch --all
            echo "[DRY RUN] git log --oneline HEAD..origin/HEAD"
            git log --oneline HEAD..origin/HEAD || true
        fi
        echo "[DRY RUN] No changes applied."
        exit 0
    fi

    # Warn if there are local changes (skip if --force)
    if [[ "$FORCE" != "yes" ]]; then
        if ! git diff --quiet || ! git diff --cached --quiet; then
            echo "Warning: you have local changes that may conflict with the update."
            read -p "Continue with git pull and potentially overwrite local changes? (yes/no): " CONFIRM_UPDATE
            if [[ "$CONFIRM_UPDATE" != "yes" ]]; then
                echo "Update aborted."
                exit 0
            fi
        fi
    else
        echo "--force set: skipping local changes check"
    fi

    if [[ -n "$BRANCH" ]]; then
        git pull --ff-only origin "$BRANCH"
    else
        git pull --ff-only
    fi
    if [[ $? -ne 0 ]]; then
        echo "Error: git pull failed" >&2
        exit 1
    fi

    echo "Repository updated. Re-running setup..."
    # Re-run this script without arguments to perform a fresh install
    exec "$0"
fi

# Uninstall option: clears virtualenv, .env and optionally database
if [[ "$1" == "uninstall" || "$1" == "--uninstall" ]]; then
    echo "WARNING: This will remove the virtual environment (.venv), the .env file, and may remove the database file (db.sqlite3)."
    read -p "Are you sure you want to proceed? (yes/no): " CONFIRM
    if [[ "$CONFIRM" != "yes" ]]; then
        echo "Uninstallation aborted."
        exit 0
    fi

    # Remove virtual environment
    if [[ -d .venv ]]; then
        rm -rf .venv
        if [[ $? -eq 0 ]]; then
            echo "Removed .venv"
        else
            echo "Warning: Failed to remove .venv" >&2
        fi
    else
        echo ".venv not found, skipping."
    fi

    # Remove .env
    if [[ -f .env ]]; then
        rm -f .env
        if [[ $? -eq 0 ]]; then
            echo "Removed .env"
        else
            echo "Warning: Failed to remove .env" >&2
        fi
    else
        echo ".env not found, skipping."
    fi

    # Optionally remove database file
    if [[ -f db.sqlite3 ]]; then
        read -p "Remove database file 'db.sqlite3' as well? (yes/no) [default: yes]: " REMOVE_DB
        REMOVE_DB=${REMOVE_DB:-yes}
        if [[ "$REMOVE_DB" == "yes" ]]; then
            rm -f db.sqlite3
            if [[ $? -eq 0 ]]; then
                echo "Removed db.sqlite3"
            else
                echo "Warning: Failed to remove db.sqlite3" >&2
            fi
        else
            echo "Kept db.sqlite3"
        fi
    fi

    echo "Uninstallation complete."
    exit 0
fi

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

    read -p "Enter email sender name [default: Project Bot]: " EMAIL_SENDER_NAME
    EMAIL_SENDER_NAME=${EMAIL_SENDER_NAME:-Project Bot}
    sed -i "s|EMAIL_SENDER_NAME=.*|EMAIL_SENDER_NAME=$EMAIL_SENDER_NAME|" .env

    read -p "Enter email sender address: " EMAIL_SENDER_ADDRESS
    sed -i "s|EMAIL_SENDER_ADDRESS=.*|EMAIL_SENDER_ADDRESS=$EMAIL_SENDER_ADDRESS|" .env

    if [[ "$PROD_MODE" == "true" ]]; then
        read -p "Choose mailer client - 'smtp' or 'mailersend' [default: mailersend]: " MAILER_CLIENT
        MAILER_CLIENT=${MAILER_CLIENT:-mailersend}
        sed -i "s|MAILER_CLIENT=.*|MAILER_CLIENT=\"$MAILER_CLIENT\"|" .env

        if [[ "$MAILER_CLIENT" == "smtp" ]]; then
            read -p "Enter SMTP_HOST: " SMTP_HOST
            sed -i "s|SMTP_HOST = .*|SMTP_HOST = \"$SMTP_HOST\"|" .env
            
            read -p "Enter SMTP_PORT: " SMTP_PORT
            sed -i "s|SMTP_PORT = .*|SMTP_PORT = $SMTP_PORT|" .env
            
            read -p "Enter SMTP_USER: " SMTP_USER
            sed -i "s|SMTP_USER = .*|SMTP_USER = \"$SMTP_USER\"|" .env
            
            read -p "Enter SMTP_PASS: " SMTP_PASS
            sed -i "s|SMTP_PASS = .*|SMTP_PASS = \"$SMTP_PASS\"|" .env
        else
            read -p "Enter MailerSend API key: " MAILERSEND_API_KEY
            sed -i "s|MAILERSEND_API_KEY=.*|MAILERSEND_API_KEY=\"$MAILERSEND_API_KEY\"|" .env
        fi
    else
        sed -i "s|MAILER_CLIENT=.*|MAILER_CLIENT=\"mailersend\"|" .env
        read -p "Enter MailerSend API key: " MAILERSEND_API_KEY
        sed -i "s|MAILERSEND_API_KEY=.*|MAILERSEND_API_KEY=\"$MAILERSEND_API_KEY\"|" .env
    fi

    read -p "Enable AI features (true/false) [default: false]: " AI_FEATURES_ENABLED
    AI_FEATURES_ENABLED=${AI_FEATURES_ENABLED:-false}
    sed -i "s|AI_FEATURES_ENABLED=.*|AI_FEATURES_ENABLED=\"$AI_FEATURES_ENABLED\"|" .env

    if [[ "$AI_FEATURES_ENABLED" == "true" ]]; then
        read -p "Enter OpenAI API key: " OPENAI_API_KEY
        sed -i "s|OPENAI_API_KEY=.*|OPENAI_API_KEY=\"$OPENAI_API_KEY\"|" .env
    fi

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
if [[ -f init_db.py ]] && grep -q "DATABASE_URL" .env; then
    python init_db.py
    if [[ $? -ne 0 ]]; then
        echo "Error: Database initialization failed" >&2
        exit 1
    else
        echo "Database initialized successfully"
    fi
else
    echo "Database initialization skipped (init_db.py not found or DATABASE_URL not set)"
fi

deactivate
echo "Installation complete. You can now run the application using ./run.sh"

exit 0