import os
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


def write_sample_file(filename):
    columns = "Name,Date,Subscribers,Live Users\n"
    with open(filename, 'w') as f:
        f.write(columns)


def main():
    args = parse_args()
    file = args.file
    locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")
    auj = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    reddit = redditconnect("bot")

    logger.debug("Subreddit list parsing")
    if file is None:
        logger.debug("Using default subreddit_list.txt")
        file = pkg_resources.resource_string(__name__, "subreddit_list.txt")
        subreddits = file.decode("utf-8").split('\n')
        subreddits = subreddits[:-1]
    else:
        logger.debug(f"Using {file} custom list")
        with open(file, 'r') as f:
            subreddits = f.readlines()
        subreddits = [x.strip() for x in subreddits]
    logger.debug(subreddits)

    logger.debug("Check Exports Folder")
    directory = "Exports"
    Path(directory).mkdir(parents=True, exist_ok=True)

    global_filename = f"{directory}/subreddits_subscribers_count.csv"
    if not Path(global_filename).is_file():
        write_sample_file(global_filename)

    for subreddit in subreddits:
        logger.debug(f"Extracting infos for subreddit {subreddit}")
        subscribers_count = reddit.subreddit(subreddit).subscribers
        live_users = reddit.subreddit(subreddit).accounts_active

        filename = f"{directory}/{subreddit}_subscribers_count.csv"
        if not Path(filename).is_file():
            write_sample_file(filename)

        logger.debug(f"/r/{subreddit} : {subscribers_count} subscribers")
        with open(global_filename, 'a+') as f:
            f.write(f"{subreddit},{auj},{subscribers_count},{live_users}\n")
        with open(filename, 'a+') as f:
            f.write(f"{subreddit},{auj},{subscribers_count},{live_users}\n")

    logger.debug("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description="Script extracting the subscribers count of several subreddits")
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-f', '--file', help="File containing the subreddits (default : sample file containing popular subreddits)", type=str)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()
