# KBFriend

Slack integration with kanboard
https://kanboard.org/

## Getting Started

This project use the slack and kanboard api to get a cli of kanboard on slack.

### Prerequisites

In the file requirements.txt 

To install manually the requirements:

```
$ apt-get install python3 python3-pip
```


```
$pip3 install slackclient
```

```
$pip3 install kanboard
```

## Running

To run this project just run `kbfriend.py` with python3

```
$python3 kbfriend.py
```

### Test

On slack, invite the created app to a channel and send a message, for example:

```
kb help
```
