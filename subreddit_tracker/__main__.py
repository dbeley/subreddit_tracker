import argparse
import logging
import time
import locale
import praw
import datetime
import pkg_resources
from pathlib import Path
from .db_utils import SubredditTrackerDB
from threading import Thread, RLock

logger = logging.getLogger()
logging.getLogger("prawcore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
temps_debut = time.time()
AUJ = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
SUPPORTED_BACKENDS = ["csv", "sqlite"]
EXPORT_DIRECTORY = "Exports"
db_lock = RLock()


class subreddit_tracker_thread(Thread):
    def redditconnect(self, bot):
        user_agent = "python:bot"

        self.api = praw.Reddit(bot, user_agent=user_agent)

    def write_header_file(self, filename):
        columns = "Name,Date,Subscribers,Live_Users\n"
        with open(filename, "w") as f:
            f.write(columns)

    def extract_data_from_subreddit(self, subreddit):
        try:
            # logger.debug(
            #     "Thread %s - Extracting infos for subreddit %s.",
            #     self.reddit_account,
            #     subreddit,
            # )
            subscribers_count = self.api.subreddit(subreddit).subscribers
            live_users = self.api.subreddit(subreddit).accounts_active

            # logger.debug(
            #     "Thread %s - /r/%s : %s subscribers, %s live users.",
            #     self.reddit_account,
            #     subreddit,
            #     subscribers_count,
            #     live_users,
            # )
            infos = [
                str(subreddit),
                str(AUJ),
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
            f"{EXPORT_DIRECTORY}/subreddits_subscribers_count.csv"
        )
        if not Path(global_filename).is_file():
            write_header_file(global_filename)

        # Global export file
        with open(global_filename, "a+") as f:
            for i in self.list_infos:
                f.write(",".join(i) + "\n")
        logger.info("Export to csv %s. DONE.", self.reddit_account)
        return None

    def export_list_infos_to_sqlite(self):
        db_filename = f"{EXPORT_DIRECTORY}/subreddit_tracker.db"
        subreddit_tracker_db = SubredditTrackerDB(db_filename)
        subreddit_tracker_db.insert_to_table(self.list_infos)
        subreddit_tracker_db.quit()
        logger.info("Export to sqlite %s. DONE.", self.reddit_account)

    def __init__(self, reddit_account, subreddits, backend):
        Thread.__init__(self)
        self.reddit_account = reddit_account
        self.subreddits = subreddits
        self.length = len(subreddits)
        # self.api = api
        self.redditconnect(reddit_account)
        self.backend = backend
        logger.info("Init thread %s.", self.reddit_account)

    def run(self):
        logger.info("Running thread %s.", self.reddit_account)
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

        with db_lock:
            logger.info("Using database for %s.", self.reddit_account)
            if self.backend == "csv":
                self.export_list_infos_to_csv()
            elif self.backend == "sqlite":
                self.export_list_infos_to_sqlite()


def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))


def main():
    args = parse_args()
    locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")

    logger.debug("Subreddit list parsing.")
    if args.backend not in SUPPORTED_BACKENDS:
        logger.error("%s not a supported backend. Exiting.", args.backend)
        exit()
    if args.file is None:
        logger.info("Using default subreddits_list.txt.")
        file = pkg_resources.resource_string(__name__, "subreddits_list.txt")
        subreddits = file.decode("utf-8").split("\n")
        subreddits = subreddits[:-1]
    else:
        logger.debug("Using %s custom list.", args.file)
        with open(args.file, "r") as f:
            subreddits = f.readlines()
        subreddits = [x.strip() for x in subreddits]
    logger.debug("%s subreddits loaded.", len(subreddits))

    Path(EXPORT_DIRECTORY).mkdir(parents=True, exist_ok=True)

    subreddits_list = list(chunker_list(subreddits, args.nb_threads))

    threads = []
    for index, l in enumerate(subreddits_list, 1):
        reddit_account = f"reddit_bot_{index}"
        t = subreddit_tracker_thread(reddit_account, l, args.backend)
        # t = Thread(target=check_url, args=(url,))
        t.start()
        threads.append(t)

    # thread_1 = subreddit_tracker_thread(
    #     "reddit1", subreddits_list[0], args.backend
    # )
    # thread_2 = subreddit_tracker_thread(
    #     "reddit2", subreddits_list[1], args.backend
    # )
    # thread_3 = subreddit_tracker_thread(
    #     "reddit3", subreddits_list[2], args.backend
    # )
    # thread_4 = subreddit_tracker_thread(
    #     "reddit4", subreddits_list[3], args.backend
    # )
    # thread_5 = subreddit_tracker_thread(
    #     "reddit5", subreddits_list[4], args.backend
    # )

    # thread_1.start()
    # thread_2.start()
    # thread_3.start()
    # thread_4.start()
    # thread_5.start()

    # join all threads
    for t in threads:
        t.join()

    # thread_1.join()
    # thread_2.join()
    # thread_3.join()
    # thread_4.join()
    # thread_5.join()

    logger.info(
        "Subreddit_tracker runtime : %.2f seconds"
        % (time.time() - temps_debut)
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract subscribers and live users count of a list of subreddit defined in a text file."
    )
    parser.add_argument(
        "--debug",
        help="Display debugging information",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "-f",
        "--file",
        help="File containing the subreddits (Default : sample file containing popular subreddits)",
        type=str,
    )
    parser.add_argument(
        "-n",
        "--nb_threads",
        help="Number of threads to use. Be sure to have corresponding entries in your praw.ini file (reddit_bot_1... reddit_bot_N).",
        type=int,
        default=1,
    )
    parser.add_argument(
        "-b",
        "--backend",
        help="Backend to store the extracted data (sqlite or csv, Default : csv).",
        type=str,
        default="csv",
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == "__main__":
    main()
