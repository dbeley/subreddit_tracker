import sqlite3
import logging

logger = logging.getLogger()


class SubredditTrackerDB:
    def __init__(self, db_name="subreddit_tracker.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        try:
            self.cursor.execute(
                """CREATE TABLE measures (Name text, Date text, Subscribers int, Live_Users int)"""
            )
            self.conn.commit()
        except Exception as e:
            logger.warning(e)

    def insert_to_table(self, list_tuples):
        self.cursor.executemany(
            "INSERT INTO measures VALUES (?,?,?,?)", list_tuples
        )

    def return_all_rows(self):
        for i in self.cursor.execute("SELECT * FROM measures"):
            yield i

    def quit(self):
        self.conn.commit()
        self.conn.close()
