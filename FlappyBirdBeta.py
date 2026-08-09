

# 测试函数
def test(*args,**kwargs):
    print(args, kwargs,'test')

# 导入模块
import time
import msvcrt
import random
import sys
import copy
import datetime
# import os
import json

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
        self.image = '\033[31m@\033[0m'
        self.y = HEIGHT // 2
        # self.y = 0  # TEST
        self.score = 0
        self.x = 1
    def fall(self):
        self.y += 1
    def rise(self):
        self.y -= 1


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


# 用户登录
def user_login():
    user_name = input('账号：')
    user_login_flag = True
    return user_name, user_login_flag

# UI界面打印
def ui_frame(tip_input):
    ui_frame_temp = ''  # 待打印页面
    game_over_tip = tip_input  # 提示词
    blank_line = ' ' * (WIDTH + 2) + '\n' # 空白行
    ui_frame = []  # 待打印页面参数
    # 空白页
    for j in range(HEIGHT):
        ui_frame.append(blank_line)
    # 分割线
    ui_frame[0] = '-' * WIDTH
    ui_frame[HEIGHT - 1] = '-' * WIDTH
    # 中间提示
    ui_frame[HEIGHT // 2] = blank_line[:WIDTH // 2 - len(game_over_tip) // 2] + \
    game_over_tip +blank_line[WIDTH // 2 - len(game_over_tip) // 2 + len(game_over_tip):]

    # 打印UI页面
    for ui_frame_index in range(len(ui_frame)):
        ui_frame_temp = ui_frame_temp + ui_frame[ui_frame_index]
    print(ui_frame_temp)

# 结果记录
def score_record(player, score, play_time):
    try:
        with open('FlappyBirdRecord.txt', mode='r', encoding='utf-8') as f:
            data_temp = json.load(f)
        try:
            data_temp[player].append((score, play_time))
        except KeyError:
            data_temp[player] = [(score, play_time)]
    except FileNotFoundError:
        data_temp = {player: [(score, play_time)]}
    data_temp_json = json.dumps(data_temp)
    with open('FlappyBirdRecord.txt', mode='w', encoding='utf-8') as f:
        f.write(data_temp_json)

def best_score_and_time_output():
    try:
        with open('FlappyBirdRecord.txt', mode='r', encoding='utf-8') as f:
            dict_temp = json.load(f)
            player_score_and_time_list = dict_temp[user_name]
            player_best_record = max(player_score_and_time_list, key = lambda x: x[0])
            return player_best_record
    except (FileNotFoundError, KeyError):
        return 0, '???'
# 游戏
def play(user_name):
    bird1 = Bird()
    counter = CallCounter()
    best_score, best_score_play_time = best_score_and_time_output()
    game_flag = True
    pipes = [Pipe((WIDTH0 * k) - 2, random.randint(HEIGHT // 5, HEIGHT - HEIGHT // 5)) for k in range(4)]

    def calculate_frame_parameters():
        nonlocal pipes, game_flag
        # 参数生成
        frames = [[AIR] * WIDTH for _ in range(HEIGHT)]  # 生成画面
        # 画管道
        for j in range(len(frames)):
            for i in range(len(frames[j])):
                for k in range(len(pipes)):
                    if i == pipes[k].x or i == pipes[k].x - 1 or i == pipes[k].x + 1:
                        if not ((j == pipes[k].y) or (j == pipes[k].y - 1) or (j == pipes[k].y + 1)):
                            frames[j][i] = PIPE_IMAGE

        # 管道碰撞检测
        if frames[bird1.y][bird1.x] == PIPE_IMAGE:
            game_flag = False
        frames[bird1.y][bird1.x] = bird1.image  # 画小鸟
        # 画暂停画面
        pause_frame = copy.deepcopy(frames)
        # H包裹
        for j in range(HEIGHT // 4, HEIGHT - HEIGHT // 4):
            for i in range(WIDTH // 4, WIDTH - WIDTH // 4):
                pause_frame[j][i] = 'H'
        # 用空气填充内部
        for j in range(HEIGHT // 4 + 1, HEIGHT - HEIGHT // 4 - 1):
            for i in range(WIDTH // 4 + 1, WIDTH - WIDTH // 4 - 1):
                pause_frame[j][i] = AIR
        return frames, pause_frame

    def render_frame(frame_input, information_line, separate_line):
        # print('\033[H', end='')
        print('\033[2J\033[3J\033[H', end='')
        lines = [separate_line, information_line]
        lines.extend(''.join(row) for row in frame_input)
        lines.append(separate_line)
        frame = '\n'.join(lines)
        print(frame)

    def calculate_game_parameters():
        nonlocal game_flag
        # 计算下一次参数
        counter.execute()  # 计时参数+1
        for i in range(len(pipes)):
            pipes[i].x -= 1
        if bird1.y == HEIGHT - 1 or bird1.y == 0:
            game_flag = False
            time.sleep(2)
            print('\033[2J\033[3J\033[H', end='')
            ui_frame(f'GAME OVER !Your score : {bird1.score}')
            time.sleep(2)
            return
        if counter.count % 4 == 3:
            bird1.fall()
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
        information = [f'{user_name}当前得分{bird1.score}', f'于{best_score_play_time}取得历史最高分{best_score}',
                       '[esc] 退出  [P] 退出 [space] 跳跃']
        separator = '---'
        separate_line = '-' * WIDTH
        information_line = separator
        for information_line_index in range(len(information)):
            information_line = information_line + information[information_line_index] + separator



        # 按键监听
        if msvcrt.kbhit():
            key = msvcrt.getch()

            # 按P暂停
            if key == b'p' or key == b'P':
                dot_count = 6
                def calculate_pause_frame(dot_count_input, pause_frame_input):
                    # 将信息提示转换成字符串列表
                    tip_list = []
                    tip_string = '[C] Continue [ESC] Exit'
                    for string_index in range(len(tip_string)):
                        tip_list.append(tip_string[string_index])

                    # [C] Continue [ESC] Exit
                    for tip_list_index in range(len(tip_list)):
                        pause_frame_input[HEIGHT//2][WIDTH//2 - len(tip_list) // 2 + tip_list_index] = tip_list[tip_list_index]
                    # OOOOO
                    for dot in range(dot_count_input):
                        pause_frame_input[HEIGHT//2 + 1][WIDTH//2 - dot_count // 2 + dot] = 'O'  # 6

                # 卡入循环
                pause_flag = True
                while pause_flag:
                    pause_frame = calculate_frame_parameters()[1]
                    for dot_num in range(1, dot_count):
                        time.sleep(1)
                        calculate_pause_frame(dot_num, pause_frame)
                        render_frame(pause_frame, information_line, separate_line)
                        if msvcrt.kbhit():
                            key = msvcrt.getch()
                            if key == b'\x1b':
                                game_flag = False
                                pause_flag = False
                                break

                            elif key == b'c' or key == b'C':
                                pause_flag = False
                                break

                            elif key == b't' or key == b'T':
                                sys.exit(0)

            # 按空格跳跃
            elif key == b' ':
                bird1.rise()

            # 按ESC结束
            elif key == b'\x1b':
                time.sleep(2)
                print('\033[2J\033[3J\033[H', end='')
                ui_frame(f'GAME OVER !Your score : {bird1.score}')
                time.sleep(2)
                break

            elif key == b't' or key == b'T':
                sys.exit(0)

        # 画面参数计算
        frames = calculate_frame_parameters()[0]
        # 画面打印
        render_frame(frames, information_line, separate_line)
        if game_flag == False:  # 游戏状态为False打印结束画面
            time.sleep(2)
            # print('\033[H', end='')
            print('\033[2J\033[3J\033[H', end='')
            ui_frame(f'GAME OVER !Your score : {bird1.score}')
            time.sleep(2)
        # 下一轮游戏参数计算
        elif game_flag == True:
            calculate_game_parameters()
    return bird1, counter
if __name__ == '__main__':
    game_start_flag = True
    while game_start_flag:
        user_name, user_login_flag =user_login()
        while user_login_flag:
            time.sleep(0.05)
            # print('\033[H', end='')
            print('\033[2J\033[3J\033[H', end='')
            ui_frame('按S以开始，按ESC以结束，按C切换账号')
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key.lower() == b's':
                    bird1, counter = play(user_name)
                    play_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    score_record(user_name, bird1.score, play_time)
                    bird1.score = 0
                    counter.count = 0

                elif key == b'\x1b':
                    print('\033[2J\033[3J\033[H', end='')
                    sys.exit(0)

                elif key.lower() == b'c':
                    user_login_flag = False

# 测试：demo
# SpringU26325
# 304960459