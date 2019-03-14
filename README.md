# reddit_subscribers_count

Extract subscribers count of a list of subreddit defined in a text file to a csv file

## Pre-requisites

- working praw config in ~/.config/ (see praw.ini_sample for an example)

## Installation

```
sudo python setup.py install
```

## Help

```
reddit_subscribers_count -h
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
reddit_subscribers_count -f subreddit_list.txt
```

## Autostarting

A systemd service and its timer are provided in the systemd-service/ folder. You can tweak the service file to launch the script in another directory or to launch the script with other options.

The timer is set to launch the script every hour.

Then copy the service and the timer files in ~/.config/systemd/user/

You can launch the timer with

```
systemctl --user daemon-reload
systemctl --user enable --now reddit_subscribers_count.timer
```
