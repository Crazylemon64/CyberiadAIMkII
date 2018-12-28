import pkgutil
# allow cascading imports for everything in the "cyberiadai.commands" path
# so you can have separate packages for different batches of commands
__path__ = pkgutil.extend_path(__path__, __name__)
