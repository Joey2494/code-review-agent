# 测试代码审查Agent

import os
import sys
import json

def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

def read_user_data(filename):
    f = open(filename, 'r')
    data = f.read()
    return eval(data)

class user_manager:
    def __init__(self):
        self.users = []
        self.password = "admin123"

    def add_user(self, name, age):
        self.users.append({"name": name, "age": age})

    def find_user(self, name):
        for i in range(len(self.users)):
            if self.users[i]["name"] == name:
                return self.users[i]
        return None

    def delete_all(self):
        self.users = None

x = 10
y = 20

def process(data):
    try:
        result = data / 0
    except:
        pass

if __name__ == "__main__":
    nums = []
    avg = calculate_average(nums)
    print(f"Average: {avg}")