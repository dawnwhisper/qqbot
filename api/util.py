import re
import random
from typing import Optional, Tuple

banner = """
[/menu] 召唤此菜单
[/rp] 查看今日人品
[/r <min> <max>] 获取a到b的随机数
[/恰啥] 那我问你 今天吃啥
"""

class CommandHandler:
    def __init__(self):
        self.dynamic_handlers = {}
        self.commands = {
            r"^/menu$": self.handle_menu,
            r"^/rp$": self.get_handler("rp"),
            r"^/r\s+(\d+)\s+(\d+)$": self.handle_random,
            r"^/恰啥$": self.get_handler("food"),  # 修改这里，使用动态处理器
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
    
    def handle_rp(self, *args):
        return "Function rewrite failed"

    def handle_food(self, *args):
        return "Function rewrite failed"
        
    def handle_random(self, *args):
        try:
            min_val, max_val = map(int, args)
            return f"随机数: {random.randint(min_val, max_val)}"
        except ValueError:
            return "参数格式错误,使用方法: /r <最小值> <最大值>"
