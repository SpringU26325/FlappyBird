
# 导入模块
import time
import msvcrt
import random

#常量
WIDTH = 48
HEIGHT = 15
AIR = ' '#正式
# AIR = 'H'#测试
PIPE_AIR_IMAGE = AIR*3
PIPE_IMAGE = '#'

#变量
bird_y = HEIGHT//2
bird_x = WIDTH//4+1
score = 0
temp1 = -2
temp2 = -2
temp3 = -2
temp4 = -2




if __name__ == '__main__':


    # 游戏画面
    # 管道宽3，高HIGHT，口子3。画面内有3根管道
    # 游戏画面变量计算
    # 1.管道
    def random_pipe():# 生成一个大致位于中间的数
        return random.randint(HEIGHT // 5, HEIGHT - HEIGHT // 5)

    # temp1 = temp2
    # temp2 = temp3
    # temp3 = pipe_temp
    # print(temp1)
    # print(temp2)
    # print(temp3)

    # 2.小鸟

    # 游戏画面参数计算
    while True:
        temp1 = random_pipe()
        temp2 = random_pipe()
        temp3 = random_pipe()
        list_temp1 = [temp1, temp1 + 1, temp1 - 1]  # TEST:[5,4,3]
        list_temp2 = [temp2, temp2 + 1, temp2 - 1]
        list_temp3 = [temp3, temp3 + 1, temp3 - 1]

    # for _ in range(1): # 循环16次

        # 按键控制
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x1b':  # 检测
                break
            elif key == b' ':
                bird_y += 1
            else:
                pass
        information_line = f'得分：{score}' + ' ' * 3 + '按esc退出，按space跳跃'
        time.sleep(0.0147)
        frames = [[[AIR for i in range(WIDTH)] for j in range(HEIGHT)] for k in range(int(WIDTH/3))]
        # 内层 i 列表推导式生成每一行的48字符，中层 j 生成15行，最外层 k 生成16个循环帧

        #生成管道
        for k in range(len(frames)):
            for j in range(len(frames[k])):
                seg_width = int(WIDTH/3)
                for offset in (13, 14, 15):  # 三个偏移量
                    base = (offset - k) % seg_width  # 基础列索引（不含段偏移）
                    for seg in range(3):  # 三个段（0, 1, 2）
                        frames[k][j][base + seg * seg_width] = PIPE_IMAGE

        # 生成管道空气
        for k in range(len(frames)): #每帧

                # for i in range(len(frames[k][j])):
            #:##             ###             ###             #
            if frames[k][0][0] == PIPE_IMAGE and frames[k][0][1] == PIPE_IMAGE and frames[k][0][2] == AIR:
                temp4 = random_pipe()
                list_temp4 = [temp4, temp4 + 1, temp4 - 1]

                for j in range(len(frames[k])):  # 每行
                    if j in list_temp1:
                        frames[k][j][0] = AIR
                        frames[k][j][1] = AIR
                    if j in list_temp2:
                        frames[k][j][15] = AIR
                        frames[k][j][16] = AIR
                        frames[k][j][17] = AIR
                    if j in list_temp3:
                        for i in (15+16,16+16,17+16):
                            frames[k][j][i] = AIR
                    if j in list_temp4:
                        frames[k][j][WIDTH-1] = AIR

                #:#             ###             ###             ##
            elif frames[k][0][0] == PIPE_IMAGE and frames[k][0][1] == AIR and frames[k][0][2] == AIR:
                for j in range(len(frames[k])):  # 每行
                    if j in list_temp1:
                        frames[k][j][0] = AIR
                    if j in list_temp2:
                        frames[k][j][14] = AIR
                        frames[k][j][15] = AIR
                        frames[k][j][16] = AIR
                    if j in list_temp3:
                        for i in (14 + 16, 15 + 16, 16 + 16):
                            frames[k][j][i] = AIR
                    if j in list_temp4:
                        frames[k][j][WIDTH - 1] = AIR
                        frames[k][j][WIDTH - 2] = AIR

                # elif frames[k][j][0] == AIR and frames[k][j][1] == AIR and frames[k][j][2] == AIR:
                #     pass

            # 三根管道
            else:
                i = frames[k][0].index(PIPE_IMAGE)
                for j in range(len(frames[k])):  # 每行
                    if j in list_temp1:
                        frames[k][j][i] = AIR
                        frames[k][j][i + 1] = AIR
                        frames[k][j][i + 2] = AIR
                    if j in list_temp2:
                        frames[k][j][i + 16] = AIR
                        frames[k][j][i + 1 + 16] = AIR
                        frames[k][j][i + 2 + 16] = AIR
                    if j in list_temp3:
                        frames[k][j][i + 16 * 2] = AIR
                        frames[k][j][i + 1 + 16 * 2] = AIR
                        frames[k][j][i + 2 + 16 * 2] = AIR
        # 随机数重置：
        temp1 = temp2
        temp2 = temp3
        temp3 = temp4

        pass

        # 游戏画面绘制
        for k in range(len(frames)):
            time.sleep(0.02)
            print('')
            print(information_line)
            # 字符串拼接
            for j in range(len(frames[k])):
                line_temp = ''
                for i in range(len(frames[k][j])):
                    line_temp = line_temp + frames[k][j][i]#临时字符串换行
                print(line_temp)
        # test
        break













