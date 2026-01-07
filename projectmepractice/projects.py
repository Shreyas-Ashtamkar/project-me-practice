import csv, random
from pathlib import Path

from .db import Project, ModelSelect, db

def feed_all_projects(file_name:Path) -> ModelSelect:
    projects_list = []
    try:
        with db.atomic():
            with open(file_name, "r") as file:
                for row_data in csv.DictReader(file):
                    project = Project.create(
                        title=row_data.get("Project Idea", ""),
                        description=row_data.get("Description", ""),
                        domain=row_data.get("Domain", ""),
                        duration=int(row_data.get("Weeks", 1)),
                        group_id=row_data.get("Group", ""),
                        group_part=row_data.get("Step", None),
                    )
                    projects_list.append(project)
            print(f"{len(projects_list)} projects added to DB.")
    except FileNotFoundError:
        print("Project DB not created, run feed_all_projects with a valid file.")
    except Exception as e:
        print(f"Error feeding projects: {e}")
    return projects_list

def fetch_all_projects(*args) -> ModelSelect:
    return Project.select(*args)

# User except_ with another query of selected projects - users' already selected
# def select_random_project(exclude_projects:ModelSelect)
def select_random_project() -> Project:
    selected_project = random.choice(list(fetch_all_projects()))
    return selected_project