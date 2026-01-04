import csv
from uuid import uuid4
from datetime import datetime

from .const import USERS_DB

def register_new_user(name, email):
    users = fetch_registered_users()
    new_user = None
    for user in users:
        if user["email"] == email:
            print("User with this email already exists.")
            new_user = user
            break
    else:
        new_user = {
            "id": str(uuid4()),
            "name": name,
            "email": email,
            "created_on": datetime.now().isoformat()
        }
        with open(USERS_DB, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=new_user.keys())
            if f.tell() == 0:  # Write header if file is empty
                writer.writeheader()
            writer.writerow(new_user)
    return new_user

def fetch_registered_users():
    users = []
    with open(USERS_DB, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row)
    return users

def modify_user_email(user_id, new_email):
    users = fetch_registered_users()
    modified_user = None
    with open(USERS_DB, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "email", "created_on"])
        writer.writeheader()
        for user in users:
            if user["id"] == user_id:
                user["email"] = new_email
                modified_user = user
            writer.writerow(user)
    return modified_user

def delete_user(user_id):
    users = fetch_registered_users()
    with open(USERS_DB, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "email", "created_on"])
        writer.writeheader()
        for user in users:
            if user["id"] != user_id:
                writer.writerow(user)
    return fetch_registered_users()