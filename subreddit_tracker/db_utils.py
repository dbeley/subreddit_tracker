import sqlite3
import logging

logger = logging.getLogger()


class SubredditTrackerDB:
    def __init__(self, db_name="subreddit_tracker.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table("measures")

    def create_table(self, name):
        try:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS %s (Name text, Date text, Subscribers int, Live_Users int)"""
                % name
            )
            self.conn.commit()
        except Exception as e:
            logger.warning(e)

    def insert_to_table(self, list_tuples):
        for i in list_tuples:
            subreddit_name = i[0]
            self.create_table(subreddit_name)
            self.cursor.execute("INSERT INTO %s VALUES (?,?,?,?)" % subreddit_name, i)

    def return_all_rows(self):
        for i in self.cursor.execute("SELECT * FROM measures"):
            yield i

    def quit(self):
        self.conn.commit()
        self.conn.close()
