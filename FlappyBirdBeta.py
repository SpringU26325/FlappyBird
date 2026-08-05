

# 测试函数
def test(*args,**kwargs):
    print(args, kwargs,'test')

# 导入模块
import time
import msvcrt
import random
import math
import datetime
import os
import gc

# 常量
WIDTH = 96
WIDTH0 = WIDTH//3
HEIGHT = 15
AIR = ' '#正式
# AIR = 'H'#测试
PIPE_IMAGE = '#'

# 鸟
class Bird:
    def __init__(self):
        self.image = '@'
        self.y = HEIGHT // 2
        self.score = 0
        self.x = 1
    def fall(self):
        self.y += 1

bird1 = Bird()

# 水管
class Pipe:
    def __init__(self, x, y):#central_air
        self.image = '#'
        self.x = x
        self.y = y


# 画面
def frame_rendering():
    # 参数生成
    pipes = [Pipe((WIDTH0 * (k + 1)) - 2, random.randint(HEIGHT // 5, HEIGHT - HEIGHT // 5)) for k in range(3)]
    frames = [[AIR for i in range(WIDTH)] for j in range(HEIGHT)]# 生成画面
    for j in range(len(frames)):
        for i in range(len(frames[j])):
            for k in range(len(pipes)):
                if i == pipes[k].x or i == pipes[k].x - 1 or i == pipes[k].x + 1:
                    if not ((j == pipes[k].y) or (j == pipes[k].y - 1)  or (j == pipes[k].y + 1)):
                        frames[j][i] = PIPE_IMAGE
    frames[bird1.y][bird1.x] = bird1.image# 画小鸟


    # 打印画面
    frame = ''
    for j in range(len(frames)):
        temp_line = ''
        for i in range(len(frames[j])):
            temp_line = temp_line + frames[j][i]# 拼接好一行
        frame = frame + temp_line + '\n'
    print(frame)

frame_rendering()