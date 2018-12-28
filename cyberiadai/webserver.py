"""
Handles incoming messages sent from the server
"""

import asyncio
import ast
import logging
import pickle

from cyberiadai.context import botinstance

async def handle_incoming_byond(reader, writer):
    logger = logging.getLogger(__name__)
    data = await reader.read(-1)
    # hmm this seems un-good, especially since this comes before the password auth
    # manually parsing a pickle is inane
    # I'd like to replace the irc botcommand script before putting this live
    # using something compatible with ast.eval_literal
    message = pickle.loads(data)
    data = message['data']
    bot = botinstance.get()
    if data[0] != bot._byondmsgpassword:
        bot.log.warning("Bad password: {} (Remaining data: {})".format(data[0], data[1:]))
        bot.log.warning("Offending IP: {}".format(writer.transport.get_extra_info('socket').getpeername()))
        return
    data.pop(0) # remove the password
    bot.queue_message(' '.join(data), message['ip'])
