import os
import argparse
import logging
import time
import locale
import praw
import datetime
import pkg_resources


logger = logging.getLogger()
temps_debut = time.time()


def redditconnect(bot):
    user_agent = "python:bot"

    reddit = praw.Reddit(bot, user_agent=user_agent)
    return reddit


def main():
    args = parse_args()
    file = args.file
    locale.setlocale(locale.LC_TIME, "fr_FR.utf-8")
    auj = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    reddit = redditconnect("bot")

    if file is None:
        file = pkg_resources.resource_string(__name__, "subreddit_list.txt")
        subreddits = file.decode("utf-8").split('\n')
        subreddits = subreddits[:-1]
    else:
        with open(file, 'r') as f:
            subreddits = f.readlines()
        subreddits = [x.strip() for x in subreddits]
    logger.debug(subreddits)

    logger.debug("Check Exports Folder")
    directory = "Exports"
    if not os.path.exists(directory):
        logger.debug("Creating Exports Folder")
        os.makedirs(directory)

    for subreddit in subreddits:
        subscribers_count = reddit.subreddit(subreddit).subscribers
        print(f"/r/{subreddit} : {subscribers_count} subscribers")
        with open(f"{directory}/subreddits_subscribers_count.csv", 'a+') as f:
            f.write(f"{subreddit},{auj},{subscribers_count}\n")

    logger.debug("Runtime : %.2f seconds" % (time.time() - temps_debut))


def parse_args():
    parser = argparse.ArgumentParser(description="Script extracting the subscribers count of several subreddits"))
    parser.add_argument('--debug', help="Display debugging information", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('-f', '--file', help="File containing the subreddits (default : sample file containing popular subreddits)", type=str)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    return args


if __name__ == '__main__':
    main()
