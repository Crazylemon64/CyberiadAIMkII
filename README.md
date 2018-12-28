# Cyberiad AI MKII

A discord bot to manage day-to-day operations of Paradise Station.

## Dependencies

Python 3.7+
pip

## Installation

```py
pip install https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py[voice]

python setup.py install
```

## Running

First, generate the base config file by running the bot with
```
cyberiad_ai
```

Then, generate/insert your discord bot key in the configuration file, and set passwords as appropriate.

## Configuration

To get the channel IDs, use the `dumpserverinfo` command, which will list information of channel IDs and topics for all connected servers in the bot's console. (This command is owner-only)
Channel lists are comma-separated lists of numbers.
