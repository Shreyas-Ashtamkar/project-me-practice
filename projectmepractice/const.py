from dotenv import load_dotenv
from os import getenv

load_dotenv()

PROD_MODE=getenv("PROD_MODE", "false").lower() == "true"

PROJECTS_DB = getenv("PROJECTS_DB", "projects.db.csv")
PROJECT_ALLOCATIONS_DB = getenv("PROJECT_ALLOCATIONS_DB", "allocations.db.csv")
USERS_DB = getenv("USERS_DB", "users.db.csv")

DATABASE_URL = getenv("DATABASE_URL", "db.sqlite3")
USERS_TABLE = getenv("USERS_TABLE", "Users")
PROJECTS_TABLE = getenv("PROJECTS_TABLE", "Projects")
ALLOCATIONS_TABLE = getenv("ALLOCATIONS_TABLE", "Allocations")

AI_FEATURES_ENABLED=getenv("AI_FEATURES_ENABLED", "false") == "true"

# mandatory settings
EMAIL_SENDER_ADDRESS=getenv("EMAIL_SENDER_ADDRESS")
EMAIL_SENDER_NAME=getenv("EMAIL_SENDER_NAME")

if PROD_MODE:
    if getenv("MAILERSEND_API_KEY") is None:
        raise EnvironmentError("MAILERSEND_API_KEY must be set in production mode.")


if AI_FEATURES_ENABLED:
    if getenv("OPENAI_API_KEY") is None:
        raise EnvironmentError("OPENAI_API_KEY must be set if AI features are enabled.")