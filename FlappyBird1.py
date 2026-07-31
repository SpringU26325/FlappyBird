

# 导入模块
import time
import msvcrt
import random
import math
import datetime
import os



#常量
WIDTH = 96
WIDTH0 = WIDTH//3
HEIGHT = 15
AIR = ' '#正式
# AIR = 'H'#测试
PIPE_IMAGE = '#'

# 加载
print(math.ceil((WIDTH-5)/2)*'-' + '正在初始化' + math.floor((WIDTH-5)/2)*'-')
#变量
bird_y = HEIGHT//2
bird_x = 1# WIDTH//12
score = 0
temp1 = -2
temp2 = -2
temp3 = -2
temp4 = -2
flag = True

# 测试函数
def test(*args,**kwargs):
    print(args, kwargs,'test')

def play():
    # 变量引入
    global score,temp1,temp2,temp3,temp4,bird_x,bird_y,WIDTH,HEIGHT,AIR,PIPE_IMAGE,flag

    # 1.管道随机数
    def random_pipe():# 生成一个大致位于中间的数
        return random.randint(HEIGHT // 5, HEIGHT - HEIGHT // 5)
    temp1 = random_pipe()
    temp2 = random_pipe()
    temp3 = random_pipe()
    list_temp1 = [temp1, temp1 + 1, temp1 - 1]  # TEST:[5,4,3]
    list_temp2 = [temp2, temp2 + 1, temp2 - 1]
    list_temp3 = [temp3, temp3 + 1, temp3 - 1]

    # 2.小鸟
    # 游戏画面参数计算
    while True:
        frames = [[[AIR for i in range(WIDTH)] for j in range(HEIGHT)] for k in range(WIDTH0)]
        # 内层 i 列表推导式生成每一行的48字符，中层 j 生成15行，最外层 k 生成16个循环帧

        #生成管道
        for k in range(len(frames)):
        # if test:
        #     k = 0
            for j in range(len(frames[k])):
                for offset in (WIDTH0 - 3, WIDTH0 - 2, WIDTH0 - 1):  # 三个偏移量
                    base = (offset - k) % WIDTH0  # 基础列索引（不含段偏移）
                    for seg in range(3):  # 三个段（0, 1, 2）
                        frames[k][j][base + seg * WIDTH0] = PIPE_IMAGE

        # 生成管道空气
        for k in range(len(frames)): #每帧
        # if test:
        #     k = 0

            #:##             ###             ###             #
            if frames[k][0][0] == PIPE_IMAGE and frames[k][0][1] == PIPE_IMAGE and frames[k][0][2] == AIR:
                temp4 = random_pipe()
                list_temp4 = [temp4, temp4 + 1, temp4 - 1]

                for j in range(len(frames[k])):  # 每行
                    if j in list_temp1:
                        frames[k][j][0] = AIR
                        frames[k][j][1] = AIR
                    if j in list_temp2:
                        frames[k][j][WIDTH0 - 1] = AIR
                        frames[k][j][WIDTH0] = AIR
                        frames[k][j][WIDTH0 + 1] = AIR
                    if j in list_temp3:
                        for i in (WIDTH0 - 1+ WIDTH0,WIDTH0 + WIDTH0,WIDTH0 + 1 + WIDTH0):
                            frames[k][j][i] = AIR
                    if j in list_temp4:
                        frames[k][j][WIDTH-1] = AIR

            #:#             ###             ###             ##
            elif frames[k][0][0] == PIPE_IMAGE and frames[k][0][1] == AIR and frames[k][0][2] == AIR:
                for j in range(len(frames[k])):  # 每行
                    if j in list_temp1:
                        frames[k][j][0] = AIR
                    if j in list_temp2:
                        frames[k][j][WIDTH0 - 2] = AIR
                        frames[k][j][WIDTH0 - 1] = AIR
                        frames[k][j][WIDTH0] = AIR
                    if j in list_temp3:
                        for i in (WIDTH0 - 2 + WIDTH0, WIDTH0 - 1 + WIDTH0, WIDTH0 + WIDTH0):
                            frames[k][j][i] = AIR
                    if j in list_temp4:
                        frames[k][j][WIDTH - 1] = AIR
                        frames[k][j][WIDTH - 2] = AIR

            # 三根管道
            else:
                i = frames[k][0].index(PIPE_IMAGE)
                for j in range(len(frames[k])):  # 每行
                    if j in list_temp1:
                        frames[k][j][i] = AIR
                        frames[k][j][i + 1] = AIR
                        frames[k][j][i + 2] = AIR
                    if j in list_temp2:
                        frames[k][j][i + WIDTH0] = AIR
                        frames[k][j][i + 1 + WIDTH0] = AIR
                        frames[k][j][i + 2 + WIDTH0] = AIR
                    if j in list_temp3:
                        frames[k][j][i + WIDTH0 * 2] = AIR
                        frames[k][j][i + 1 + WIDTH0 * 2] = AIR
                        frames[k][j][i + 2 + WIDTH0 * 2] = AIR

        # 游戏画面绘制

        for k in range(len(frames)):
        # if test:
        #     k = 0
            # 生成小鸟 & 结束
            information_line = f'{user_name}得分：{score}' + ' ' * 3 + '按esc退出，按space跳跃' + ' '*3 + '小鸟图标：@' +' '*3+ f'管道图标{PIPE_IMAGE}'
            ceil_line = '-' * WIDTH
            floor_line = '-' * WIDTH
            if frames[k][bird_y][bird_x] == PIPE_IMAGE or bird_y == (HEIGHT - 1) or bird_y == 0:
                return
            frames[k][bird_y][bird_x] = '@'
            time.sleep(0.1)
            print('')
            print(ceil_line)
            print(information_line)
            # 字符串拼接
            for j in range(len(frames[k])):
                line_temp = ''
                for i in range(len(frames[k][j])):
                    line_temp = line_temp + frames[k][j][i]  # 临时字符串换行
                print(line_temp)
            print(floor_line)

            if k % 4 == 3:# 下降速度
                bird_y += 1
            score += 1

            # 按键控制
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\x1b':  # 检测
                    flag = False
                    return
                elif key == b' ':
                    bird_y -= 1
                else:
                    pass

        # 随机数重置：
        temp1 = temp2
        temp2 = temp3
        temp3 = temp4

        list_temp1 = [temp1, temp1 + 1, temp1 - 1]
        list_temp2 = [temp2, temp2 + 1, temp2 - 1]
        list_temp3 = [temp3, temp3 + 1, temp3 - 1]
print(math.ceil((WIDTH-5)/2)*'-' + '初始化完成' + math.floor((WIDTH-5)/2)*'-')
user_name = input('账号：')


while flag :
# if 1:
    # 游戏进程
    # 倒计时，供玩家准备
    time.sleep(1)
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')
    # 游戏函数
    play()
    # 结算
    print('')
    print(f'游戏结束，你这次的得分是{score}')

    # 结果写入
    play_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    def file_input():
        global user_name, play_time, score
        with open('FlappyBirdRecord.txt',mode = 'r',encoding='utf-8') as f:
            with open('FlappyBirdRecord_copy.txt',mode = 'w',encoding='utf-8') as f0:
                for line in f:
                    f0.write(line)
                    f0.write('\n')
                f0.write(f'{user_name}于{play_time}取得了{score}分')

    try:# 保证有个文件
        file_input()
    except FileNotFoundError:
        with open('FlappyBirdRecord.txt', mode='w', encoding='utf-8'):
            pass
        file_input()
    os.remove('FlappyBirdRecord.txt')
    os.rename('FlappyBirdRecord_copy.txt','FlappyBirdRecord.txt')

    user_input = input('按Q退出，按R重新开始')
    if user_input.upper == 'R':
        bird_y = HEIGHT // 2
        bird_x = 1  # WIDTH//12
        score = 0
        temp1 = -2
        temp2 = -2
        temp3 = -2
        temp4 = -2
    elif user_input.upper == 'Q':
        test()
        flag = False
        break



# python FlappyBird1.py
# SpringU26325
# 304960459
# 自律自强
# 456







