import csv, random
from .const import PROJECTS_DB
from email_me_anything import select_random_row

def create_project(pid, name, description, domain, group='', step=None, weeks=1):
    has_parts = bool(len(group))
    return {
        "id": pid,
        "title":name,
        "description":description,
        "domain":domain,
        "duration":weeks,
        "has_parts":has_parts,
        "group_id":group if has_parts else "",
        "group_part":step if group else ""
    }

def save_project(project_data):
    with open(PROJECTS_DB, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=project_data.keys())
        if f.tell() == 0:  # Write header if file is empty
            writer.writeheader()
        writer.writerow(project_data)
        f.close()
    return project_data

def save_all_projects(projects_list):
    with open(PROJECTS_DB, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "description", "domain", "duration", "has_parts", "group_id", "group_part"])
        writer.writeheader()
        for project in projects_list:
            writer.writerow(project)
    return projects_list

def feed_all_projects(file_name):
    projects_list = []
    try:
        with open(file_name, "r") as file:
            for row_data in csv.DictReader(file):
                projects_list.append(create_project(
                    pid=row_data.get("ID", ""),
                    name=row_data.get("Project Idea", ""),
                    description=row_data.get("Description", ""),
                    domain=row_data.get("Domain", ""),
                    group=row_data.get("Group", ""),
                    step=row_data.get("Step", None),
                    weeks=int(row_data.get("Weeks", 1))
                ))
    except FileNotFoundError:
        print("Project DB not created, run feed_all_projects with a valid file.")
    except Exception as e:
        print(f"Error feeding projects: {e}")
    
    save_all_projects(projects_list)
    return projects_list

def fetch_all_projects():
    projects = []
    try:
        with open(PROJECTS_DB, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                projects.append(row)
    except FileNotFoundError:
        print("No projects found.")
    except Exception as e:
        print(f"Error fetching projects: {e}")
    return projects

def select_random_project():
    selected_project = select_random_row(PROJECTS_DB)
    return selected_project