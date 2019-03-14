# reddit_subscribers_count

Extract subscribers count 

## Pre-requisites

- praw config in ~/.config/

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

Then copy the service and the timer files in ~/.config/systemd/user/

You can launch the timer with

```
systemctl --user daemon-reload
systemctl --user enable --now reddit_subscribers_count.timer
```
