# Projects Me Practice

A self-hosted system that sends weekly coding challenges via email. It maintains a project bank, allocates new projects per user without repeats, and sends HTML emails. Works great on always-on devices (e.g., Raspberry Pi) and standard Linux/macOS machines. Windows users can run via WSL or use Python directly.

## Features

- **Project Bank**: Import from CSV; supports grouped, multi-step projects.
- **User Management**: Register users, track current project and week number.
- **Smart Allocation**: Avoids duplicates; continues next step in a group.
- **Automated Emails**: Uses `email_me_anything` with MailerSend or SMTP.
- **Scheduling**: Cron-friendly wrapper with default weekly schedule.
- **Config via .env**: Toggle prod/debug, mailer, sender info, AI.
- **SQLite Database**: Uses Peewee ORM with CSV seeding on first run.

## Project Structure

```
project-me-practice/
├── projectmepractice/           # Main package
│   ├── __init__.py              # Public exports
│   ├── const.py                 # Env + constants (mailer, flags)
│   ├── db.py                    # Peewee models + init
│   ├── users.py                 # User CRUD helpers
│   ├── projects.py              # CSV seed + selection
│   ├── allocations.py           # Allocation helpers
│   ├── practice.py              # Allocation + email content
│   └── types.py                 # Type aliases
├── email-templates/
│   ├── project.html             # Project email template
│   └── welcome.html             # Welcome email template
├── main.py                      # Batch run for subscribers
├── onboarding.py                # First-time welcome + project
├── example_projects.csv         # Sample seed CSV (columns below)
├── prod.projects.db.csv         # Production seed CSV (optional)
├── subscribed_users.db.csv      # Subscribers (name,email)
├── db.sqlite3                   # SQLite database (generated)
├── setup.sh                     # Setup: .env, venv, deps, init db
├── run.sh                       # Wrapper to run main.py
├── schedule.sh                  # Cron job registration
├── requirements.txt             # Dependencies
├── .env.template                # Copy to .env and fill
└── debug-email.html             # Last rendered email (debug)
```

## Data Model (SQLite)

- **Projects** (`Projects`)
  - `id` (UUID, PK), `title`, `description`, `domain`, `duration` (weeks), `group_id` (nullable), `group_part` (nullable)
- **Users** (`Users`)
  - `id` (UUID, PK), `name`, `email` (unique), `created_on` (date), `week_number` (int), `is_active` (bool), `current_project` (FK nullable)
- **Allocations** (`Allocations`)
  - `id` (UUID, PK), `user` (FK), `project` (FK), `date` (date)

CSV seed file columns (for `example_projects.csv` / `prod.projects.db.csv`):
- `Project Idea`, `Description`, `Domain`, `Weeks`, `Group`, `Step`

Subscribers file (`subscribed_users.db.csv`):
- Header: `name,email`

## Installation & Setup

### Prerequisites

- Python 3.10+ recommended
- Bash shell (Linux/macOS) or WSL/Git Bash (Windows)
- Email provider credentials (MailerSend API or SMTP)

### Quick Start

1) Clone and enter the repo
```bash
git clone <repository-url>
cd project-me-practice
```

2) Run setup (creates `.env`, `.venv`, installs deps, initializes DB)
```bash
chmod +x setup.sh
./setup.sh
```

3) Fill `.env` if prompted (minimal required):
```
PROD_MODE="false"
EMAIL_SENDER_NAME="Project Bot"
EMAIL_SENDER_ADDRESS="no-reply@your-domain.com"
MAILER_CLIENT="mailersend"   # or "smtp"
MAILERSEND_API_KEY="<your-key>"  # if using MailerSend
AI_FEATURES_ENABLED="false"   # set true + OPENAI_API_KEY to enable
```

Windows without WSL: activate venv and run directly
```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\main.py
```

## Running

Single run (uses `subscribed_users.db.csv`; writes `debug-email.html` when not in prod):
```bash
./run.sh
```

Schedule weekly (default: Saturday 7:30 AM):
```bash
chmod +x schedule.sh
./schedule.sh --register
```

Custom schedule (example: Monday 9 AM):
```bash
./schedule.sh --custom "0 9 * * 1"
```

## Programmatic Usage

```python
from projectmepractice import (
    feed_all_projects,
    register_user,
    allocate_next_project_for_user,
    fetch_all_projects,
    build_html_content,
)

# Seed projects from CSV (first run)
feed_all_projects("example_projects.csv")  # or "prod.projects.db.csv"

# Create or fetch a user
user = register_user("Jane Doe", "jane@example.com")

# Allocate next project (continues group steps when applicable)
project = allocate_next_project_for_user(user)

# Optional: render email HTML using the built-in template
html = build_html_content(
    template_path="email-templates/project.html",
    data={
        **project.to_dict(),
        "recipient_name": user.name,
        "sender_name": "Project Bot",
        "current_week": str(user.week_number or 1),
        "date": "January 01, 2026",
    },
    variable_map={"name": "title"},
)
```

Additional helpers are available:
- Users: `fetch_registered_users`, `modify_user_email`, `unregister_user` (import from `projectmepractice.users`)
- Allocations: `fetch_allocated_projects`, `fetch_allocations` (import from `projectmepractice.allocations`)

## Email Configuration

- **Debug (PROD_MODE="false")**: writes the last email to `debug-email.html`.
- **Production (PROD_MODE="true")**: sends via `email_me_anything` using:
  - `MAILER_CLIENT=mailersend` + `MAILERSEND_API_KEY`, or
  - `MAILER_CLIENT=smtp` + `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`.

Optional AI expansion (set `AI_FEATURES_ENABLED="true"` and `OPENAI_API_KEY`) augments the email with a concise AI-generated PRD fragment.

## Troubleshooting

- python3 not found: install Python 3.10+.
- Missing .env or venv: run `./setup.sh`.
- Packages missing: activate venv then `pip install -r requirements.txt`.
- Emails not sending: check `PROD_MODE`, `MAILER_CLIENT` and credentials in `.env`.
- Cron not running: `crontab -l` and system logs.

## Dependencies

- email_me_anything
- peewee
- openai (only required if AI features are enabled)

See requirements.txt for exact versions.

## Notes

- Projects and PRD expansion (if enabled) are AI-generated; validate before use.
- SQLite database is created automatically; CSV files are for seeding and subscribers.
- `run.sh` is Linux/macOS oriented; on Windows prefer WSL or run `python main.py` with an activated venv.

## Roadmap

- Difficulty selection and user preferences
- Web UI for user management
- Additional email providers and templates

## Contributing

Found issues or have suggestions? Please open an issue or PR.
