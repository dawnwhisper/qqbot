from core.rp import rp_system
from core.food import food_system
from .util import CommandHandler

class bot_facade:
    def __init__(self):
        self.rp = rp_system()
        self.food = food_system()
        self.cmd_handler = CommandHandler()
        
        self.register_handlers()
    
    def register_handlers(self):
        handlers = {
            "rp": self.handle_rp,
            "food": self.handle_food
        }
        for name, handler in handlers.items():
            self.cmd_handler.register_handler(name, handler)
        
    def handle_rp(self, *args):
        return self.rp.get_rp_final(self.current_user_id)

    def handle_food(self, *args):
        return self.food.get_random_food()

    def handle_message(self, message: dict):
        content = message.content.strip()
        self.current_user_id = message.author.member_openid
        
        handler, args = self.cmd_handler.parse_command(content)
        if handler:
            return handler(*args)
        
        return "未知指令"
