from .db import User, Project, Allocation, ModelSelect
from .projects import fetch_all_projects

def fetch_allocations(user:User|None) -> ModelSelect:
    allocations = Allocation.select()
    if user is not None:
        allocations = allocations.where(Allocation.user == user)
    return allocations

def fetch_allocated_projects(user:User|None) -> ModelSelect:
    allocated_projects = fetch_all_projects().join(Allocation)
    if user is not None:
        allocated_projects = allocated_projects.where(Allocation.user == user)
    return allocated_projects
        
def allocate_project_to_user(project:Project, user:User) -> Allocation:
    new_allocation = Allocation.create(
        user=user,
        project=project,
    )
    user.week_number += 1
    user.current_project = project
    user.save()
    return new_allocation

def deallocate_project_from_user(user:User, project:Project) -> int:
    deallocated_project = Allocation.get((Allocation.user == user) & (Allocation.project == project))
    rows_deleted_count = deallocated_project.delete_instance()
    return rows_deleted_count
