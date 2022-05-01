with open("subreddits_list.txt", "r") as f:
    subreddits = f.read().splitlines()

with open("script.sql", "w") as f:
    for i in subreddits:
        f.write(
            f"CREATE TABLE IF NOT EXISTS {i} (Name text, Date text, Subscribers int, Live_Users int);\n"
            f"INSERT INTO {i} SELECT * FROM measures where Name='{i}';\n"
        )
