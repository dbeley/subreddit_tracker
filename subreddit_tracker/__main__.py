import argparse
import logging
import time
import locale
import pkg_resources
import datetime
from pathlib import Path
from .thread import SubredditTrackerThread

logger = logging.getLogger()
logging.getLogger("prawcore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

DEBUT_TIME = time.time()
SUPPORTED_BACKENDS = ["csv", "sqlite"]
EXPORT_DIRECTORY = "Exports"
DATE = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))


def main():
    args = parse_args()
    locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")

    if args.backend not in SUPPORTED_BACKENDS:
        logger.error("%s not a supported backend. Exiting.", args.backend)
        exit()
    if args.file is None:
        logger.debug("Using default subreddits_list.txt.")
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

    # Cut the list of subreddits into nb_threads parts.
    subreddits_list = list(chunker_list(subreddits, args.nb_threads))

    # Create and start threads.
    threads = []
    for index, subreddits_part in enumerate(subreddits_list, 1):
        reddit_account = f"reddit_bot_{index}"
        t = SubredditTrackerThread(
            reddit_account,
            subreddits_part,
            DATE,
            args.backend,
            EXPORT_DIRECTORY,
        )
        t.start()
        threads.append(t)

    # Join all threads.
    for t in threads:
        t.join()

    logger.info(
        "Subreddit_tracker runtime : %.2f seconds" % (time.time() - DEBUT_TIME)
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
