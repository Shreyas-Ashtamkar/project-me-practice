from dotenv import load_dotenv
from os import getenv

load_dotenv()

PROD_MODE=getenv("PROD_MODE", "false").lower() == "true"

DATABASE_URL = getenv("DATABASE_URL", "db.sqlite3")
USERS_TABLE = getenv("USERS_TABLE", "Users")
PROJECTS_TABLE = getenv("PROJECTS_TABLE", "Projects")
ALLOCATIONS_TABLE = getenv("ALLOCATIONS_TABLE", "Allocations")

AI_FEATURES_ENABLED=getenv("AI_FEATURES_ENABLED", "false") == "true"

# mandatory settings
EMAIL_SENDER_ADDRESS=getenv("EMAIL_SENDER_ADDRESS")
EMAIL_SENDER_NAME=getenv("EMAIL_SENDER_NAME")

# testing environment settings
if not getenv("EMAIL_SENDER_ADDRESS", False):
    raise EnvironmentError("EMAIL_SENDER_ADDRESS must be set.")

if not getenv("EMAIL_SENDER_NAME", False):
    raise EnvironmentError("EMAIL_SENDER_NAME must be set.")

if PROD_MODE:
    if getenv("MAILER_CLIENT", "mailersend") == "smtp":
        if not getenv("SMTP_HOST", False):
            raise EnvironmentError("SMTP_HOST must be set when using MAILER_CLIENT smtp.")
        if not getenv("SMTP_PORT", False):
            raise EnvironmentError("SMTP_PORT must be set when using MAILER_CLIENT smtp.")
        if not getenv("SMTP_USER", False):
            raise EnvironmentError("SMTP_USER must be set when using MAILER_CLIENT smtp.")
        if not getenv("SMTP_PASS", False):
            raise EnvironmentError("SMTP_PASS must be set when using MAILER_CLIENT smtp.")
    else:
        if not getenv("MAILERSEND_API_KEY", False):
            raise EnvironmentError("MAILERSEND_API_KEY must be set in production mode. If not available use MAILER_CLIENT=\"smtp\" with custom settings")

if AI_FEATURES_ENABLED:
    if not getenv("OPENAI_API_KEY", False):
        raise EnvironmentError("OPENAI_API_KEY must be set if AI features are enabled.")