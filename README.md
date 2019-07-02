# subreddit_tracker

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5fbad580efe24b898e80ec7cd64345c9)](https://app.codacy.com/app/dbeley/subreddit_tracker?utm_source=github.com&utm_medium=referral&utm_content=dbeley/subreddit_tracker&utm_campaign=Badge_Grade_Dashboard)

Extract subscribers and live users count of a list of subreddit defined in a csv file or a sqlite database.

## Requirements

- praw
- working praw config in ~/.config/ (see praw.ini_sample for an example)

## Installation in a virtualenv (recommended)

```
pipenv install '-e .'
```

## Usage

Given a simple txt file subreddit_list.txt

```
funny
gifs
videos
```

You can then call

```
subreddit_tracker -f subreddit_list.txt
```

## Autostarting

A systemd service and its timer are provided in the systemd-service/ folder. You can tweak the service file to launch the script in another directory or to launch the script with other options.

The timer is set to launch the script every hour.

Then copy the service and the timer files in ~/.config/systemd/user/

You can launch the timer with

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
usage: subreddit_tracker [-h] [--debug] [-f FILE] [-b BACKEND]

Extract subscribers and live users count of a list of subreddit defined in a
text file.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  -f FILE, --file FILE  File containing the subreddits (default : sample file
                        containing popular subreddits)
  -b BACKEND, --backend BACKEND
                        Backend to store the extracted data (sqlite or csv,
                        Default=csv).
```
