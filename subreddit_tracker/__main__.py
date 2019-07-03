import argparse
import logging
import time
import locale
import praw
import datetime
import pkg_resources
from pathlib import Path
from .db_utils import SubredditTrackerDB

logger = logging.getLogger()
temps_debut = time.time()
AUJ = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
SUPPORTED_BACKENDS = ["csv", "sqlite"]


def redditconnect(bot):
    user_agent = "python:bot"

    reddit = praw.Reddit(bot, user_agent=user_agent)
    return reddit


def write_header_file(filename):
    columns = "Name,Date,Subscribers,Live_Users\n"
    with open(filename, "w") as f:
        f.write(columns)


def extract_data_from_subreddit(reddit_api, subreddit):
    try:
        logger.debug("Extracting infos for subreddit %s", subreddit)
        subscribers_count = reddit_api.subreddit(subreddit).subscribers
        live_users = reddit_api.subreddit(subreddit).accounts_active

        logger.debug(
            "/r/%s : %s subscribers, %s live users",
            subreddit,
            subscribers_count,
            live_users,
        )
        infos = [
            str(subreddit),
            str(AUJ),
            str(subscribers_count),
            str(live_users),
        ]
    except Exception as e:
        logger.error("Subreddit %s: %s", subreddit, e)
        return None
    return infos


def export_list_infos_to_csv(directory, list_infos):
    global_filename = f"{directory}/subreddits_subscribers_count.csv"
    if not Path(global_filename).is_file():
        write_header_file(global_filename)

    # Global export file
    with open(global_filename, "a+") as f:
        for i in list_infos:
            f.write(",".join(i) + "\n")
    logger.info("Export to csv. DONE.")
    return None


def export_list_infos_to_sqlite(directory, list_infos):
    db_filename = f"{directory}/subreddit_tracker.db"
    subreddit_tracker_db = SubredditTrackerDB(db_filename)
    subreddit_tracker_db.insert_to_table(list_infos)
    subreddit_tracker_db.quit()
    logger.info("Export to sqlite. DONE.")


def main():
    args = parse_args()
    locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")

    logger.debug("Subreddit list parsing")
    if args.backend not in SUPPORTED_BACKENDS:
        logger.error("%s not a supported backend. Exiting.", args.backend)
        exit()
    if args.file is None:
        logger.info("Using default subreddit_list.txt")
        file = pkg_resources.resource_string(__name__, "subreddit_list.txt")
        subreddits = file.decode("utf-8").split("\n")
        subreddits = subreddits[:-1]
    else:
        logger.debug("Using %s custom list", args.file)
        with open(args.file, "r") as f:
            subreddits = f.readlines()
        subreddits = [x.strip() for x in subreddits]
    logger.debug(subreddits)

    reddit_api = redditconnect(args.praw_user)

    logger.debug("Check Exports Folder")
    directory = "Exports"
    Path(directory).mkdir(parents=True, exist_ok=True)
    list_infos = []

    for subreddit in subreddits:
        infos = extract_data_from_subreddit(reddit_api, subreddit)
        if infos:
            list_infos.append(infos)

    if args.backend == "csv":
        export_list_infos_to_csv(directory, list_infos)
    elif args.backend == "sqlite":
        export_list_infos_to_sqlite(directory, list_infos)

    logger.debug("Runtime : %.2f seconds" % (time.time() - temps_debut))


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
        "-p",
        "--praw_user",
        help="User to use in the praw.ini file (Default : bot_subreddit_tracker).",
        type=str,
        default="bot_subreddit_tracker",
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
