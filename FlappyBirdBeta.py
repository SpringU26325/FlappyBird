

# 测试函数
def test(*args,**kwargs):
    print(args, kwargs,'test')

# 导入模块
import time
import msvcrt
import random
import sys
import copy
# import math
# import datetime
# import os
# import gc

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
    def rise(self):
        self.y -= 1

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
    pause = False
    game_flag = True
    pipes = [Pipe((WIDTH0 * k) - 2, random.randint(HEIGHT // 5, HEIGHT - HEIGHT // 5)) for k in range(4)]
    while game_flag:
        time.sleep(0.1)

        # 计数器：管道参数和小鸟分数
        if counter.count == 0:
            pipes.pop(0)
        elif counter.count == WIDTH0 - 2:
            pipes.append(Pipe(WIDTH, random.randint(HEIGHT // 5, HEIGHT - HEIGHT // 5)))
        elif counter.count == WIDTH0 - 1:
            bird1.score += 1

        # 画面
        information = [f'当前得分{bird1.score}', '按esc退出','按P暂停']
        separator = '---'
        separate_line = '-' * WIDTH
        information_line = separator
        for i in range(len(information)):
            information_line = information_line + information[i] + separator
        def calculate_frame_parameters():
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
            # 画暂停画面
            pause_frame = copy.deepcopy(frames)
            for j in range(HEIGHT//4, HEIGHT - HEIGHT//4):
                for i in range(WIDTH//4, WIDTH - WIDTH//4):
                    pause_frame[j][i] = 'H'

            for j in range(HEIGHT // 4 + 1, HEIGHT - HEIGHT // 4 - 1):
                for i in range(WIDTH // 4 + 1, WIDTH - WIDTH // 4 - 1):
                    pause_frame[j][i] = AIR
            return frames, pause_frame

        def render_frame(frame_input):
            # 打印画面
            frame = separate_line + '\n' + information_line + '\n'
            for j in range(len(frame_input)):
                temp_line = ''
                for i in range(len(frame_input[j])):
                    temp_line = temp_line + frame_input[j][i]  # 拼接好一行
                frame = frame + temp_line + '\n'  # 拼接画面
            frame = frame + separate_line
            print(frame)

        def calculate_game_parameters():
            # 计算下一次参数
            counter.execute()  # 计时参数+1
            for i in range(len(pipes)):
                pipes[i].x -= 1
            if bird1.y == HEIGHT - 1 or bird1.y == 0:
                game_flag = False
            if counter.count %4 == 3:
                bird1.fall()


        # 按键监听
        if msvcrt.kbhit():
            key = msvcrt.getch()

            # 按P暂停
            if key == b'p' or key == b'P':
                pause = True
                # 创建暂停框

                dot_count = 6
                def calculate_pause_frame(dot_count_input, pause_frame_input):
                    # 将信息提示转换成字符串列表
                    tip_list = []
                    tip_string = '[Q] Continue [C] Switch Account'
                    for string_index in range(len(tip_string)):
                        tip_list.append(tip_string[string_index])

                    # [Q] Continue [C] Switch Account
                    for tip_list_index in range(len(tip_list)):
                        pause_frame_input[HEIGHT//2][WIDTH//2 - len(tip_list) // 2 + tip_list_index] = tip_list[tip_list_index]
                    # OOOOO
                    for dot in range(dot_count_input):
                        pause_frame_input[HEIGHT//2 + 1][WIDTH//2 - dot_count // 2 + dot] = 'O'  # 6


                # 卡入循环
                while 1:
                    pause_frame = calculate_frame_parameters()[1]
                    for dot_num in range(1, dot_count):
                        time.sleep(1)
                        calculate_pause_frame(dot_num, pause_frame)
                        render_frame(pause_frame)
                        if msvcrt.kbhit():
                            key = msvcrt.getch()
                            if key == b'\x1b':
                               sys.exit(0)
                            elif key == b'q' or key == b'Q':
                                return




            # 按空格跳跃
            elif key == b' ':
                bird1.rise()

            # 按ESC结束
            elif key == b'\x1b':
                game_over_frame_temp = ''  # 待打印页面
                game_over_tip = f'GAME OVER !Your score is bird1: {bird1.score}'  # 提示词
                blank_line = ' ' * WIDTH  # 空白行
                game_over_frame = []  # 待打印页面参数
                # 空白页
                for j in range(HEIGHT):
                    game_over_frame.append(blank_line)
                # 分割线
                game_over_frame[0] = separate_line
                game_over_frame[HEIGHT - 1] = separate_line
                # 中间提示
                game_over_frame[HEIGHT // 2] = blank_line[:
                WIDTH // 2 - len(game_over_tip) // 2] + game_over_tip +blank_line[WIDTH // 2 - len(game_over_tip) // 2 + len(game_over_tip):]
                # 打印结束页面
                for game_over_frame_index in range(len(game_over_frame)):
                    game_over_frame_temp = game_over_frame_temp + game_over_frame[game_over_frame_index]
                print(game_over_frame_temp)
                break

        # 画面参数计算
        frames = calculate_frame_parameters()[0]  # 解包接受参数
        # 画面打印
        render_frame(frames)
        # 下一轮游戏参数计算
        calculate_game_parameters()

if __name__ == '__main__':
    play()