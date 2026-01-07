from datetime import datetime
from email_me_anything import build_html_content, send_email

from projectmepractice import (
    register_user, 
    feed_all_projects, 
    allocate_next_project_for_user, 
    PROD_MODE, 
    EMAIL_SENDER_ADDRESS, 
    EMAIL_SENDER_NAME
)

if __name__ == "__main__":
    # feed_all_projects("500ProjectsList.csv")
    
    user = register_user("Shreyas", "shreyas.ashtamkar18@gmail.com")
    new_allocated_project = allocate_next_project_for_user(user=user)
    
    data = {
        **new_allocated_project.to_dict(),
        'current_week': "1",
        'recipient_name': user.name,
        'sender_name': EMAIL_SENDER_NAME,
    }
    
    print(f"Project #{new_allocated_project.id} allocated to {user.name}")
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
    
    print("Email sent status:", status)