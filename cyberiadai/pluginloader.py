from straight.plugin import loaders
from discord.ext import commands

class CybCommandLoader(loaders.ObjectLoader):
    def __init__(self, *args, **kwargs):
        super(CybCommandLoader, self).__init__(*args, **kwargs)

    def _matchesFilter(self, module, attr_name):
        return super(CybCommandLoader, self)._matchesFilter(module, attr_name) and isinstance(getattr(module, attr_name), commands.core.Command)
