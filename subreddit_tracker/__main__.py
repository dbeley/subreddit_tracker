import argparse
import logging
import time
import locale
import praw
import datetime
import pkg_resources
from pathlib import Path

logger = logging.getLogger()
temps_debut = time.time()


def redditconnect(bot):
    user_agent = "python:bot"

    reddit = praw.Reddit(bot, user_agent=user_agent)
    return reddit


def write_header_file(filename):
    columns = "Name,Date,Subscribers,Live Users\n"
    with open(filename, "w") as f:
        f.write(columns)


def main():
    args = parse_args()
    locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")
    auj = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    reddit = redditconnect("bot")

    logger.debug("Subreddit list parsing")
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

    logger.debug("Check Exports Folder")
    directory = "Exports"
    Path(directory).mkdir(parents=True, exist_ok=True)

    global_filename = f"{directory}/subreddits_subscribers_count.csv"
    if not Path(global_filename).is_file():
        write_header_file(global_filename)

    for subreddit in subreddits:
        logger.debug("Extracting infos for subreddit %s", subreddit)
        subscribers_count = reddit.subreddit(subreddit).subscribers
        live_users = reddit.subreddit(subreddit).accounts_active

        logger.debug(
            "/r/%s : %s subscribers, %s live users",
            subreddit,
            subscribers_count,
            live_users,
        )
        # Global export file
        with open(global_filename, "a+") as f:
            f.write(f"{subreddit},{auj},{subscribers_count},{live_users}\n")
        # Distinct export files
        if args.distinct_file:
            filename = f"{directory}/{subreddit}_subscribers_count.csv"
            if not Path(filename).is_file():
                write_header_file(filename)

            with open(filename, "a+") as f:
                f.write(
                    f"{subreddit},{auj},{subscribers_count},{live_users}\n"
                )

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
        help="File containing the subreddits (default : sample file containing popular subreddits)",
        type=str,
    )
    parser.add_argument(
        "-d",
        "--distinct_file",
        help="Create discting file for each subreddits (in addition to the global file).",
        dest="distinct_file",
        action="store_true",
    )
    parser.set_defaults(distinct_file=False)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == "__main__":
    main()
