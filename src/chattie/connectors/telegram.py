"""A connector for the Telegram bot API.

This connector only requires the TELEGRAM_API_TOKEN environment
variable is set. You can acquire a token and instructions for making
your bot join rooms from here: https://core.telegram.org/bots
"""

import os

try:
    from .telegram.ext import Updater
    from .telegram.ext import MessageHandler
except ImportError:
    import sys
    print('You need to pip3 install python-telegram-bot before '
          'using this connector!')
    sys.exit(1)



class Connector:
    """Connector class for the Telegram bot API."""

    # Holds the bots for all given rooms
    bots = {}

    def __init__(self, parser):
        """Will load the api token from $TELEGRAM_API_TOKEN."""
        token = os.getenv('TELEGRAM_API_TOKEN')
        if token is None:
            raise Exception('TELEGRAM_API_TOKEN not set')
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.parser = parser
        self.dispatcher.add_handler(MessageHandler(None, self.parse_incoming))

    def listen(self):
        """Listen for messages."""
        self.updater.start_polling()
        self.updater.idle()

    def send_message(self, room_id, msg):
        """Send a message to the given room_id."""
        self.bots[str(room_id)].sendMessage(chat_id=room_id, text=msg)

    def parse_incoming(self, bot, incoming):
        """Transform incoming telegram info into format Chattie can parse."""
        self.bots[str(incoming.message.chat_id)] = bot
        self.parser(incoming.message.chat_id, incoming.message.text)
