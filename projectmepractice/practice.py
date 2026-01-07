from .allocations import allocate_project_to_user, fetch_allocated_projects
from .projects import fetch_all_projects
from .db import User, Project
import random

# TODO : Improve selection logic to inculcate the GROUPS and STEPS of the projects
def allocate_next_project_for_user(user:User) -> Project:
    all_projects = fetch_all_projects()
    allocated_projects = fetch_allocated_projects(user=user)
    unallocated_projects = all_projects.except_(allocated_projects)
    if unallocated_projects.count() > 0:
        selected_project = random.choice(list(unallocated_projects))  
    else:
        selected_project = None
    if selected_project is not None:
        allocate_project_to_user(selected_project, user)
    else:
        raise LookupError("No new projects available for allocation.")
    return selected_project