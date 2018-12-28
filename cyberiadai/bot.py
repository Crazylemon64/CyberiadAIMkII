import discord
from discord.ext import commands
import asyncio
import logging
import sys
import traceback
import enum

from cyberiadai.defines import CRoleType
from cyberiadai.pluginloader import DiscordCommandLoader
from cyberiadai.context import botinstance
from cyberiadai.webserver import handle_incoming_byond

commandsRegistry = None

class BroadcastCategory(enum.Enum):
    GENERAL = enum.auto()
    AHELP = enum.auto()
    GITHUB_PUBLIC = enum.auto()
    ADMIN = enum.auto()
    SQUELCH = enum.auto()

def init_registries():
    global commandsRegistry
    if commandsRegistry is None:
        commandsRegistry = DiscordCommandLoader(recurse=True).load("cyberiadai.commands")

class CyberiadAIBot(commands.Bot):
    def __init__(self, config):
        def parse_channel_list(chanlist_str):
            return [int(x) for x in chanlist_str.split(',') if x]

        super().__init__(command_prefix=config['DEFAULT']['cmdprefix'])
        self._log = logging.getLogger('cyberiadAI')
        self._authkey = config['DEFAULT']['botkey']
        self._byondmsgpassword = config['DEFAULT']['byondmsgpassword']
        self._serverCoro = asyncio.start_server(
                handle_incoming_byond, 
                config['DEFAULT']['byondmsghost'], 
                config['DEFAULT']['byondmsgport'], loop=self.loop)
        self._queue = asyncio.Queue(loop=self.loop)
        # Set the private attributes for the various channels lists
        channel_lists = ["admin",
                "admin_github",
                "admin_ahelp",
                "public",
                "public_github",]
        for k in channel_lists:
            setattr(self, '_{}_channels'.format(k), 
                    parse_channel_list(config['DEFAULT']['{}_channels'.format(k)]))
        
    def run(self):
        self._add_commands()
        self.loop.run_until_complete(self._serverCoro)
        self.loop.create_task(self.handle_queue())
        super().run(self._authkey)
        
    def queue_message(self, message, target):
        self.loop.create_task(self._queue.put((message, target)))
    
    @staticmethod    
    def getBroadcastCategory(target):
        # These values are taken from the default paradise config files
        if target == "#admin":
            return BroadcastCategory.AHELP
        elif target == "#main":
            return BroadcastCategory.GENERAL
        elif target == "#paradiseStaff":
            return BroadcastCategory.ADMIN
        elif target == "#cidrandomizer":
            return BroadcastCategory.ADMIN
        # An invalid ID by default so that information doesn't leak where it shouldn't
        return BroadcastCategory.SQUELCH
        
    async def send_message_to_channels_in_list(self, message, chanlist):
        for chan_id in chanlist:
            chan = self.get_channel(chan_id)
            if not chan:
                self.log.warn("Bad channel ID: {}".format(chan_id))
                continue
            await chan.send(message)
        
    async def handle_queue(self):
        queuedMsg, queuedTgt = await self._queue.get()
        # I get bad feelings from this
        # This function should probably be a loop instead?
        self.loop.create_task(self.handle_queue())
        cat = self.getBroadcastCategory(queuedTgt)
        channel_list = []
        if cat == BroadcastCategory.ADMIN:
            channel_list = self._admin_channels
        elif cat == BroadcastCategory.AHELP:
            channel_list = self._admin_ahelp_channels
        elif cat == BroadcastCategory.GENERAL:
            channel_list = self._admin_channels + self._public__channels
        elif cat == BroadcastCategory.SQUELCH:
            self.log.error("Invalid target channel: {}".format(queuedTgt))
            return
        await self.send_message_to_channels_in_list(queuedMsg, channel_list)
    
    @property
    def log(self):
        """The bot's logging object"""
        return self._log
    
    def _add_commands(self):
        init_registries()
        
        count = 0
        self.log.info("Adding commands!")
        for cmd in commandsRegistry:
            count += 1
            self.log.debug("Adding command {0}".format(cmd.name))
            self.add_command(cmd)
        self.log.info("Added {} commands".format(count))
        self.log.debug("Loaded commands: {}".format([x.name for x in self.commands]))
        
    @asyncio.coroutine
    def on_ready(self):
        self.log.info('Logged in as {0.user}'.format(self))
        
    @asyncio.coroutine
    def on_error(self, event_method, *args, **kwargs):
        self.log.error("Exception in {}!".format(event_method), exc_info=True)
        
    @asyncio.coroutine
    def on_command_error(self, context, exception):
        self.log.debug(f"{repr(exception)}, {repr(context)}")
        if hasattr(context.command, "on_error"):
            return
        if isinstance(exception, commands.errors.CommandNotFound):
            self.log.debug(exception)
        else:
            for l in traceback.format_exception(type(exception), exception, exception.__traceback__):
                self.log.error(l)
