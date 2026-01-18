from datetime import datetime
from email_me_anything import send_email

from projectmepractice.types import UserType, ProjectType
from projectmepractice import (
    register_user, 
    feed_all_projects, 
    allocate_next_project_for_user, 
    db_initialized,
    build_html_content
)

from projectmepractice.const import (
    PROD_MODE, 
    EMAIL_SENDER_ADDRESS, 
    EMAIL_SENDER_NAME
)

from welcome import welcome_user

def send_project_to_user(user:UserType, project:ProjectType) -> str:
    data = {
        **project.to_dict(),
        'current_week': "1",
        'recipient_name': user.name,
        'sender_name': EMAIL_SENDER_NAME,
        'date': datetime.now().strftime("%B %d, %Y")
    }
    print(f"Project #{project.id} allocated to {user.name}")
    html_content = build_html_content(
        template_path="email-templates/project.html",
        data = data,
        variable_map={
            "name" : "title"
        }
    )
    if PROD_MODE:
        status = send_email(
            sender={"email": EMAIL_SENDER_ADDRESS, "name": EMAIL_SENDER_NAME},
            recipients=[{"email": user.email, "name": user.name}],
            subject = "New Practice Project - " + datetime.now().strftime("%B %d, %Y"),
            html_content = html_content
        )
    else:
        with open("debug-email.html", "w", encoding="utf-8", newline="\n") as f:
            f.write(html_content)
        status = {"status":"Skipped......", "message":"PROD mode is off"}
    return status

def run(name:str, email:str):
    user = register_user(name, email)
    if user.is_new:
        # welcome_user(name, email)
        new_allocated_project = allocate_next_project_for_user(user=user)
        status = send_project_to_user(user, new_allocated_project)
        print(f"Email sending (project) to {name}:", status["status"])

if __name__ == "__main__":
    from os import getenv
    from pathlib import Path
    from concurrent.futures import ThreadPoolExecutor
    
    subscribed_users_file = Path("subscribed_users.db.csv")
    projects_file = Path("prod.projects.db.csv")
    projects_file = projects_file if projects_file.exists() else Path("example_projects.csv")
    
    MUTI_THREADED_EXECUTION = getenv("MUTI_THREADED_EXECUTION", "false") == "true"
    
    if not db_initialized():
        feed_all_projects(projects_file)
        
    if subscribed_users_file.exists():
        SUBSCRIBER_FILE_PRESENT = True
        NAME,EMAIL=0,1
        with open(subscribed_users_file, 'r') as input_file:
            recepients = input_file.readlines()[1:]
            SUBSCRIBER_FILE_PRESENT = len(recepients)>0
                
    if SUBSCRIBER_FILE_PRESENT:
        def process_recipient(recipient_line:str):
            recipient = recipient_line.split(",")
            run(recipient[NAME], recipient[EMAIL].strip())
        
        if MUTI_THREADED_EXECUTION:
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(process_recipient, recepients)
        else:
            for recipient in recepients:
                process_recipient(recipient)
            
    else:
        run("Shreyas", "shreyas.ashtamkar18@gmail.com")