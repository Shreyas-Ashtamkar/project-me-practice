from .practice import allocate_project_to_user, deallocate_project_from_user, fetch_allocated_projects
from .users import register_new_user, fetch_registered_users, modify_user_email, delete_user
from .projects import feed_all_projects, select_random_project

# TODO : Improve selection logic to inculcate the GROUPS and STEPS of the projects
def fetch_next_project_for_user(user_id:str):
    allocated_projects = fetch_allocated_projects(user_id=user_id)
    allocated_project_ids = {proj["project"] for proj in allocated_projects}
    selected_project = None
    for _ in range(500):
        selected_project = select_random_project()
        if selected_project["id"] not in allocated_project_ids:
            break
    else:
        print("Could not find a new project to allocate.")
    
    return selected_project

def allocate_next_project_for_user(user_id:str):
    project = fetch_next_project_for_user(user_id)
    if project is not None:
        allocate_project_to_user(project["id"], user_id)
    return project