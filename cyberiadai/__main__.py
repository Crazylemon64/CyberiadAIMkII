# monkeypatches and other things that must go in the prelude
from cyberiadai.hacks import monkeypatches

import discord
import asyncio
import xdg

import os
import logging
import configparser
import signal
import platform
from collections import OrderedDict

from .bot import CyberiadAIBot
from .context import botinstance

APP_DIRNAME = 'cyberiadai'

def loadconfig():
    # might as well be nice to windows users
    if 'APPDATA' in os.environ:
        APP_CONFIG_PATH = os.path.join(os.environ['APPDATA'], APP_DIRNAME)
    else:
        APP_CONFIG_PATH = os.path.join(xdg.XDG_CONFIG_HOME, APP_DIRNAME)
    
    if not os.path.exists(APP_CONFIG_PATH):
        try:
            os.makedirs(APP_CONFIG_PATH)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    
    config = configparser.ConfigParser()
    cfilepath = os.path.join(APP_CONFIG_PATH, "config.ini")
        
    config['DEFAULT'] = OrderedDict([
            ('botkey', 'UNDEFINED'),
            ('cmdprefix', '👀'),
            ('byondmsgport', 45678),
            ('byondmsgpassword', 'UNDEFINED'),
            ('byondmsghost', 'localhost'),
            ('byondtimeout', '10'),
            ('admin_channels', '000000000000000000,'),
            ('admin_github_channels', '000000000000000000,'),
            ('admin_ahelp_channels', '000000000000000000,'),
            ('public_channels', '000000000000000000'),
            ('public_github_channels', '000000000000000000,'),
            ])
    try:
        with open(cfilepath, "r") as cf:
            config.read_file(cf)
    except FileNotFoundError:
        with open(cfilepath, 'w') as cf:
            config.write(cf)
    
    return CyberiadAIBot(config)


def main():
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING"))
    logging.getLogger('cyberiadai').setLevel(logging.DEBUG)
    
    bot = loadconfig()
    bot.log.setLevel(logging.DEBUG)
    botinstance.set(bot)
    
    signals = [signal.SIGHUP, signal.SIGTERM, signal.SIGINT]
    if platform.system() == 'Windows':
        signals.append([signal.CTRL_C_EVENT, signal.CTRL_BREAK_EVENT])
    # add some kind of signals handler here
    
    bot.run()
