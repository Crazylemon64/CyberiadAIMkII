from straight.plugin import loaders
from discord.ext import commands

class DiscordCommandLoader(loaders.ObjectLoader):
    """Loads all discord commands in the given namespace"""
    def __init__(self, *args, **kwargs):
        super(DiscordCommandLoader, self).__init__(*args, **kwargs)

    def _matchesFilter(self, module, attr_name):
        return super(DiscordCommandLoader, self)._matchesFilter(module, attr_name) and isinstance(getattr(module, attr_name), commands.core.Command)
