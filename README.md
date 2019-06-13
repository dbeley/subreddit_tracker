# subreddit_tracker

Extract subscribers and live users count of a list of subreddit defined in a text file.

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
```

## Help

```
subreddit_tracker -h
```

```
```
