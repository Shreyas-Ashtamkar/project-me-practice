if __name__ == "__main__":
    import os
    from projectmepractice.db import initialize_db, DATABASE_URL
    from projectmepractice.projects import feed_all_projects
    
    if os.path.exists(DATABASE_URL):
        print("Database already exists")
    else:
        initialize_db()
        print("Tables Created.")