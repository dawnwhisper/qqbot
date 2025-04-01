import re
import random
from typing import Optional, Tuple

def admin_required(func):
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'is_admin') or not self.is_admin:
            return random.choice(["你不是我的master！","你✅8️⃣谁啊？"])
        return func(self, *args, **kwargs)
    return wrapper

banner = """
[/menu] 召唤此菜单
[/rp] 查看今日人品
[/r <min> <max>] 获取a到b的随机数
[/恰啥] 那我问你 今天吃啥
[/都有啥吃的] 查看所有食物
[/(零食/早餐/午餐/晚餐/夜宵)想吃xxx] 添加食物 (admin)
[/(零食/早餐/午餐/晚餐/夜宵)不想吃xxx] 删除食物 (admin)
[/prprpr] 舔狗日记
"""[:-1]

class CommandHandler:
    def __init__(self, admins=None):
        self.admins = admins or []
        self.dynamic_handlers = {}
        self.commands = {
            r"^/menu$": self.handle_menu,
            r"^/rp$": self.get_handler("rp"),
            r"^/r\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)$": self.handle_random,
            r"^/恰啥$": self.get_handler("food"),
            r"^/都有啥吃的$": self.get_handler("show_food"),
            r"^/(零食|早餐|午餐|晚餐|夜宵)想吃(.+)$": self.get_handler("add_food"),
            r"^/(零食|早餐|午餐|晚餐|夜宵)不想吃(.+)$": self.get_handler("remove_food"),
            r"^/prprpr$": self.get_handler("tiangou"),
        }
    
    def get_handler(self, name):
        def wrapper(*args):
            if name in self.dynamic_handlers:
                return self.dynamic_handlers[name](*args)
            return f"Handler {name} not implemented"
        return wrapper
    
    def register_handler(self, name, handler):
        self.dynamic_handlers[name] = handler
    
    def parse_command(self, content: str) -> Tuple[Optional[callable], list]:
        for pattern, handler in self.commands.items():
            match = re.match(pattern, content.strip())
            if match:
                return handler, list(match.groups())
        return None, []

    def handle_menu(self, *args):
        return banner
        
    def handle_random(self, *args):
        try:
            min_val, max_val = map(float, args)
            
            if min_val.is_integer() and max_val.is_integer():
                result = random.randint(int(min_val), int(max_val))
                return f"随机数: {result}"
            else:
                result = random.uniform(min_val, max_val)
                return f"随机数: {result:.2f}"
        except ValueError:
            return "参数格式错误,使用方法: /r <最小值> <最大值>"
