""" Add content from a sqlite file created by subreddit_tracker to a new or existing database."""
from subreddit_tracker import db_utils

# If subreddit_tracker.db file doesn't exist, it will be created.
print("Opening or creating database subreddit_tracker.db.")
db = db_utils.SubredditTrackerDB()

# Open csv file
print("Reading sqlite file.")
old_db = db_utils.SubredditTrackerDB("subreddit_tracker_amerger.db")

lines = [x for x in old_db.return_all_rows()]

# Insert tuples into database
print("Inserting data.")
db.insert_to_table(lines)
db.quit()
