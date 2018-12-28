# monkeypatches and other things that must go in the prelude
from cyberiadai.hacks import monkeypatches

import discord
import asyncio
import xdg

import os
import logging
import configparser

from .bot import CyberiadAIBot

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
        
    config['DEFAULT'] = {
            'botkey': 'UNDEFINED',
            'cmdprefix': '👀',
            }
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
    logging.getLogger('straight.plugin').setLevel(logging.DEBUG)
    
    bot = loadconfig()
    bot.log.setLevel(logging.DEBUG)
    
    @bot.event
    async def on_ready():
        bot.log.info('Logged in as {0.user}'.format(bot))
        
#   @bot.event
#   async def on_message(message):
#       if message.content.startswith('!test'):
#           counter = 0
#           tmp = await message.channel.send('Calculating messages...')
#           async for log in message.channel.history(limit=100):
#               if log.author == message.author:
#                   counter += 1
#                   
#           await tmp.edit(content='You have {} messages.'.format(counter))
#       elif message.content.startswith('!sleep'):
#           await asyncio.sleep(5)
#           await message.channel.send('Done sleeping')
    
    bot.run()
