import discord
from discord.ext import commands
import asyncio
import logging
import sys

from cyberiadai.defines import CRoleType
from cyberiadai.pluginloader import CybCommandLoader

commandsRegistry = None

def init_registries():
    global commandsRegistry
    if commandsRegistry is None:
        commandsRegistry = CybCommandLoader(recurse=True).load("cyberiadai.commands")

def add_commands(bot):
    init_registries()
    
    count = 0
    bot.log.info("Adding commands!")
    for cmd in commandsRegistry:
        count += 1
        bot.log.debug("Adding command {0}".format(cmd.name))
        bot.add_command(cmd)
    bot.log.info("Added {} commands".format(count))
    bot.log.debug("Loaded commands: {}".format([x.name for x in bot.commands]))

class CyberiadAIBot(commands.Bot):
    def __init__(self, config):
        super().__init__(command_prefix=config['DEFAULT']['cmdprefix'])
        self._log = logging.getLogger('cyberiadAI')
        self._authkey = config['DEFAULT']['botkey']
        
    def run(self):
        add_commands(self)
        super().run(self._authkey)
    
    @property
    def log(self):
        """The bot's logging object"""
        return self._log
