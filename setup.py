from setuptools import setup, find_packages

NAME = "cyberiad_ai_mkii"
DESCRIPTION = "A discord bot to manage the operations of paradise station"
AUTHOR = "Marlyn"
REQUIRES_PYTHON = '>=3.7.0'
VERSION = None

print("discord.py doesn't work on 3.7+ unless you use the dev version, but it's not published there. However, pip doesn't support installing from external repositories inline. You will need to install the updated version of discord.py by hand until one party reconciles this.")
print("pip install https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py[voice]")

REQUIRED = [
        "xdg",
        "straight.plugin",
        ]
#REQUIRED = [
        # Using this branch bc older ones don't work with 3.7
#        "discord.py@https://github.com/Rapptz/discord.py/archive/async.zip#egg=discord.py[voice]",
#        ]

setup(
        name = NAME,
        version = VERSION,
        author = AUTHOR,
        description = DESCRIPTION,
        packages = find_packages(exclude=['docs', 'tests']),
        install_requires = REQUIRED,
        license='MIT',
        entry_points = {
            'console_scripts': ['cyberiad_ai = cyberiadai.__main__:main'],
            },
)
