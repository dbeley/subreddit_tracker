""" Add content from a csv file created by subreddit_tracker to a new or existing database."""
from subreddit_tracker import db_utils


# If subreddit_tracker.db file doesn't exist, it will be created.
print("Opening or creating database subreddit_tracker.db.")
db = db_utils.SubredditTrackerDB()

# Open csv file
print("Reading csv file.")
with open("subreddits_subscribers_count_2019-07-02.csv") as f:
    # Create tuples from csv file
    lines = [x.strip().split(",") for x in f.readlines()]

# Fill tuples if 4th field doesn't exist
for index, x in enumerate(lines):
    if len(x) == 3:
        lines[index] = x + [None]

# Insert tuples into database
print("Inserting data.")
db.insert_to_table(lines)
db.quit()
