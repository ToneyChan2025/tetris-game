#!/usr/bin/env python3
"""
俄罗斯方块游戏 (Tetris)
使用 pygame 开发
"""

import pygame
import random
from copy import deepcopy

# 初始化 pygame
pygame.init()

# 游戏常量
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
FPS = 60

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# 方块颜色
COLORS = [
    (0, 255, 255),    # 青色 (I)
    (255, 255, 0),    # 黄色 (O)
    (128, 0, 128),    # 紫色 (T)
    (0, 255, 0),      # 绿色 (S)
    (255, 0, 0),      # 红色 (Z)
    (0, 0, 255),      # 蓝色 (J)
    (255, 165, 0),    # 橙色 (L)
]

# 方块形状定义
SHAPES = [
    [[1, 1, 1, 1]],           # I
    [[1, 1], [1, 1]],         # O
    [[0, 1, 0], [1, 1, 1]],   # T
    [[0, 1, 1], [1, 1, 0]],   # S
    [[1, 1, 0], [0, 1, 1]],   # Z
    [[1, 0, 0], [1, 1, 1]],   # J
    [[0, 0, 1], [1, 1, 1]],   # L
]

class Piece:
    def __init__(self, x, y, shape_index):
        self.x = x
        self.y = y
        self.shape_index = shape_index
        self.shape = SHAPES[shape_index]
        self.color = COLORS[shape_index]
        self.rotation = 0
    
    def get_rotated_shape(self):
        """获取旋转后的形状"""
        shape = self.shape
        for _ in range(self.rotation % 4):
            shape = [list(row) for row in zip(*shape[::-1])]
        return shape

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("俄罗斯方块 - Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
    
    def reset_game(self):
        """重置游戏"""
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = 1000  # 毫秒
    
    def new_piece(self):
        """创建新方块"""
        shape_idx = random.randint(0, len(SHAPES) - 1)
        x = GRID_WIDTH // 2 - len(SHAPES[shape_idx][0]) // 2
        return Piece(x, 0, shape_idx)
    
    def valid_move(self, piece, x_offset=0, y_offset=0, rotation=0):
        """检查移动是否有效"""
        test_rotation = (piece.rotation + rotation) % 4
        shape = piece.shape
        for _ in range(test_rotation):
            shape = [list(row) for row in zip(*shape[::-1])]
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + x_offset
                    new_y = piece.y + y + y_offset
                    
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True
    
    def lock_piece(self, piece):
        """锁定方块到网格"""
        shape = piece.get_rotated_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = piece.y + y
                    grid_x = piece.x + x
                    if 0 <= grid_y < GRID_HEIGHT and 0 <= grid_x < GRID_WIDTH:
                        self.grid[grid_y][grid_x] = piece.shape_index + 1
        
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        if not self.valid_move(self.current_piece):
            self.game_over = True
    
    def clear_lines(self):
        """清除满行"""
        lines = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines += 1
            else:
                y -= 1
        
        if lines > 0:
            self.lines_cleared += lines
            self.score += lines * 100 * self.level
            if lines == 4:
                self.score += 400 * self.level  # 奖励四消
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(100, 1000 - (self.level - 1) * 100)
    
    def handle_input(self):
        """处理输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        return False
                    continue
                
                if event.key == pygame.K_LEFT:
                    if self.valid_move(self.current_piece, x_offset=-1):
                        self.current_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if self.valid_move(self.current_piece, x_offset=1):
                        self.current_piece.x += 1
                elif event.key == pygame.K_DOWN:
                    if self.valid_move(self.current_piece, y_offset=1):
                        self.current_piece.y += 1
                        self.score += 1
                elif event.key == pygame.K_UP:
                    if self.valid_move(self.current_piece, rotation=1):
                        self.current_piece.rotation += 1
                elif event.key == pygame.K_SPACE:
                    # 快速下落
                    while self.valid_move(self.current_piece, y_offset=1):
                        self.current_piece.y += 1
                        self.score += 2
                    self.lock_piece(self.current_piece)
                elif event.key == pygame.K_p:
                    self.pause_game()
        
        return True
    
    def pause_game(self):
        """暂停游戏"""
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    paused = False
            
            self.draw_text("暂停 - 按 P 继续", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, WHITE)
            pygame.display.flip()
            self.clock.tick(FPS)
        return True
    
    def update(self, dt):
        """更新游戏状态"""
        if self.game_over:
            return
        
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            if self.valid_move(self.current_piece, y_offset=1):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)
    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BLACK)
        
        # 绘制网格背景
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, DARK_GRAY, rect, 1)
        
        # 绘制已固定的方块
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    color = COLORS[cell - 1]
                    self.draw_block(x, y, color)
        
        # 绘制当前方块
        if not self.game_over:
            shape = self.current_piece.get_rotated_shape()
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        self.draw_block(
                            self.current_piece.x + x,
                            self.current_piece.y + y,
                            self.current_piece.color
                        )
        
        # 绘制侧边栏信息
        sidebar_x = GRID_WIDTH * BLOCK_SIZE + 20
        
        # 分数
        self.draw_text(f"分数: {self.score}", sidebar_x, 20, WHITE)
        self.draw_text(f"等级: {self.level}", sidebar_x, 60, WHITE)
        self.draw_text(f"行数: {self.lines_cleared}", sidebar_x, 100, WHITE)
        
        # 下一个方块预览
        self.draw_text("下一个:", sidebar_x, 160, WHITE)
        shape = self.next_piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        sidebar_x + x * BLOCK_SIZE,
                        200 + y * BLOCK_SIZE,
                        BLOCK_SIZE - 2,
                        BLOCK_SIZE - 2
                    )
                    pygame.draw.rect(self.screen, self.next_piece.color, rect)
        
        # 操作说明
        instructions = [
            "操作说明:",
            "← → 移动",
            "↓ 加速下落",
            "↑ 旋转",
            "空格 直接落下",
            "P 暂停",
        ]
        y_offset = 350
        for line in instructions:
            self.draw_text(line, sidebar_x, y_offset, GRAY, small=True)
            y_offset += 25
        
        # 游戏结束画面
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            self.draw_text("游戏结束!", SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 50, WHITE)
            self.draw_text(f"最终分数: {self.score}", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, WHITE)
            self.draw_text("按 R 重新开始", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, GRAY)
            self.draw_text("按 Q 退出", SCREEN_WIDTH//2 - 70, SCREEN_HEIGHT//2 + 80, GRAY)
        
        pygame.display.flip()
    
    def draw_block(self, x, y, color):
        """绘制单个方块"""
        if y < 0:
            return
        rect = pygame.Rect(x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
        pygame.draw.rect(self.screen, color, rect)
        # 高光效果
        highlight_color = tuple(min(255, c + 50) for c in color)
        pygame.draw.rect(self.screen, highlight_color, rect, 2)
    
    def draw_text(self, text, x, y, color, small=False):
        """绘制文字"""
        font = self.small_font if small else self.font
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))
    
    def run(self):
        """主游戏循环"""
        running = True
        while running:
            dt = self.clock.tick(FPS)
            running = self.handle_input()
            self.update(dt)
            self.draw()
        
        pygame.quit()

def main():
    print("俄罗斯方块游戏启动!")
    print("操作说明:")
    print("  ← → : 左右移动")
    print("  ↓   : 加速下落")
    print("  ↑   : 旋转")
    print("  空格 : 直接落下")
    print("  P   : 暂停")
    print("=" * 40)
    
    game = TetrisGame()
    game.run()

if __name__ == "__main__":
    main()
