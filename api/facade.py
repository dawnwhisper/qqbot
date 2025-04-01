from core.rp import rp_system
from core.food import food_system
from core.tiangou import tiangou_comment
from .util import CommandHandler, admin_required

class bot_facade:
    def __init__(self, config=None):
        self.rp = rp_system()
        self.food = food_system()
        self.admins = config.get("admins", []) if config else []
        self.config = config or {}
        self.cmd_handler = CommandHandler(self.admins)
        
        self.register_handlers()
    
    def register_handlers(self):
        handlers = {
            "rp": self.handle_rp,
            "food": self.handle_food,
            "show_food": self.handle_show_food,
            "add_food": self.handle_add_food,
            "remove_food": self.handle_remove_food,
            "tiangou": self.handle_tiangou,
        }
        for name, handler in handlers.items():
            self.cmd_handler.register_handler(name, handler)
        
    def handle_rp(self, *args):
        return self.rp.get_rp_final(self.current_user_id)

    def handle_food(self, *args):
        return self.food.get_random_food()
    
    def handle_show_food(self, *args):
        return self.food.show_all_food()

    @admin_required
    def handle_add_food(self, time_type, food_name):
        return self.food.add_food(time_type + food_name)
        
    @admin_required
    def handle_remove_food(self, time_type, food_name):
        return self.food.remove_food(time_type + food_name)

    def handle_message(self, message: dict):
        content = message.content.strip()
        self.current_user_id = message.author.member_openid
        self.is_admin = self.current_user_id in self.admins
        
        handler, args = self.cmd_handler.parse_command(content)
        if handler:
            return handler(*args)
        
        return "未知指令"
    
    def handle_tiangou(self, *args):
        return tiangou_comment()