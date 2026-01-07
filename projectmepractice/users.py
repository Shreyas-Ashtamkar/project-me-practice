from .db import User, ModelSelect

def register_user(name:str, email:str) -> User:
    existing_user = User.select().where(User.email == email)
    if existing_user.count() > 0:
        return existing_user.get()
    new_user = User.create(name=name, email=email)
    return new_user

def fetch_registered_users() -> ModelSelect:
    users = User.select()
    return users

def modify_user_email(user:User, new_email:str) -> User:
    user.email = new_email
    user.save()
    return user

def add_user_week(user:User) -> User:
    user.week_number += 1
    user.save()
    return user

def unregister_user(user:User) -> User:
    user.delete_instance()
    return user