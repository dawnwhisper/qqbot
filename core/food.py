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
        self.food = json.load(open(self.file_path, 'r', encoding='utf-8'))
        return
    
    def save_data(self):
        json.dump(self.food, open(self.file_path, 'w', encoding='utf-8'))
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
        message = ""
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
        time, food = self.get_time_segmentation_inv(data[:2]), data[2:]
        if time == None:
            return 'ERROR'
        all_food = self.load_data()
        if (food, time) in all_food:
            return '这个食物已经添加过了哦~'
        all_food[time].append(food)
        return f'新的{data}已添加！'
    
    def remove_food(self, data):
        time, food = self.get_time_segmentation_inv(data[:2]), data[2:]
        if time == None:
            return 'ERROR'
        all_food = self.load_data()
        if (food, time) not in all_food:
            return '好像本来就没有？'
        all_food[time].remove(food)
        return f'{data}已经去掉啦~'