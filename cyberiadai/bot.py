import discord
import asyncio
import logging

class CyberiadAIBot:
    def __init__(self, config):
        self._log = logging.getLogger('cyberiadAI')
        self._authkey = config['DEFAULT']['botkey']
        self._client = discord.Client()
        
    def run(self):
        self._client.run(self._authkey)
        
    @property
    def client(self):
        """The bot's Client object"""
        return self._client
    
    @property
    def log(self):
        """The bot's logging object"""
        return self._log
