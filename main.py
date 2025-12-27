from random import randint
import csv

from dotenv import load_dotenv
load_dotenv()

from os import getenv

from mailersend import MailerSendClient, EmailBuilder

from datetime import datetime

ID, GROUP, STEP, DOMAIN, NAME, DESCRIPTION, DURATION = range(7)

PROJECTS_BANK = getenv("PROJECTS_BANK")

projects_table = []
try:
    with open(PROJECTS_BANK, mode='r') as file:
        projects_table = [row for row in csv.reader(file)]
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit(1)    

headers_row = [0]
random_row = randint(1, len(projects_table) - 1)
project = projects_table[random_row]

while project[STEP] not in ["1", ""]:
    print(f"Step...{project[STEP]}..Stepping back...")
    random_row -= 1
    project = projects_table[random_row]
    
print(f"Random Project Selected: {project}")

with open("email-template.html", "r", encoding="utf-8") as file:
    html_template = file.read()

html_content = html_template.format_map(
    {
        "recipient_name": getenv("EMAIL_RECIPIENT_0_NAME"),
        "id": project[ID],
        "tags" : f"{(project[DOMAIN]+' Domain') if project[DOMAIN] else ''}{' · Group ' + project[GROUP] if project[GROUP] else ''}{' · Step ' + project[STEP] if project[STEP] else ''} · {project[DURATION]} {'Weeks' if project[DURATION]!='1' else 'Week'}",
        "group": project[GROUP],
        "step": project[STEP],
        "domain": project[DOMAIN],
        "name": project[NAME],
        "description": project[DESCRIPTION],
        "duration": project[DURATION],
        "date": datetime.now().strftime("%B %d, %Y"),
        "current_week": 1,
        "sender_name": getenv("EMAIL_SENDER")
    }
)

if getenv("DEBUG_MODE", "true").lower() == "false":
    ms = MailerSendClient()
    
    email = (EmailBuilder()
            .from_email(getenv("EMAIL_SENDER_ADDRESS"), getenv("EMAIL_SENDER"))
            .to_many([{"email": getenv("EMAIL_RECIPIENT_0_ADDRESS"), "name": getenv("EMAIL_RECIPIENT_0_NAME")}])
            .subject(f"New Project! 🚀 - #{project[ID]}")
            .html(html_content)
            .build())

    response = ms.emails.send(email)

    print(f"Email sent: {response.to_dict()}")

else:
    print("Debug mode is ON. Writing email to debug-email.html")
    with open("debug-email.html", "w", encoding="utf-8") as debug_file:
        debug_file.write(html_content)
