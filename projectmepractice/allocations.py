import datetime, csv
from uuid import uuid4

from .const import PROJECT_ALLOCATIONS_DB

def fetch_allocated_projects(user_id:str|None=None):
    allocated_projects = []
    try:
        if user_id is None:
            with open(PROJECT_ALLOCATIONS_DB, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    allocated_projects.append(row)
        else:
            with open(PROJECT_ALLOCATIONS_DB, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["user"] == user_id:
                        allocated_projects.append(row)
    except FileNotFoundError:
        print("No allocations found.")
    except Exception as e:
        print(f"Error fetching allocated projects: {e}")
    return allocated_projects
        
def allocate_project_to_user(project_id:str, user_id:str):
    new_allocation = {
        "id": str(uuid4()),
        "project": project_id,
        "user": user_id,
        "date": datetime.datetime.now().isoformat()
    }
    
    with open(PROJECT_ALLOCATIONS_DB, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_allocation.keys())
        if f.tell() == 0:  # Write header if file is empty
            writer.writeheader()
        writer.writerow(new_allocation)
    return new_allocation

def deallocate_project_from_user(project_id:str, user_id:str):
    all_projects = fetch_allocated_projects()
    deleted_project = None
    with open(PROJECT_ALLOCATIONS_DB, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "project", "user", "date"])
        writer.writeheader()
        for project in all_projects:
            if not (project["project"] == project_id and project["user"] == user_id):
                writer.writerow(project)
            else:
                deleted_project = project
    return deleted_project
