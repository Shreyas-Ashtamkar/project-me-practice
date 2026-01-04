from datetime import datetime
from projectmepractice import register_new_user, feed_all_projects, allocate_next_project_for_user
from email_me_anything import build_html_content, send_email

from os import getenv

EMAIL_DISABLE = getenv("PROD_MODE", "false").lower() != "true"  # Set to False to enable email sending
SENDER_NAME = getenv("EMAIL_SENDER_NAME", "Project Bot")
SENDER_EMAIL = getenv("EMAIL_SENDER_EMAIL", "bot@dev-master.in")

if __name__ == "__main__":
    feed_all_projects("500ProjectsList.csv")
    user = register_new_user("Shreyas", "shreyas.ashtamkar18@gmail.com")
    allocated_project = allocate_next_project_for_user(user_id=user["id"])
    data = {
        **allocated_project,
        'current_week': "1",
        'recipient_name': user['name'],
        'sender_name': SENDER_NAME,
        'tags' : (
            f"{allocated_project['domain']} Domain"
            + (f" | Group {allocated_project['group_id']} | Step {allocated_project['group_part']}" if allocated_project['has_parts'] == 'True' else "")
            + f" | {allocated_project['duration']}" + (" Week" if allocated_project['duration']=='1' else " Weeks")
        )
    }
    
    print(f"Project #{allocated_project['id']} allocated to {user['name']}")
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
    
    if EMAIL_DISABLE is False:
        status = send_email(
            sender={"email": SENDER_EMAIL, "name": SENDER_NAME},
            recipients=[{"email": user["email"], "name": user["name"]}],
            subject = datetime.now().strftime("%B %d, %Y"),
            html_content = html_content
        )
        
    else:
        with open("debug-email.html", "w") as f:
            f.write(html_content)
        status = "Skipped......"
    
    print("Email sent status:", status)