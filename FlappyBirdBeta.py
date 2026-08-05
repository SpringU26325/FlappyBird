

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
        # self.y = 0  # TEST
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

# 循环计数器
class CallCounter:
    def __init__(self):
        self.count = 0

    def execute(self):
        self.count += 1
        self.count = self.count % WIDTH0


counter = CallCounter()

# 游戏
def play():
    game_flag = True
    pipes = [Pipe((WIDTH0 * k) - 2, random.randint(HEIGHT // 5, HEIGHT - HEIGHT // 5)) for k in range(4)]
    while game_flag:
        # 参数计算


        # 管道参数
        if counter.count == 0:
            pipes.pop(0)
        elif counter.count == WIDTH0 - 2:
            pipes.append(Pipe(WIDTH, random.randint(HEIGHT // 5, HEIGHT - HEIGHT // 5)))

        # 画面
        information = [f'当前得分{bird1.score}', '按esc退出','按P暂停']
        separator = '---'
        separate_line = '-' * WIDTH
        information_line = separator
        for i in range(len(information)):
            information_line = information_line + information[i] + separator
        def frame_rendering():
            nonlocal pipes,game_flag
            # 参数生成
            frames = [[AIR for i in range(WIDTH)] for j in range(HEIGHT)]# 生成画面
            # 画管道
            for j in range(len(frames)):
                for i in range(len(frames[j])):
                    for k in range(len(pipes)):
                        if i == pipes[k].x or i == pipes[k].x - 1 or i == pipes[k].x + 1:
                            if not ((j == pipes[k].y) or (j == pipes[k].y - 1)  or (j == pipes[k].y + 1)):
                                frames[j][i] = PIPE_IMAGE
            frames[bird1.y][bird1.x] = bird1.image# 画小鸟
            # 计算下一次参数
            counter.execute()  # 计时参数+1
            for i in range(len(pipes)):
                pipes[i].x -= 1
            if bird1.y == HEIGHT - 1:
                 game_flag = False
            if counter.count %4 == 3:
                bird1.fall()


            # 打印画面
            frame = separate_line + '\n' + information_line + '\n'
            for j in range(len(frames)):
                temp_line = ''
                for i in range(len(frames[j])):
                    temp_line = temp_line + frames[j][i]# 拼接好一行
                frame = frame + temp_line + '\n'  # 拼接画面
            frame = frame + separate_line
            print(frame)

        frame_rendering()

if __name__ == '__main__':
    play()