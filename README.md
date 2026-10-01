# Flappy Bird - 终端版 (Console Flappy Bird)

一个由纯 Python 编写的、运行在 Windows 终端下的 Flappy Bird 小游戏。支持单人/双人模式，带有物理引擎、存档系统和暂停界面。

## ✨ 功能特性 (Features)
- **真实物理引擎**：采用亚像素累加器平滑移动，加入三次方空气阻力和重力模拟，手感丝滑。
- **双人模式**：支持两名玩家同屏竞技（玩家1红鸟，玩家2蓝鸟）。
- **数据持久化**：使用 JSON 自动保存历史最高分和达成时间。
- **游戏内UI**：完美支持暂停、切换账号、重开和ESC退出。
- **防伪标识**：自带 ZCY 灵魂防伪 ASCII 艺术。

## 🖥️ 运行环境 (Prerequisites)
- **操作系统**：仅支持 **Windows**（因为使用了 `msvcrt` 模块和底层 API 禁用输入法）。
- **Python 版本**：Python 3.6 及以上。
- **依赖**：零第三方依赖，纯原生 Python 标准库。

## 🚀 如何游玩 (How to Run)
1. 克隆或下载本仓库的代码到本地。
2. 打开 Windows 终端（CMD 或 PowerShell），导航到代码所在目录。
3. 运行游戏：
   ```bash
   python FlappyBird.py
