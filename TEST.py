# import time
# import os
#
#
# def generate_ascii_frames():
#     width = 16  # 总宽度 = 4组 * 4个字符 = 16
#     block_len = 3  # 阴影块的长度是 3
#     frames = []  # 存放所有的帧
#
#     # 循环生成 16 个不同的状态（走完一个完整的循环）
#     for i in range(16):
#         # 初始化一行全部为 H
#         arr = ['H'] * width
#
#         # 核心逻辑：阴影的起始位置从 0-based 索引 13 开始，每次向左移动 1 格
#         start = (13 - i) % width
#         for j in range(block_len):
#             idx = (start + j) % width
#             arr[idx] = '#'  # 将当前位置替换为 #
#
#         # 将 16 个字符切分成 4 组，并用空格连接
#         line = ' '.join(''.join(arr[k:k + 4]) for k in range(0, width, 4))
#         frames.append(line)
#
#     return frames
#
#
# # ----------------- 运行动画测试 -----------------
# frames = generate_ascii_frames()
#
# print("开始生成循环动画，按 Ctrl+C 可以停止：")
# try:
#     while True:  # 无限循环播放
#         for frame in frames:
#             # 清屏命令 (Windows用 cls，Mac/Linux用 clear)
#             os.system('cls' if os.name == 'nt' else 'clear')
#             print(frame)
#             time.sleep(0.15)  # 每一帧停留 0.15 秒
# except KeyboardInterrupt:
#     print("\n动画结束！")

