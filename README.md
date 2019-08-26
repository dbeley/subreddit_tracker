# subreddit_tracker

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5fbad580efe24b898e80ec7cd64345c9)](https://app.codacy.com/app/dbeley/subreddit_tracker?utm_source=github.com&utm_medium=referral&utm_content=dbeley/subreddit_tracker&utm_campaign=Badge_Grade_Dashboard)

Extract subscribers and live users count of a list of subreddit defined in a csv file or a sqlite database.

## Requirements

- praw
- working praw config in ~/.config/ (see praw.ini_sample for an example)

## Installation

Installation in a virtualenv with pipenv (recommended) :

```
pipenv install '-e .'
```

Installation in the system-wide environment :

```
python setup.py install
```

Installation in the systemd-wide environment with pip :

```
pip install .
```

## Usage

Given a simple txt file subreddit_list.txt

```
funny
gifs
videos
```

You can then call (depending on the backend you want) :

```
subreddit_tracker -f subreddit_list.txt -b csv
subreddit_tracker -f subreddit_list.txt -b sqlite
```

## Autostarting

Systemd services and their respective timers are provided in the systemd-service/ folder.

You will have to change the service files to launch the script in another directory or to launch it with other options (by default the service files launch the script in a pipenv virtualenv located in the same directory as the script).

The timer is set to launch the script every 10 minutes.

After copying the service and timer files in ~/.config/systemd/user/, you can launch the timer with :

```
systemctl --user daemon-reload
systemctl --user enable --now subreddit_tracker.timer
systemctl --user enable --now subreddit_tracker_sqlite.timer
```

## Help

```
subreddit_tracker -h
```

```
usage: subreddit_tracker [-h] [--debug] [-f FILE] [-n NB_THREADS] [-b BACKEND]

Extract subscribers and live users count of a list of subreddit defined in a
text file.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  -f FILE, --file FILE  File containing the subreddits (Default : sample file
                        containing popular subreddits)
  -n NB_THREADS, --nb_threads NB_THREADS
                        Number of threads to use. Be sure to have
                        corresponding entries in your praw.ini file
                        (reddit_bot_1... reddit_bot_N).
  -b BACKEND, --backend BACKEND
                        Backend to store the extracted data (sqlite or csv,
                        Default : csv).
```

## Threads

You can use several threads with the -n/--nb_threads argument. Be sure to have corresponding entries in your praw.ini file with different accounts under \[reddit_bot_2], \[reddit_bot_3], ... headings.

The subreddit list will be divided into N sublists. Each of those will be extracted with a separate reddit account to make things faster.
