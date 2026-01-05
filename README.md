# Projects Me Practice

A personal coding practice system that automatically sends weekly coding challenges via email. Built for self-hosted deployment (ideal for Raspberry Pi or similar always-on servers), this application manages a bank of 500+ coding projects and intelligently allocates new challenges to registered users on a weekly schedule.

## Features

- **Project Bank Management**: Store and manage 500+ coding projects sourced from AI-generated content
- **User Management**: Register users and track their progress through allocated projects
- **Smart Allocation**: Intelligent project assignment that avoids duplicate allocations and respects project groupings/steps
- **Automated Email Delivery**: Sends formatted HTML emails with project details and difficulty tags
- **Scheduled Execution**: Built-in cron scheduling for weekly problem delivery (runs every Saturday at 7:30 AM by default)
- **Flexible Configuration**: Environment-based configuration for email providers, sender details, and production modes
- **CSV-Based Database**: Simple, file-based persistence for portability and easy backups

## Project Structure

```
project-me-practice/
├── projectmepractice/           # Main package
│   ├── __init__.py              # Entry point exports and logic
│   ├── const.py                 # Database file constants
│   ├── users.py                 # User registration and management
│   ├── projects.py              # Project CRUD and selection logic
│   └── practice.py              # Project allocation logic
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── 500ProjectsList.csv          # Source project bank (500+ projects)
├── email-template.html          # HTML template for emails
├── install.sh                   # Setup and initialization script
├── run.sh                       # Execution wrapper with error handling
└── schedule.sh                  # Cron job registration utility
```

## Data Models

### Projects Database (`projects.db.csv`)
- **id**: Unique project identifier
- **title**: Project name
- **description**: Problem statement and requirements
- **domain**: Technology domain (Web, Mobile, Data Science, etc.)
- **duration**: Time to complete in weeks
- **has_parts**: Boolean indicating if project has multi-step groups
- **group_id**: ID for multi-part projects
- **group_part**: Step number within a group

### Users Database (`users.db.csv`)
- **id**: Unique user UUID
- **name**: User's display name
- **email**: Contact email for problem delivery
- **created_on**: ISO timestamp of registration

### Allocations Database (`allocations.db.csv`)
- **id**: Unique allocation UUID
- **project**: Allocated project ID
- **user**: Recipient user ID
- **date**: ISO timestamp of allocation

## Installation & Setup

### Prerequisites

- Python 3.7+
- Bash shell (Linux/macOS) or WSL (Windows)
- Email service credentials (MailerSend recommended)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd project-me-practice
   ```

2. **Run the installation script**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
   
   This script will:
   - Verify Python 3 is installed
   - Create a `.env` configuration file from `.env.template`
   - Set up a Python virtual environment in `.venv`
   - Create the virtual environment and install dependencies

3. **Configure environment variables**
   
   The installation script will prompt you for:
   - **PROD_MODE**: Set to `true` to enable email sending (default: `false`)
   - **MAILERSEND_API_KEY**: Your MailerSend API key (only needed if PROD_MODE=true)
   - **EMAIL_SENDER_NAME**: Name displayed in emails (default: "Project Bot")
   - **EMAIL_SENDER_EMAIL**: Sender email address (default: "no-reply@your-domain.com")

   Example `.env` file:
   ```
   PROD_MODE=true
   MAILERSEND_API_KEY=your-mailersend-api-key-here
   EMAIL_SENDER_NAME=Project Bot
   EMAIL_SENDER_EMAIL=no-reply@your-domain.com
   ```

### Running the Application

#### Single Execution (Debug Mode)
```bash
./run.sh
```
This will:
- Verify all dependencies are installed
- Execute `main.py`
- Log any errors to `fatal.log`
- Generate `debug-email.html` if PROD_MODE is disabled

#### Automated Weekly Delivery

1. **Register the default cron job** (Saturday 7:30 AM)
   ```bash
   chmod +x schedule.sh
   ./schedule.sh --register
   ```

2. **Use custom schedule** (if desired)
   ```bash
   ./schedule.sh --custom "0 9 * * 1"  # Every Monday at 9 AM
   ```

3. **View registered cron jobs**
   ```bash
   crontab -l
   ```

4. **Remove scheduling**
   ```bash
   ./schedule.sh --unregister
   ```

## Usage Examples

### Direct Python Usage

```python
from projectmepractice import (
    feed_all_projects,
    register_new_user,
    allocate_next_project_for_user,
    fetch_allocated_projects,
    fetch_registered_users
)

# Initialize project bank
feed_all_projects("500ProjectsList.csv")

# Register a new user
user = register_new_user("John Doe", "john@example.com")

# Allocate next unassigned project
project = allocate_next_project_for_user(user["id"])

# View user's allocated projects
allocated = fetch_allocated_projects(user_id=user["id"])

# List all registered users
all_users = fetch_registered_users()
```

### Managing Users

```python
from projectmepractice import modify_user_email, delete_user

# Update user email
modify_user_email(user_id="uuid-here", new_email="newemail@example.com")

# Delete a user
delete_user(user_id="uuid-here")
```

## Email Configuration

### Debug Mode (PROD_MODE=false)
- Emails are written to `debug-email.html` instead of being sent
- Useful for testing template rendering and content

### Production Mode (PROD_MODE=true)
- Emails are sent via MailerSend API
- Requires valid `MAILERSEND_API_KEY`
- Check `fatal.log` for delivery errors

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `python3 not found` | Install Python 3.7+ from python.org |
| `.env not found` | Run `install.sh` again to regenerate |
| `.venv not working` | Delete `.venv/` and run `install.sh` again |
| Missing dependencies | Run `source .venv/bin/activate && pip install -r requirements.txt` |
| Emails not sending | Verify `PROD_MODE=true` and valid `MAILERSEND_API_KEY` in `.env` |
| Cron job not running | Verify with `crontab -l` and check system logs |

## Dependencies

- **email_me_anything**: Email rendering and delivery service integration

See [requirements.txt](requirements.txt) for complete dependency list.

## Project Bank

The primary project source is [500ProjectsList.csv](500ProjectsList.csv), containing 500+ coding challenges across multiple domains and difficulty levels, sourced from AI-generated content.

## Notes

- Projects are AI-generated and may vary in quality and originality
- This is a personal project built for continuous learning and practice
- No solutions are included; challenges are designed for self-study
- Suitable for self-hosted deployment on always-on systems like Raspberry Pi
- Check logs (`fatal.log`) for debugging issues

## Future Improvements

- Enhance project selection logic to consider project groups and steps more intelligently
- Add user dashboard for progress tracking
- Implement difficulty level selection
- Add support for alternative email providers
- Create web-based UI for user management

## Contributing

Found issues or have suggestions? Please report them via the Issues section.
