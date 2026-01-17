from openai import OpenAI
from functools import cache

from .allocations import allocate_project_to_user, fetch_allocated_projects
from .projects import fetch_all_projects, fetch_next_project_in_group, fetch_random_project
from .db import User, Project

from .const import AI_FEATURES_ENABLED, _AI_INSTRUCTION_PROMPT, _AI_INPUT_TEMPLATE, _AI_EMAIL_INJECTION_TEMPLATE

client = OpenAI()

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

def __generate_document(data:dict):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        temperature=0,
        messages=[
            {"role":"system", "content":_AI_INSTRUCTION_PROMPT},
            {"role":"user", "content":_AI_INPUT_TEMPLATE.format(**data)}
        ],
        reasoning_effort="none"
    )
    print(f"Used {response.usage.total_tokens} tokens")
    return response.choices[0].message.content

@cache
def __get_template_content(template_path:str):
    template = ""
    with open(template_path, 'r') as file:
        template = file.read()
    return template

def build_html_content(template_path:str, data:dict, variable_map:dict|None=None) -> str:
    if variable_map is not None:
        for key in variable_map:
            data[key] = data[variable_map[key]]
    template = __get_template_content(template_path)
    if AI_FEATURES_ENABLED:
        try:
            generated_html = __generate_document(data)
        except Exception as e:
            print("practice:60:",e)
            
        if len(generated_html) > 0:
            data["description"] = _AI_EMAIL_INJECTION_TEMPLATE.format(short_description=data["description"], generated_html=generated_html)
    
    return template.format(**data)