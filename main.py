from datetime import datetime
from email_me_anything import build_html_content, send_email

from projectmepractice import (
    register_user, 
    feed_all_projects, 
    allocate_next_project_for_user, 
    PROD_MODE, 
    EMAIL_SENDER_ADDRESS, 
    EMAIL_SENDER_NAME,
    UserType, ProjectType, AllocationType,
    db_initialized
)

def send_project_to_user(user:UserType, project:ProjectType) -> str:
    data = {
        **project.to_dict(),
        'current_week': "1",
        'recipient_name': user.name,
        'sender_name': EMAIL_SENDER_NAME,
    }
    
    print(f"Project #{project.id} allocated to {user.name}")
    html_content = build_html_content(
        template_path="email-template.html",
        data = data,
        variable_map={
            "id" : "id",
            "name" : "title",
            "description" : "description",
            "tags" : "tags",
            "current_week": "current_week",
            "recipient_name": "recipient_name",
            "sender_name": "sender_name",
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
        with open("debug-email.html", "w") as f:
            f.write(html_content)
        status = "Skipped......"
    
    return status

def run(name:str, email:str):
    if not db_initialized():
        feed_all_projects("500ProjectsList.csv")
    
    user = register_user(name, email)
    new_allocated_project = allocate_next_project_for_user(user=user)
    
    status = send_project_to_user(user, new_allocated_project)
    print("Email sent status:", status)


if __name__ == "__main__":
    run("Shreyas", "shreyas.ashtamkar18@gmail.com")
    # run("Priyanka", "priyanka.c.ashtamkar@gmail.com")