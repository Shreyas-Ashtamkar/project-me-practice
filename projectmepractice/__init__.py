from .users import register_user
from .projects import feed_all_projects, feed_all_projects, fetch_all_projects
from .practice import allocate_next_project_for_user, build_html_content
from .const import PROD_MODE, EMAIL_SENDER_ADDRESS, EMAIL_SENDER_NAME, AI_FEATURES_ENABLED
from .types import ProjectType, UserType, AllocationType

def db_initialized():    
    return bool(fetch_all_projects().get_or_none())
        