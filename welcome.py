from datetime import datetime
from typing import overload
from email_me_anything import send_email

from projectmepractice.types import UserType
from projectmepractice import build_html_content, register_user

from projectmepractice.const import (
    PROD_MODE,
    EMAIL_SENDER_NAME,
    EMAIL_SENDER_ADDRESS
)

def send_greeting_to_user(user:UserType):
    data = {
        'current_week': "1",
        'recipient_name': user.name,
        'sender_name': EMAIL_SENDER_NAME,
        'date': datetime.now().strftime("%B %d, %Y")
    }
    print(f"Welcoming {user.name}.")
    html_content = build_html_content(
        template_path="email-templates/welcome.html",
        data=data,
        simple=True #Disable AI for greeting, as it's not implemented
    )
    print("Built HTML template")
    if PROD_MODE:
        status = send_email(
            sender={"email": EMAIL_SENDER_ADDRESS, "name": EMAIL_SENDER_NAME},
            recipients=[{"email": user.email, "name": user.name}],
            subject = "Welcome to Practice Me Project",
            html_content = html_content
        )
    else:
        with open("debug-email.html", "w", encoding="utf-8", newline="\n") as f:
            f.write(html_content)
        status = {"status":"Skipped......", "message":"PROD mode is off"}
    return status

def welcome_user(name:str, email:str):
    user = register_user(name, email)
    if user.is_new:
        status = send_greeting_to_user(user)
        print(f"Email sending (greeting) to {user.name}:", status["status"])
    else:
        print("User Old")

if __name__ == "__main__":
    from os import getenv
    from pathlib import Path
    from concurrent.futures import ThreadPoolExecutor
    
    subscribed_users_file = Path("subscribed_users.db.csv")
    
    MUTI_THREADED_EXECUTION = getenv("MUTI_THREADED_EXECUTION", "false") == "true"
    
    if subscribed_users_file.exists():
        SUBSCRIBER_FILE_PRESENT = True
        NAME,EMAIL=0,1
        with open(subscribed_users_file, 'r') as input_file:
            recepients = input_file.readlines()[1:]
            SUBSCRIBER_FILE_PRESENT = len(recepients)>0
    
    if SUBSCRIBER_FILE_PRESENT:
        def process_recipient(recipient_line:str):
            recipient = recipient_line.split(",")
            welcome_user(recipient[NAME], recipient[EMAIL].strip())
        
        if MUTI_THREADED_EXECUTION:
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(process_recipient, recepients)
        else:
            for recipient in recepients:
                process_recipient(recipient)