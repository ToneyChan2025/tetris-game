# 俄罗斯方块游戏 (Tetris)

一个使用 Python 和 Pygame 开发的经典俄罗斯方块游戏。

## 功能特性

- ✅ 完整的俄罗斯方块游戏逻辑
- ✅ 7 种经典方块形状
- ✅ 方块旋转和移动
- ✅ 消行计分系统
- ✅ 等级系统（速度随等级增加）
- ✅ 下一个方块预览
- ✅ 暂停功能
- ✅ 游戏结束和重新开始

## 操作说明

| 按键 | 功能 |
|------|------|
| ← | 向左移动 |
| → | 向右移动 |
| ↓ | 加速下落 |
| ↑ | 旋转方块 |
| 空格 | 直接落下 |
| P | 暂停/继续 |
| R | 游戏结束后重新开始 |
| Q | 退出游戏 |

## 运行要求

- Python 3.7+
- Pygame

## 安装依赖

```bash
pip install pygame
```

## 运行游戏

```bash
python tetris.py
```

## 打包成可执行文件

```bash
# 安装 pyinstaller
pip install pyinstaller

# 打包
pyinstaller --onefile --windowed tetris.py
```

打包后的可执行文件在 `dist/` 目录中。

## 游戏截图

（待添加）

## 技术栈

- Python 3
- Pygame

## 作者

ToneyChan2025

## 许可证

MIT License
