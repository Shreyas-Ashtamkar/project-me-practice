import csv, random
from pathlib import Path

from .db import Project, ModelSelect, db
from peewee import DoesNotExist

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

def fetch_all_projects(except_:ModelSelect=None) -> ModelSelect:
    all_projects = Project.select()
    if except_ is not None:
        all_projects.except_(except_)
    return all_projects

def fetch_next_project_in_group(project:Project) -> Project:
    try:
        return project.next_group_part()
    except DoesNotExist:
        print("No new project in group")
    return None

def fetch_first_project_in_group(project:Project) -> Project:
    group_id = project.group_id
    project = None
    try:
        project = Project.get((Project.group_id == group_id) & (Project.group_part == "1"))
    except DoesNotExist:
        print("No new project in group")
    return project

def fetch_random_project(project_list:ModelSelect) -> Project:
    selected_project = None
    try:
        selected_project:Project = random.choice(project_list)
    
        if selected_project.has_parts:
            selected_project = fetch_first_project_in_group(selected_project)
    except DoesNotExist as err:
        print(f"Could not fetch random project")
            
    return selected_project