from .allocations import allocate_project_to_user, fetch_allocated_projects
from .projects import fetch_all_projects, fetch_next_project_in_group, fetch_random_project
from .db import User, Project

# TODO: Fix Problem -> Project only selected in group again and again
def allocate_next_project_for_user(user:User) -> Project:
    selected_project = None
    
    if user.current_project and user.current_project.has_parts:
        selected_project = fetch_next_project_in_group(user.current_project)
    
    if not selected_project:
        allocated_projects = fetch_allocated_projects(user=user)
        unallocated_projects = fetch_all_projects(except_=allocated_projects)
        selected_project = fetch_random_project(unallocated_projects)

    if selected_project is not None:
        allocate_project_to_user(selected_project, user)
    else:
        raise LookupError("No new projects available for allocation.")
    return selected_project