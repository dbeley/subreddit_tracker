from threading import Thread, RLock
import logging
import praw
from .db_utils import SubredditTrackerDB

logger = logging.getLogger(__name__)
DB_LOCK = RLock()


class SubredditTrackerThread(Thread):
    def redditconnect(self, bot):
        user_agent = "python:bot"

        self.api = praw.Reddit(bot, user_agent=user_agent)

    def write_header_file(self, filename):
        columns = "Name,Date,Subscribers,Live_Users\n"
        with open(filename, "w") as f:
            f.write(columns)

    def extract_data_from_subreddit(self, subreddit):
        try:
            subscribers_count = self.api.subreddit(subreddit).subscribers
            live_users = self.api.subreddit(subreddit).accounts_active

            logger.debug(
                "Thread %s - /r/%s : %s subscribers, %s live users.",
                self.reddit_account,
                subreddit,
                subscribers_count,
                live_users,
            )
            infos = [
                str(subreddit),
                str(self.date),
                str(subscribers_count),
                str(live_users),
            ]
        except Exception as e:
            logger.error(
                "Thread %s - Subreddit %s : %s.",
                self.reddit_account,
                subreddit,
                e,
            )
            return None
        return infos

    def export_list_infos_to_csv(self):
        global_filename = (
            f"{self.export_directory}/subreddits_subscribers_count.csv"
        )
        if not Path(global_filename).is_file():
            write_header_file(global_filename)

        with open(global_filename, "a+") as f:
            for i in self.list_infos:
                f.write(",".join(i) + "\n")
        logger.info("Export to csv %s. DONE.", self.reddit_account)
        return None

    def export_list_infos_to_sqlite(self):
        db_filename = f"{self.export_directory}/subreddit_tracker.db"
        subreddit_tracker_db = SubredditTrackerDB(db_filename)
        subreddit_tracker_db.insert_to_table(self.list_infos)
        subreddit_tracker_db.quit()
        logger.info("Export to sqlite %s. DONE.", self.reddit_account)

    def __init__(
        self, reddit_account, subreddits, date, backend, export_directory
    ):
        Thread.__init__(self)

        self.reddit_account = reddit_account
        self.subreddits = subreddits
        self.length = len(subreddits)
        self.date = date
        self.backend = backend
        self.export_directory = export_directory

        self.redditconnect(reddit_account)
        logger.debug("Init thread %s.", self.reddit_account)

    def run(self):
        logger.debug("Running thread %s.", self.reddit_account)
        self.list_infos = []
        for index, subreddit in enumerate(self.subreddits, 0):
            logger.debug(
                "Thread %s - Subreddit %s/%s : %s.",
                self.reddit_account,
                index,
                self.length,
                subreddit,
            )
            infos = self.extract_data_from_subreddit(subreddit)
            if infos:
                self.list_infos.append(infos)

        with DB_LOCK:
            logger.debug("Using database for %s.", self.reddit_account)
            if self.backend == "csv":
                self.export_list_infos_to_csv()
            elif self.backend == "sqlite":
                self.export_list_infos_to_sqlite()
