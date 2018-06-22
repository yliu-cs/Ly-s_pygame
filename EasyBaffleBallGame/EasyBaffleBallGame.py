# -*- coding:utf-8 -*-

from sys import exit

import pygame
from pygame.locals import *

pygame.init()

# 创建窗口
ScreenWidth = 500
ScreenHright = 720
ScreenSize = (ScreenWidth, ScreenHright)
Screen = pygame.display.set_mode(ScreenSize, 0, 32)
pygame.display.set_caption("Ly's Easy Ball Game")
# 背景音乐
pygame.mixer.music.load('Sugar.mp3')
pygame.mixer.music.play(-1, 0.0)
# 碰撞音效
CollisionMusic = pygame.mixer.Sound('collision.wav')
# 重新开始按钮音效
ButtonMusic = pygame.mixer.Sound('button.wav')
# 游戏结束音效
GameOverMusic = pygame.mixer.Sound('over.wav')

def GameStart():
    # 游戏背景Surface对象
    Background = pygame.image.load('GameBackground.jpg').convert()
    # 挡板Surface对象
    Baffle = pygame.image.load('Baffle.png').convert_alpha()
    # 球Surface对象
    Ball = pygame.image.load('Ball.png').convert_alpha()
    # 挡板位置信息
    BaffleX = 140
    BaffleY = 600
    BaffleSpeed = 1000
    BaffleXSpeed = BaffleSpeed
    BaffleYSpeed = BaffleSpeed
    BaffleMove = {K_LEFT: 0, K_RIGHT: 0, K_UP: 0, K_DOWN: 0}
    # 球位置信息
    BallX = 235
    BallY = 0
    BallSpeed = 1000.
    BallXSpeed = BallSpeed
    BallYSpeed = BallSpeed

    # 帧率控制Clock对象
    FPSClock = pygame.time.Clock()
    # 时间显示Clock对象
    ProgramRunClock = pygame.time.get_ticks()
    # 时间显示Font对象
    RunTimeFont = pygame.font.Font('Jura-DemiBold.ttf', 24)

    # 游戏结果
    GameResult = ''

    while True:
        # 接收信息处理
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key in BaffleMove:
                    BaffleMove[event.key] = 1
            elif event.type == KEYUP:
                if event.key in BaffleMove:
                    BaffleMove[event.key] = 0

        # 绘制背景
        Screen.blit(Background, (0, 0))

        RunTimeStr = str((pygame.time.get_ticks() - ProgramRunClock) / 1000.0)
        # print(RunTimeStr)
        # 使用render方法显示时间字体
        RunTimeSurface = RunTimeFont.render(RunTimeStr, True, (255, 52, 179))
        # 显示时间
        Screen.blit(RunTimeSurface, (0, 0))

        # 距上次调用clock对象时间
        SecondTimePassed = FPSClock.tick(60) / 1000.0

        # 绘制球
        Screen.blit(Ball, (BallX, BallY))

        BallX += BallXSpeed * SecondTimePassed
        BallY += BallYSpeed * SecondTimePassed

        # 判断球边界条件
        if BallX > 500 - Ball.get_width():
            BallXSpeed = -BallXSpeed
            BallX = 500 - Ball.get_width()
        elif BallX < 0:
            BallXSpeed = -BallXSpeed
            BallX = 0
        if BallY > 720 - Ball.get_width():
            BallYSpeed = -BallYSpeed
            BallY = 720 - Ball.get_width()
        elif BallY < 0:
            BallYSpeed = -BallYSpeed
            BallY = 0

        # 定位挡板移动后坐标
        BaffleX -= BaffleMove[K_LEFT] * BaffleXSpeed * SecondTimePassed
        BaffleX += BaffleMove[K_RIGHT] * BaffleXSpeed * SecondTimePassed
        BaffleY -= BaffleMove[K_UP] * BaffleYSpeed * SecondTimePassed
        BaffleY += BaffleMove[K_DOWN] * BaffleYSpeed * SecondTimePassed

        # 判断挡板边界条件
        if BaffleX > 500 - Baffle.get_width():
            BaffleX = 500 - Baffle.get_width()
        elif BaffleX < 0:
            BaffleX = 0
        if BaffleY > 720 - 45 - Baffle.get_height():
            BaffleY = 720 - 45 - Baffle.get_height()
        elif BaffleY < 720 - Baffle.get_height() * 3:
            BaffleY = 720 - Baffle.get_height() * 3
        # 绘制挡板
        Screen.blit(Baffle, (BaffleX, BaffleY))

        # 判断球碰撞挡板条件
        # 挡板左上角
        if BallX == BaffleX - Ball.get_width() and BallY == BaffleY - Ball.get_height():
            BallXSpeed = -BallXSpeed
            BallYSpeed = -BallYSpeed
            CollisionMusic.play()
        # 挡板左下角
        elif BallX == BaffleX - Ball.get_width() and BallY == BaffleY + Baffle.get_height():
            BallXSpeed = -BallXSpeed
            BallYSpeed = -BallYSpeed
            CollisionMusic.play()
        # 挡板右上角
        elif BallX == BaffleX + Baffle.get_width() and BallY == BaffleY - Ball.get_height():
            BallXSpeed = -BallXSpeed
            BallYSpeed = -BallYSpeed
            CollisionMusic.play()
        # 挡板右下角
        elif BallX == BaffleX + Baffle.get_width() and BallY == BaffleY + Baffle.get_height():
            BallXSpeed = -BallXSpeed
            BallYSpeed = -BallYSpeed
            CollisionMusic.play()
        # 挡板上表面
        elif BallX > BaffleX and BallX < BaffleX + Baffle.get_width() and BallY > BaffleY - Ball.get_height() and BallY < BaffleY:
            BallYSpeed = -BallYSpeed
            BallY = BaffleY - Ball.get_height()
            CollisionMusic.play()
        # 挡板下表面
        elif BallX > BaffleX and BallX < BaffleX + Baffle.get_width() and BallY < BaffleY + Baffle.get_height() and BallY > BaffleY:
            BallYSpeed = -BallYSpeed
            BallY = BaffleY + Baffle.get_height()
            CollisionMusic.play()
        # 挡板左侧面
        elif BallY > BaffleY and BallY < BaffleY + Baffle.get_height() and BallX > BaffleX - Ball.get_width() and BallX < BaffleX:
            BallXSpeed = -BallXSpeed
            BallX = BaffleX
            CollisionMusic.play()
        # 挡板右侧面
        elif BallY > BaffleY and BallY < BaffleY + Baffle.get_height() and BallX > BaffleX + Baffle.get_width() - Ball.get_width() and BallX < BaffleX + Baffle.get_width():
            BallXSpeed = -BallXSpeed
            BallX = BaffleX + Baffle.get_width()
            CollisionMusic.play()

        if BallY > 720 - 45:
            GameResult = RunTimeStr
            GameOverMusic.play()
            return GameResult

        # 刷新显示
        pygame.display.update()

def GameResult(GameResult):
    # 游戏结果背景Surface对象
    GameResultBackground = pygame.image.load('GameResultBackground.png').convert()
    # 游戏结果引导
    ResultHint = pygame.image.load('ResultFont.png').convert_alpha()
    # 游戏结果Font对象
    GameResultFont = pygame.font.Font('EuroBold.ttf', 100)
    # 重新开始按钮
    ReStartButton = pygame.image.load('ReStartButton.png').convert_alpha()
    # 重新开始Hover按钮
    ReStartButtonHover = pygame.image.load('ReStartButtonHover.png').convert_alpha()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and 150 <= event.pos[
                0] <= 150 + ReStartButton.get_width() and 450 <= event.pos[1] <= 450 + ReStartButton.get_height():
                ButtonMusic.play()
                return True
        # 游戏结果背景
        Screen.blit(GameResultBackground, (0, 0))
        # 游戏结果引导
        Screen.blit(ResultHint, (45, 200))
        RunTimeSurface = GameResultFont.render(GameResult, True, (255, 69, 0))
        Screen.blit(RunTimeSurface, (90, 270))
        # 重新开始游戏按钮
        MouseX, MouseY = pygame.mouse.get_pos()
        if 150 <= MouseX <= 150 + ReStartButton.get_width() and 450 <= MouseY <= 450 + ReStartButton.get_height():
            Screen.blit(ReStartButtonHover, (150, 450))
        else:
            Screen.blit(ReStartButton, (150, 450))
        # 游戏结果
        pygame.display.update()

if __name__ == '__main__':
    flag = True
    while flag:
        GameResultStr = GameStart()
        if GameResultStr != '':
            flag = GameResult(GameResultStr)
