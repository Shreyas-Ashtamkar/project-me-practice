if __name__ == "__main__":
    import time, main
    if not main.db_initialized():
        main.feed_all_projects("example_projects.csv")
    for _ in range(6):
        main.run("Shreyas", "shreyas.ashtamkar18@gmail.com")
        time.sleep(1)
