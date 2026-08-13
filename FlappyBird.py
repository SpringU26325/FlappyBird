# 常量
WIDTH = 96
WIDTH0 = WIDTH // 3
HEIGHT = 15
AIR = ' '
PIPE_IMAGE = '#'


# 导入模块
import time
import msvcrt
import random
import sys
import copy
import datetime
import json


# 测试函数
def test(*args, **kwargs):
    print(args, kwargs, 'test')


# UI界面打印
def ui_frame(tip_input):
    blank_line = ' ' * WIDTH  # 空白行
    ui_frame_lines = [blank_line for j in range(HEIGHT)]  # 空白页
    # 分割线
    ui_frame_lines[0] = '-' * WIDTH
    ui_frame_lines[HEIGHT - 1] = '-' * WIDTH
    # 中间提示
    ui_frame_lines[HEIGHT // 2] = blank_line[:WIDTH // 2 - len(tip_input) // 2] + \
                                  tip_input + blank_line[WIDTH // 2 - len(tip_input) // 2 + len(tip_input):]
    # 拼接字符串
    ui_frame = '\n'.join(ui_frame_lines)
    # 打印UI页面
    print(ui_frame)


# 用户登录
def user_login():
    # 等待用户按下1或2
    ui_frame('按1选择单人模式，按2选择双人模式')
    while 1:
        key = msvcrt.getch()
        if key == b'1':
            player_num_flag_output = 1
            break
        elif key == b'2':
            player_num_flag_output = 2
            break
    print('\033[2J\033[3J\033[H', end='')
    if player_num_flag_output == 2:
        player1_name = input('玩家1昵称：')
        player2_name = input('玩家2昵称：')
        player_name_tuple_output = (player1_name, player2_name)
    elif player_num_flag_output == 1:
        player1_name = input('玩家昵称：')
        player_name_tuple_output = (player1_name,)
    user_login_flag_output = True
    return player_name_tuple_output, user_login_flag_output, player_num_flag_output


# 取出最佳成绩
def best_score_and_time_output(player_name_tuple, player_num_flag):
    try:
        with open('FlappyBirdRecord.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 根据模式读取对应玩家数据
            if player_num_flag == 1:
                # 单玩家模式：只读玩家1
                records = data.get(player_name_tuple[0], [(0, '???')])
                player1_best_record = max(records, key=lambda x: x[0])
            elif player_num_flag == 2:
                # 双玩家模式：同时读取两人
                records1 = data.get(player_name_tuple[0], [(0, '???')])
                records2 = data.get(player_name_tuple[1], [(0, '???')])
                player1_best_record = max(records1, key=lambda x: x[0])
                player2_best_record = max(records2, key=lambda x: x[0])
            else:
                # 未知模式，返回默认值（或者抛出异常）
                pass
    except (FileNotFoundError, json.JSONDecodeError):
        # 文件不存在或格式错误，保持默认值
        player1_best_record = (0, '???')
        player2_best_record = (0, '???') if player_num_flag == 2 else None

    # 根据模式返回对应结果
    if player_num_flag == 1:
        return (player1_best_record,)
    elif player_num_flag == 2:
        return player1_best_record, player2_best_record
    return None


def score_record(player_name_tuple, players_record, player_num_flag):
    # 新数据合并至旧数据
    play_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if player_num_flag == 1:
        player1_score = players_record[0]
    elif player_num_flag == 2:
        player1_score, player2_score = players_record

    try:  # 防止文件不存在
        try:
            with open('FlappyBirdRecord.json', mode='r', encoding='utf-8') as f:
                data_temp = json.load(f)  # 把json文件变成字典
        except json.decoder.JSONDecodeError:
            data_temp = {}
        try:
            data_temp[player_name_tuple[0]].append((player1_score, play_time))
        except KeyError:
            data_temp[player_name_tuple[0]] = [(player1_score, play_time)]
        if player_num_flag == 2:
            try:
                data_temp[player_name_tuple[1]].append((player2_score, play_time))
            except KeyError:
                data_temp[player_name_tuple[1]] = [(player2_score, play_time)]
    except FileNotFoundError:
        if player_num_flag == 1:
            data_temp = {player_name_tuple[0]: [(player1_score, play_time)]}
        elif player_num_flag == 2:
            data_temp = {player_name_tuple[0]: [(player1_score, play_time)],
                         player_name_tuple[1]: [(player2_score, play_time)]}
    # 数据写入
    data_temp_json = json.dumps(data_temp)
    with open('FlappyBirdRecord.json', mode='w', encoding='utf-8') as f:
        f.write(data_temp_json)


def get_key():  # 用于检测单个必须按键
    key = msvcrt.getch()
    return [key]


def poll_keys():
    keys = []
    while msvcrt.kbhit():
        key = msvcrt.getch()
        keys.append(key)
    return keys


def clear_key_buffer():
    """清空键盘缓冲区中所有遗留的按键"""
    while msvcrt.kbhit():
        msvcrt.getch()


# 鸟
class Bird:
    def __init__(self):
        self.image = '\033[31m@\033[0m'
        self.y = HEIGHT // 2
        self.score = 0
        self.x = 1
        self.death = False

    def fall(self):
        self.y += 1

    def rise(self):
        self.y -= 1

    def check_death_status(self, frames):
        if frames[self.y][self.x] == PIPE_IMAGE or self.y == HEIGHT - 1 or self.y == 0:
            self.death = True


# 水管
class Pipe:
    def __init__(self, x, y):
        self.image = '#'
        self.x = x
        self.y = y


class PipeManager:
    def __init__(self):
        self.pipes = [Pipe((WIDTH0 * k) - 1, random.randint(HEIGHT // 5, HEIGHT - HEIGHT // 5)) for k in range(4)]

    def update_pipes(self):
        for pipe in self.pipes:
            pipe.x -= 1
        if self.pipes[0].x == 0:
            self.pipes.append(Pipe(WIDTH, random.randint(HEIGHT // 5, HEIGHT - HEIGHT // 5)))
        if self.pipes[0].x <= -2:
            self.pipes.pop(0)


# 循环计数器
class CallCounter:
    def __init__(self):
        self.count = -1

    def execute(self):
        self.count += 1
        self.count = self.count % WIDTH0


# 每局游戏
class Game:
    def __init__(self, player_num_flag):
        self.game_running_flag = True
        self.pause_flag = False
        self.bird1 = Bird()
        if player_num_flag == 2:
            self.bird2 = Bird()
            self.bird2.image = '@'  # 测试用
        self.counter = CallCounter()
        self.dot_count = 5
        self.pipes_manager = PipeManager()

    def calculate_frame_parameters(self, player_num_flag):
        # 参数生成
        frames = [[AIR] * WIDTH for _ in range(HEIGHT)]  # 生成画面
        # 画管道
        for j in range(len(frames)):
            for i in range(len(frames[j])):
                for k in range(len(self.pipes_manager.pipes)):
                    if i == self.pipes_manager.pipes[k].x or i == self.pipes_manager.pipes[k].x - 1 or i == \
                            self.pipes_manager.pipes[k].x + 1:
                        if not ((j == self.pipes_manager.pipes[k].y) or (j == self.pipes_manager.pipes[k].y - 1) or (
                                j == self.pipes_manager.pipes[k].y + 1)):
                            frames[j][i] = PIPE_IMAGE
        # 插入：小鸟死亡检测检测
        self.bird1.check_death_status(frames)
        if player_num_flag == 2:
            self.bird2.check_death_status(frames)
        # 画小鸟
        if not self.bird1.death:
            frames[self.bird1.y][self.bird1.x] = self.bird1.image  # 画小鸟
        if player_num_flag == 2:
            if not self.bird2.death:
                frames[self.bird2.y][self.bird2.x] = self.bird2.image
        return frames

    @staticmethod  # 标志静态函数
    def calculate_pause_frame(pause_frame_input, dot_count_input):
        # 将信息提示 [C] Continue [ESC] Exit 转换成字符串列表
        tip_list = []
        tip_string = '[C] Continue [ESC] Exit'
        for string_index in range(len(tip_string)):
            tip_list.append(tip_string[string_index])

        # [C] Continue [ESC] Exit 加入列表frames
        for tip_list_index in range(len(tip_list)):
            pause_frame_input[HEIGHT // 2][WIDTH // 2 - len(tip_list) // 2 + tip_list_index] = tip_list[
                tip_list_index]
        # OOOOO 加入列表frames
        for dot in range(dot_count_input):
            pause_frame_input[HEIGHT // 2 + 1][WIDTH // 2 - dot_count_input // 2 + dot] = 'O'
        return pause_frame_input

    @staticmethod
    def render_frame(frame_input, info_line_input):
        separate_line = '-' * WIDTH
        lines = [separate_line, info_line_input]
        lines.extend(''.join(row) for row in frame_input)
        lines.append(separate_line)
        frame = '\n'.join(lines)
        print('\033[2J\033[3J\033[H', end='')
        print(frame)

    def calculate_game_parameters(self, player_num_flag, player_name_tuple, best_record):
        # 计算本次参数
        self.counter.execute()  # 计时参数+1
        self.pipes_manager.update_pipes()
        if self.counter.count % 4 == 3:
            if not self.bird1.death:
                self.bird1.fall()
            if player_num_flag == 2:
                if not self.bird2.death:
                    self.bird2.fall()
        # 计数器：管道参数和小鸟分数
        if self.counter.count == WIDTH0 - 1:
            if not self.bird1.death:
                self.bird1.score += 1
            if player_num_flag == 2:
                if not self.bird2.death:
                    self.bird2.score += 1
        # info
        if player_num_flag == 1:
            player1_best_score, player1_best_score_play_time = best_record[0]
            info = [f'{player_name_tuple[0]}当前得分{self.bird1.score}',
                    f'于{player1_best_score_play_time}取得历史最高分{player1_best_score}',
                    '[esc] 退出  [P] 暂停 [space] 跳跃']
        elif player_num_flag == 2:
            player1_best_score, player1_best_score_play_time = best_record[0]
            player2_best_score, player2_best_score_play_time = best_record[1]
            info = [f'{player_name_tuple[0]}当前得分{self.bird1.score}',
                    f'于{player1_best_score_play_time}取得历史最高分{player1_best_score}',
                    f'{player_name_tuple[1]}当前得分{self.bird2.score}',
                    f'于{player1_best_score_play_time}取得历史最高分{player2_best_score}',
                    '[esc] 退出  [P] 暂停 玩家1：[space] 跳跃；玩家2 [0] 跳跃']
        info_line_output = '\n'.join(info)
        return info_line_output

    def handle_pause_frame(self, frames_input, info_line):
        # 拷贝暂停画面
        pause_frame = copy.deepcopy(frames_input)
        # H包裹
        for j in range(HEIGHT // 4, HEIGHT - HEIGHT // 4):
            for i in range(WIDTH // 4, WIDTH - WIDTH // 4):
                pause_frame[j][i] = 'H'
        # 用空气填充内部
        for j in range(HEIGHT // 4 + 1, HEIGHT - HEIGHT // 4 - 1):
            for i in range(WIDTH // 4 + 1, WIDTH - WIDTH // 4 - 1):
                pause_frame[j][i] = AIR
        # 卡入循环
        while self.pause_flag:
            for dot_num in range(1, self.dot_count + 1):
                time.sleep(1)
                self.calculate_pause_frame(pause_frame, dot_num)
                self.render_frame(pause_frame, info_line)
                if dot_num == 5:  # 重置00000
                    for dot in range(dot_num):
                        pause_frame[HEIGHT // 2 + 1][WIDTH // 2 - dot_num // 2 + dot] = AIR
                if msvcrt.kbhit():
                    key = get_key()[0]
                    if key == b'\x1b':
                        self.game_running_flag = False
                        self.pause_flag = False
                        break

                    elif key == b'c' or key == b'C':
                        self.pause_flag = False
                        break
                    # 测试
                    elif key == b't' or key == b'T':
                        sys.exit(0)

    def react_keys(self, keys_input, player_num_flag, player_name_tuple, info_line):
        # 逐一操作按键
        for key in keys_input:
            # 游戏进程中监听
            if self.game_running_flag and not self.pause_flag:
                # 按P暂停
                if key.lower() == b'p':
                    self.pause_flag = True

                # 按空格、0跳跃
                elif key == b' ':
                    self.bird1.rise()

                elif key == b'0':
                    try:
                        self.bird2.rise()
                    except NameError:
                        pass

                # 按ESC结束
                elif key == b'\x1b':
                    self.game_running_flag = False
                    break
                # 测试：按T结束程序
                elif key == b't' or key == b'T':
                    sys.exit(0)

    def check_game_over(self,player_name_tuple, player_num_flag):
        # 游戏结束判断
        if player_num_flag == 1:
            if self.bird1.death:
                self.game_running_flag = False
        elif player_num_flag == 2:
            if self.bird1.death and self.bird2.death:
                self.game_running_flag = False

        # 游戏结束
        if not self.game_running_flag:
            time.sleep(2)
            print('\033[2J\033[3J\033[H', end='')
            if player_num_flag == 2:
                ui_frame(f'GAME OVER !Your score :{player_name_tuple[0]} : {self.bird1.score}---{player_name_tuple[1]} : {self.bird2.score}')
            elif player_num_flag == 1:
                ui_frame(f'GAME OVER !Your score : {player_name_tuple[0]} : {self.bird1.score}')
            time.sleep(2)
            print('\033[2J\033[3J\033[H', end='')
        return

    def run_game(self, player_num_flag, player_name_tuple, best_record):
        # 游戏主循环
        while self.game_running_flag:
            time.sleep(0.1)  # fps=10
            info_line = self.calculate_game_parameters(player_num_flag, player_name_tuple, best_record)  # 计算得分
            frames = self.calculate_frame_parameters(player_num_flag)  # 计算画面
            self.render_frame(frames, info_line)  # 打印画面
            keys = poll_keys()  # 按键轮询
            self.react_keys(keys, player_num_flag, player_name_tuple, info_line)  # 按键反应
            if self.pause_flag:
                self.handle_pause_frame(player_num_flag, info_line)
            self.check_game_over(player_name_tuple, player_num_flag)
        # 返回结果准备写入
        if player_num_flag == 1:
            players_record = (self.bird1.score,)
        elif player_num_flag == 2:
            players_record = self.bird1.score, self.bird2.score
        return players_record


def main():
    game_launching = True
    while game_launching:
        # 用户登录
        player_name_tuple, user_login_flag, player_num_flag = user_login()
        # 最佳成绩接收
        best_record = best_score_and_time_output(player_name_tuple, player_num_flag)
        if player_num_flag == 1:
            player1_best_record = best_record
        elif player_num_flag == 2:
            player1_best_record, player2_best_record = best_record
        # 开始游戏
        while user_login_flag:
            clear_key_buffer()
            while 1:
                ui_frame('按S以开始，按ESC以退出游戏，按C切换账号')
                key = get_key()[0]
                if key.lower() == b's':  # 按S以开始
                    game = Game(player_num_flag)  # 创建一局游戏
                    players_record = game.run_game(player_num_flag, player_name_tuple, best_record)  # 运行游戏并返回结果
                    score_record(player_name_tuple, players_record, player_num_flag)  # 结果写入
                elif key.lower() == b'\x1b':  # 按ESC以退出游戏
                    sys.exit(0)
                elif key.lower() == b'c':  # 按C切换账号
                    user_login_flag = False
                    print('\033[2J\033[3J\033[H', end='')


if __name__ == '__main__':
    main()
# python FlappyBird.py
# 暂停循环每次都会重新计算 calculate_frame_parameters 并 deepcopy 出暂停帧，哪怕画面根本没变。
# 完全可以进入暂停时缓存一个静态的暂停帧，然后一直复用。
