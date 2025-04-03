import random
import datetime
import threading
import json
import os
from core.my_random import random_choice as choice
from botpy import logging

# 获取日志记录器
_log = logging.get_logger()

class rp_system():
    def __init__(self):
        self.file_path = 'data/rp.json'
        self.last_reset_date_file = 'data/rp_last_reset.txt'
        
        # 确保数据文件存在
        os.makedirs('data', exist_ok=True)
        if not os.path.exists(self.file_path):
            self.clear_rp()
        
        # 检查是否需要重置
        self.check_reset_date()
        
        # 设置定时器
        self.schedule_next_reset()
        return

    def random_choice(self, seq, prob, k=1):
        return choice(seq, prob, k)

    def clear_rp(self) -> None:
        self.refresh = False
        json.dump({}, open(self.file_path, 'w', encoding='utf-8'))
        # 保存重置日期
        with open(self.last_reset_date_file, 'w') as f:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d"))
        return

    def check_reset_date(self) -> None:
        """检查是否需要重置 RP 数据"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # 如果上次重置日期文件不存在或日期不是今天，则重置
        if not os.path.exists(self.last_reset_date_file):
            self.clear_rp()
            return
            
        with open(self.last_reset_date_file, 'r') as f:
            last_date = f.read().strip()
            
        if last_date != today:
            self.clear_rp()

    def schedule_next_reset(self) -> None:
        """调度下一次重置的时间"""
        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)
        next_reset = datetime.datetime(
            year=tomorrow.year,
            month=tomorrow.month,
            day=tomorrow.day,
            hour=0,
            minute=0,
            second=0
        )
        
        delay = (next_reset - now).total_seconds()
        timer = threading.Timer(delay, self._reset_callback)
        timer.daemon = True  # 设置为守护线程，这样程序退出时线程也会退出
        timer.start()
        
        # 将输出添加到日志中
        _log.info(f"下一次 RP 值重置时间: {next_reset}, 还有 {delay:.1f} 秒")
        self.refresh = True
        return

    def _reset_callback(self) -> None:
        """定时器回调函数"""
        self.clear_rp()
        _log.info("RP 值已重置")
        self.schedule_next_reset()  # 重新调度下一次重置

    def get_rp(self, uid) -> int:
        # 确保已检查过是否需要重置
        if not hasattr(self, 'refresh') or not self.refresh:
            self.check_reset_date()
        
        # 读取 RP 数据
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                rp_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            rp_data = {}
            
        # 如果用户 ID 不存在，生成新的 RP 值
        if uid not in rp_data:
            value = self.random_choice([random.randint(0,100), 114514], [0.95, 0.05])[0]
            rp_data[uid] = value
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(rp_data, f)
                
        return rp_data[uid]
    
    def get_rp_final(self, uid) -> str:
        rp = self.get_rp(uid)
        final_msg = f'今日rp:{rp}'

        if rp == 114514:
            final_msg += '\n好臭的人品啊啊啊啊啊啊！'
        elif rp >= 90:
            banner = ['\n是锦鲤！贴贴！','\nrp风向标找到啦！','\n哇，金色传说！','']
            prob = [0.3,0.3,0.3,0.1]
            final_msg += self.random_choice(banner, prob)[0]
        elif rp >=70 and rp < 90:
            banner = ['\n一般般啦~','\n还不错嘛','']
            porb = [0.4,0.4,0.2]
            final_msg += self.random_choice(banner, porb)[0]
        elif rp >=60 and rp < 70:
            banner = ['\n嘛，还好及格了','\n就这样吧','']
            porb = [0.3,0.3,0.4]
            final_msg += self.random_choice(banner, porb)[0]
        elif rp >=50 and rp < 60:
            banner = ['\n呜呜，差一点就及格了','\n还好吧，马上就及格啦','']
            porb = [0.3,0.3,0.4]
            final_msg += self.random_choice(banner, porb)[0]
        elif rp >30 and rp < 50:
            banner = ['\n今天rp有点低，要小心哇','\n啊这','']
            porb = [0.4,0.4,0.2]
            final_msg += self.random_choice(banner, porb)[0]
        elif rp <= 30:
            banner = ['\n有霉B，但我不说是谁','\n啧啧，这也太惨了','\n0.0','']
            porb = [0.3,0.3,0.3,0.1]
            final_msg += self.random_choice(banner, porb)[0]

        if not self.refresh:
            self.update_rp()

        return final_msg
