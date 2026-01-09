from .allocations import allocate_project_to_user, fetch_allocated_projects
from .projects import fetch_all_projects, fetch_next_project_in_group, fetch_random_project
from .db import User, Project
from typing import List
import random

def get_new_project(project_list, current_project:Project):
    selected_project = None
    
    if not project_list:
        return None
    
    if current_project and current_project.has_parts:
        selected_project = fetch_next_project_in_group(current_project.group_id, current_project.group_part)
    
    if not selected_project:
        selected_project = fetch_random_project(project_list)
        
    return selected_project    

def allocate_next_project_for_user(user:User) -> Project:
    allocated_projects = fetch_allocated_projects(user=user)
    current_project = user.current_project
    
    if current_project:
        if user.current_project:
            unallocated_projects = fetch_all_projects(group_id=user.current_project.group_id, except_=allocated_projects)
        else:
            unallocated_projects = fetch_all_projects(except_=allocated_projects)
        
    selected_project = get_new_project(unallocated_projects, user.current_project)

    if selected_project is not None:
        allocate_project_to_user(selected_project, user)
    else:
        raise LookupError("No new projects available for allocation.")
    return selected_project