import random
import datetime
import threading
import json
from core.my_random import random_choice as choice

class rp_system():
    def __init__(self):
        self.file_path = 'data/rp.json'
        self.refresh = False
        return

    def random_choice(self, seq, prob, k=1):
        return choice(seq, prob, k)

    def clear_rp(self) -> None:
        self.refresh = False
        json.dump({}, open(self.file_path, 'w', encoding='utf-8'))
        return

    def update_rp(self) -> None:
        self.refresh = True
        now_time = datetime.datetime.now()
        next_time = now_time + datetime.timedelta(days=+1)
        next_year = next_time.date().year
        next_month = next_time.date().month
        next_day = next_time.date().day
        next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+" 00:00:00", "%Y-%m-%d %H:%M:%S")
        timer_start_time = (next_time - now_time).total_seconds()
        timer = threading.Timer(timer_start_time, self.Clear_RP)
        timer.start()
        return

    def get_rp(self, uid) -> int:
        rp_data = json.load(open(self.file_path, 'r', encoding='utf-8'))
        if uid in rp_data:
            return rp_data[uid]
        else:
            value = self.random_choice([random.randint(0,100),114514],[0.95,0.05])[0]
            rp_data[uid] = value
            json.dump(rp_data, open(self.file_path, 'w', encoding='utf-8'))
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

        # if not self.refresh:
        #     self.update_rp()

        return final_msg
