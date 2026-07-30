#导入模块







'''
第二行效果
k = 0
HHHH HHHH HHHH H###       H H H H  H H H H  H H H H  H # # #     H H H H  H H H H  H H H H  H # # #
0123 4567 891011 12131415      16171819 20212223 24252627 28293031    32333435 36373839 40414243 44454647
k = 1
HHHH HHHH HHHH ###H

13 -> 12

'''


# 游戏进程
# 初次加载：
# print('正在初始化，请稍后。。。')
# for _ in range(int((WIDTH-(WIDTH//4+1))/4)):
#     time.sleep(1)
#     bird_y -= 1
#     bird_x += 1

# print('初始化完成')
# time.sleep(1)
# print('3')
# time.sleep(1)
# print('2')
# time.sleep(1)
# print('1')
# while True:
#     time.sleep(2)
#     bird_y-=1
#     bird_x+=1

    # 按键控制
    # if msvcrt.kbhit():
    #     key = msvcrt.getch()
    #     if key == b'\x1b':#检测
    #         break
    #     elif key == b' ':
    #         bird_y += 1
    #     else:
    #         pass


# #每过一个管道1分
# #结算界面
# print('\n')
# print('游戏结束')
# print(f'你的得分是{score}')