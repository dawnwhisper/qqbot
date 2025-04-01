from .facade import bot_facade
from botpy.ext.cog_yaml import read
import os

config = read(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml"))
bot = bot_facade(config)

def process_request(data):
    return bot.handle_message(data)