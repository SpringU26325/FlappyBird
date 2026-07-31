
# 导入模块
import time
import msvcrt
import random

#常量
WIDTH = 96
WIDTH0 = WIDTH//3
HEIGHT = 15
AIR = ' '#正式
# AIR = 'H'#测试
PIPE_IMAGE = '#'

#变量
bird_y = HEIGHT//2
bird_x = 1# WIDTH//12
score = 0
temp1 = -2
temp2 = -2
temp3 = -2
temp4 = -2

# 测试函数
def test(*args,**kwargs):
    print(args, kwargs,'test')

def play():
    # 变量引入
    global score,temp1,temp2,temp3,temp4,bird_x,bird_y,WIDTH,HEIGHT,AIR,PIPE_IMAGE

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
            information_line = f'得分：{score}' + ' ' * 3 + '按esc退出，按space跳跃'
            if frames[k][bird_y][bird_x] == PIPE_IMAGE or bird_y == (HEIGHT - 1):
                return
            frames[k][bird_y][bird_x] = '@'
            time.sleep(0.1)
            print('')
            print(information_line)
            # 字符串拼接
            for j in range(len(frames[k])):
                line_temp = ''
                for i in range(len(frames[k][j])):
                    line_temp = line_temp + frames[k][j][i]  # 临时字符串换行
                print(line_temp)

            if k % 4 == 3:# 下降速度
                bird_y += 1
            score += 1

            # 按键控制
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\x1b':  # 检测
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

play()
print(f'游戏结束，你这次的得分是{score}')











