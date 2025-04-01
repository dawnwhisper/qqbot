from .my_random import random_choice
from datetime import datetime
from functools import reduce
import random
import json

class food_system():
    def __init__(self) -> None:
        self.file_path = 'data/food.json'
        self.food = {}
        self.load_data()
        return
    
    def load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.food = json.load(f)
        return
    
    def save_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.food, f, ensure_ascii=False, indent=4)
        return

    def get_hour_time(self):
        hour = datetime.now().hour
        if(6 <= hour and hour <= 9):
            return '早餐'
        elif(11 <= hour and hour <= 14):
            return '午餐'
        elif(17 <= hour and hour <= 19):
            return '晚餐'
        elif(22 <= hour or hour <= 3):
            return '夜宵'
        return '零食'
    
    def get_food_menu(self, time):
        return self.food[time] if time else self.food['零食']
    
    def get_time_segmentation(self, time):
        message = ['零食','早餐','午餐','晚餐','夜宵']
        return message[time]

    def get_time_segmentation_inv(self, string):
        message = ['零食','早餐','午餐','晚餐','夜宵']
        if string not in message:
            return None
        return message.index(string)
        
    def show_all_food(self):
        message = "\n"
        for time in self.food.keys():
            message += str(time) + ':\n'
            for food in self.food[time]:
                message += food + '，'
            message = message[:-1] + '\n'
        return message

    def get_random_food(self):
        time = self.get_hour_time()
        time = random_choice([time, '零食'], [0.8, 0.2])[0]
        food = random.choice(self.get_food_menu(time))
        if time != self.get_hour_time():
            message = '别恰'+ self.get_hour_time() + '了，恰' + food
        else:
            message = time + '恰' + food
        return message

    def add_food(self, data):
        time_str = data[:2]
        food_name = data[2:]
        time = self.get_time_segmentation_inv(time_str)
        
        if time is None:
            return f'时间段"{time_str}"无效，请使用：零食/早餐/午餐/晚餐/夜宵'
            
        time_key = self.get_time_segmentation(time)
        
        if food_name in self.food[time_key]:
            return f'{time_key}"{food_name}"已经存在啦~'
            
        self.food[time_key].append(food_name)
        self.save_data()
        return f'新的{time_key}"{food_name}"已添加！'
    
    def remove_food(self, data):
        time_str = data[:2]
        food_name = data[2:]
        time = self.get_time_segmentation_inv(time_str)
        
        if time is None:
            return f'时间段"{time_str}"无效，请使用：零食/早餐/午餐/晚餐/夜宵'
            
        time_key = self.get_time_segmentation(time)
        
        if food_name not in self.food[time_key]:
            return f'{time_key}"{food_name}"不在列表中，无法删除'
            
        self.food[time_key].remove(food_name)
        self.save_data()
        return f'{time_key}"{food_name}"已成功删除~'