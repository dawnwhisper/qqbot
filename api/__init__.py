from .facade import bot_facade

bot = bot_facade()

def process_request(data: dict):
    return bot.handle_message(data)