from random import randint
import csv

from dotenv import load_dotenv
load_dotenv()

from os import getenv

from mailersend import MailerSendClient, EmailBuilder

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
    
ms = MailerSendClient()

email = (EmailBuilder()
         .from_email("info@domain.com", "Sender Name")
         .to_many([{"email": "shreyas.ashtamkar18@gmail.com", "name": "Recipient"}])
         .subject("Hello from MailerSend!")
         .html("Hello World!")
         .text("Hello World!")
         .build())

response = ms.emails.send(email)
print(f"Email sent: {response.message_id}")
