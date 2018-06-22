# -*- coding:utf-8 -*-

import pygame, sys, random, copy
from pygame.locals import *

pygame.init()

CubeWidth = 40
CubeHeight = 40
Column = 10
Row = 20
ScreenWidth = CubeWidth * (Column + 5)
ScreenHeight = CubeHeight * Row
ScreenSize = (ScreenWidth, ScreenHeight)
Screen = pygame.display.set_mode(ScreenSize, 0, 32)
pygame.display.set_caption("Ly's Tetris")

pygame.mixer.music.load('BackgroundMusic.ogg')
pygame.mixer.music.play(-1, 0.0)
ClickMusic = pygame.mixer.Sound('ClickMusic.wav')
ExplodeMusic = pygame.mixer.Sound('Explode.wav')
BackgroundImg = pygame.image.load('BackgroundImg.png').convert()
PreImg = pygame.image.load('PreImg.png').convert()
PStartImg = pygame.image.load('PStartImg.png').convert()
ResultPreImg = pygame.image.load('GameResultPreBgImg.png').convert()
RestartImg = pygame.image.load('GameResultRestBgImg.png').convert()
ScoreHintFont = pygame.font.SysFont('arial', 50)
ScoreFont = pygame.font.SysFont('arial', 40)
ResultFont = pygame.font.SysFont('arial', 200)

Aquamarine = (127, 255, 212)
LightGoldenrod = (255, 236, 139)
IndianRed = (255, 106, 106)
DarkOrchid = (153, 50, 204)
RoyalBlue = (72, 118, 255)
DarkOrange = (255, 165, 0)
Turquoise = (0, 245, 255)

IsRect = []

FPSClock = pygame.time.Clock()

class I():
    def __init__(self):
        self.Statu = ''
        self.Color = Aquamarine
        self.Body = []
        x = random.randint(1, 2)
        if x == 1:
            self.Statu = 'upright'
            for i in range(4):
                InitBody = pygame.Rect(160, i * 40, 40, 40)
                self.Body.append(InitBody)
        elif x == 2:
            self.Statu = 'horizon'
            for i in range(4):
                InitBody = pygame.Rect(120 + i * 40, 0, 40, 40)
                self.Body.append(InitBody)

    def Fall(self):
        for rect in self.Body:
            rect.top += 40

    def IsFalled(self):
        for rect in self.Body:
            if rect.top == 760:
                return True
            if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                return True

    def Move(self, Curkey):
        CanMoveFlag = True
        if Curkey == K_UP:
            self.Rotate()
        elif Curkey == K_LEFT:
            for rect in self.Body:
                if rect.left == 0:
                    CanMoveFlag = not CanMoveFlag
                    break
                elif IsRect[int(rect.top / 40) + 1][int(rect.left / 40) - 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left -= 40
        elif Curkey == K_RIGHT:
            for rect in self.Body:
                if rect.left == 360:
                    CanMoveFlag = not CanMoveFlag
                    break
                if IsRect[int(rect.top / 40) + 1][int(rect.left / 40) + 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left += 40

    def Rotate(self):
        if self.Statu == 'upright':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left -= 40
            TempRotate[0].top += 40
            TempRotate[2].left += 40
            TempRotate[2].top -= 40
            TempRotate[3].left += 40 * 2
            TempRotate[3].top -= 40 * 2
            IsRotate = True
            if TempRotate[0].left < 0:
                IsRotate = False
            if TempRotate[3].left > 360:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'horizon'
        else:
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left += 40
            TempRotate[0].top -= 40
            TempRotate[2].left -= 40
            TempRotate[2].top += 40
            TempRotate[3].left -= 40 * 2
            TempRotate[3].top += 40 * 2
            IsRotate = True
            if TempRotate[0].top < 0:
                IsRotate = False
            if TempRotate[3].top > 760:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'upright'

class O():
    def __init__(self):
        self.Color = LightGoldenrod
        self.Body = []
        for i in range(2):
            InitBody = pygame.Rect(160, i * 40, 40, 40)
            self.Body.append(InitBody)
        for i in range(2):
            InitBody = pygame.Rect(200, i * 40, 40, 40)
            self.Body.append(InitBody)

    def Fall(self):
        for rect in self.Body:
            rect.top += 40

    def IsFalled(self):
        for rect in self.Body:
            if rect.top == 760:
                return True
            if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                return True

    def Move(self, Curkey):
        CanMoveFlag = True
        if Curkey == K_UP:
            self.Rotate()
        elif Curkey == K_LEFT:
            for rect in self.Body:
                if rect.left == 0:
                    CanMoveFlag = not CanMoveFlag
                    break
                elif IsRect[int(rect.top / 40) + 1][int(rect.left / 40) - 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left -= 40
        elif Curkey == K_RIGHT:
            for rect in self.Body:
                if rect.left == 360:
                    CanMoveFlag = not CanMoveFlag
                    break
                if IsRect[int(rect.top / 40) + 1][int(rect.left / 40) + 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left += 40

    def Rotate(self):
        pass

class T():
    def __init__(self):
        self.Statu = ''
        self.Color = IndianRed
        self.Body = []
        x = random.randint(1, 4)
        if x == 1:
            self.Statu = 'up'
            self.Body.append(pygame.Rect(200, 0, 40, 40))
            for i in range(3):
                self.Body.append(pygame.Rect(160 + i * 40, 40, 40, 40))
        elif x == 2:
            self.Statu = 'left'
            self.Body.append(pygame.Rect(160, 40, 40, 40))
            for i in range(3):
                self.Body.append(pygame.Rect(200, 80 - i * 40, 40, 40))
        elif x == 3:
            self.Statu = 'down'
            self.Body.append(pygame.Rect(200, 80, 40, 40))
            for i in range(2, -1, -1):
                self.Body.append(pygame.Rect(160 + i * 40, 40, 40, 40))
        elif x == 4:
            self.Statu = 'right'
            self.Body.append(pygame.Rect(240, 40, 40, 40))
            for i in range(3):
                self.Body.append(pygame.Rect(200, i * 40, 40, 40))

    def Fall(self):
        for rect in self.Body:
            rect.top += 40

    def IsFalled(self):
        for rect in self.Body:
            if rect.top == 760:
                return True
            if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                return True

    def Move(self, Curkey):
        CanMoveFlag = True
        if Curkey == K_UP:
            self.Rotate()
        elif Curkey == K_LEFT:
            for rect in self.Body:
                if rect.left == 0:
                    CanMoveFlag = not CanMoveFlag
                    break
                elif IsRect[int(rect.top / 40) + 1][int(rect.left / 40) - 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left -= 40
        elif Curkey == K_RIGHT:
            for rect in self.Body:
                if rect.left == 360:
                    CanMoveFlag = not CanMoveFlag
                    break
                if IsRect[int(rect.top / 40) + 1][int(rect.left / 40) + 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left += 40

    def Rotate(self):
        if self.Statu == 'up':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left -= 40
            TempRotate[0].top += 40
            TempRotate[1].left += 40
            TempRotate[1].top += 40
            TempRotate[3].left -= 40
            TempRotate[3].top -= 40
            IsRotate = True
            if TempRotate[1].top > 760:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'left'
        elif self.Statu == 'left':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left += 40
            TempRotate[0].top += 40
            TempRotate[1].left += 40
            TempRotate[1].top -= 40
            TempRotate[3].left -= 40
            TempRotate[3].top += 40
            IsRotate = True
            if TempRotate[1].left > 360:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'down'
        elif self.Statu == 'down':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left += 40
            TempRotate[0].top -= 40
            TempRotate[1].left -= 40
            TempRotate[1].top -= 40
            TempRotate[3].left += 40
            TempRotate[3].top += 40
            IsRotate = True
            if TempRotate[1].top < 0:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'right'
        elif self.Statu == 'right':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left -= 40
            TempRotate[0].top -= 40
            TempRotate[1].left -= 40
            TempRotate[1].top += 40
            TempRotate[3].left += 40
            TempRotate[3].top -= 40
            IsRotate = True
            if TempRotate[1].top < 0:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'up'

class Z():
    def __init__(self):
        self.Statu = ''
        self.Color = DarkOrchid
        self.Body = []
        x = random.randint(1, 2)
        if x == 1:
            self.Statu = 'horizon'
            for i in range(2):
                self.Body.append(pygame.Rect(120 + i * 40, 0, 40, 40))
            for i in range(2):
                self.Body.append(pygame.Rect(160 + i * 40, 40, 40, 40))
        elif x == 2:
            self.Statu = 'upright'
            for i in range(2):
                self.Body.append(pygame.Rect(200, i * 40, 40, 40))
            for i in range(2):
                self.Body.append(pygame.Rect(160, 40 + i * 40, 40, 40))

    def Fall(self):
        for rect in self.Body:
            rect.top += 40

    def IsFalled(self):
        for rect in self.Body:
            if rect.top == 760:
                return True
            if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                return True

    def Move(self, Curkey):
        CanMoveFlag = True
        if Curkey == K_UP:
            self.Rotate()
        elif Curkey == K_LEFT:
            for rect in self.Body:
                if rect.left == 0:
                    CanMoveFlag = not CanMoveFlag
                    break
                elif IsRect[int(rect.top / 40) + 1][int(rect.left / 40) - 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left -= 40
        elif Curkey == K_RIGHT:
            for rect in self.Body:
                if rect.left == 360:
                    CanMoveFlag = not CanMoveFlag
                    break
                if IsRect[int(rect.top / 40) + 1][int(rect.left / 40) + 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left += 40

    def Rotate(self):
        if self.Statu == 'horizon':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left += 40 * 2
            TempRotate[1].left += 40
            TempRotate[1].top += 40
            TempRotate[3].left -= 40
            TempRotate[3].top += 40
            IsRotate = True
            if TempRotate[3].top > 760:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'upright'
        elif self.Statu == 'upright':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left -= 40 * 2
            TempRotate[1].left -= 40
            TempRotate[1].top -= 40
            TempRotate[3].left += 40
            TempRotate[3].top -= 40
            IsRotate = True
            if TempRotate[0].left < 0:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'horizon'

class S():
    def __init__(self):
        self.Statu = ''
        self.Color = DarkOrchid
        self.Body = []
        x = random.randint(1, 2)
        if x == 1:
            self.Statu = 'horizon'
            for i in range(2):
                self.Body.append(pygame.Rect(200 - i * 40, 0, 40, 40))
            for i in range(2):
                self.Body.append(pygame.Rect(160 - i * 40, 40, 40, 40))
        elif x == 2:
            self.Statu = 'upright'
            for i in range(2):
                self.Body.append(pygame.Rect(120, i * 40, 40, 40))
            for i in range(2):
                self.Body.append(pygame.Rect(160, 40 + i * 40, 40, 40))

    def Fall(self):
        for rect in self.Body:
            rect.top += 40

    def IsFalled(self):
        for rect in self.Body:
            if rect.top == 760:
                return True
            if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                return True

    def Move(self, Curkey):
        CanMoveFlag = True
        if Curkey == K_UP:
            self.Rotate()
        elif Curkey == K_LEFT:
            for rect in self.Body:
                if rect.left == 0:
                    CanMoveFlag = not CanMoveFlag
                    break
                elif IsRect[int(rect.top / 40) + 1][int(rect.left / 40) - 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left -= 40
        elif Curkey == K_RIGHT:
            for rect in self.Body:
                if rect.left == 360:
                    CanMoveFlag = not CanMoveFlag
                    break
                if IsRect[int(rect.top / 40) + 1][int(rect.left / 40) + 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left += 40

    def Rotate(self):
        if self.Statu == 'horizon':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left -= 40 * 2
            TempRotate[1].left -= 40
            TempRotate[1].top += 40
            TempRotate[3].left += 40
            TempRotate[3].top += 40
            IsRotate = True
            if TempRotate[3].top > 760:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'upright'
        elif self.Statu == 'upright':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left += 40 * 2
            TempRotate[1].left += 40
            TempRotate[1].top -= 40
            TempRotate[3].left -= 40
            TempRotate[3].top -= 40
            IsRotate = True
            if TempRotate[0].left > 360:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'horizon'

class L():
    def __init__(self):
        self.Statu = ''
        self.Color = DarkOrange
        self.Body = []
        x = random.randint(1, 4)
        if x == 1:
            self.Statu = 'horizonright'
            self.Body.append(pygame.Rect(120, 0, 40, 40))
            for i in range(3):
                self.Body.append(pygame.Rect(120 + i * 40, 40, 40, 40))
        elif x == 2:
            self.Statu = 'uprightup'
            self.Body.append(pygame.Rect(120, 80, 40, 40))
            for i in range(3):
                self.Body.append(pygame.Rect(160, 80 - i * 40, 40, 40))
        elif x == 3:
            self.Statu = 'horizonleft'
            self.Body.append(pygame.Rect(200, 40, 40, 40))
            for i in range(3):
                self.Body.append(pygame.Rect(200 - i * 40, 0, 40, 40))
        elif x == 4:
            self.Statu = 'uprightdown'
            self.Body.append(pygame.Rect(160, 0, 40, 40))
            for i in range(3):
                self.Body.append(pygame.Rect(120, i * 40, 40, 40))

    def Fall(self):
        for rect in self.Body:
            rect.top += 40

    def IsFalled(self):
        for rect in self.Body:
            if rect.top == 760:
                return True
            if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                return True

    def Move(self, Curkey):
        CanMoveFlag = True
        if Curkey == K_UP:
            self.Rotate()
        elif Curkey == K_LEFT:
            for rect in self.Body:
                if rect.left == 0:
                    CanMoveFlag = not CanMoveFlag
                    break
                elif IsRect[int(rect.top / 40) + 1][int(rect.left / 40) - 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left -= 40
        elif Curkey == K_RIGHT:
            for rect in self.Body:
                if rect.left == 360:
                    CanMoveFlag = not CanMoveFlag
                    break
                if IsRect[int(rect.top / 40) + 1][int(rect.left / 40) + 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left += 40

    def Rotate(self):
        if self.Statu == 'horizonright':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left -= 40
            TempRotate[0].top += 40
            TempRotate[2].left -= 40
            TempRotate[2].top -= 40
            TempRotate[3].left -= 40 * 2
            TempRotate[3].top -= 40 * 2
            IsRotate = True
            if TempRotate[0].left < 0:
                IsRotate = False
            if TempRotate[3].top < 0:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'uprightup'
        elif self.Statu == 'uprightup':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left += 40
            TempRotate[0].top += 40
            TempRotate[2].left -= 40
            TempRotate[2].top += 40
            TempRotate[3].left -= 40 * 2
            TempRotate[3].top += 40 * 2
            IsRotate = True
            if TempRotate[3].left < 0:
                IsRotate = False
            if TempRotate[0].top > 760:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'horizonleft'
        elif self.Statu == 'horizonleft':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left += 40
            TempRotate[0].top -= 40
            TempRotate[2].left += 40
            TempRotate[2].top += 40
            TempRotate[3].left += 40 * 2
            TempRotate[3].top += 40 * 2
            IsRotate = True
            if TempRotate[0].left > 360:
                IsRotate = False
            if TempRotate[3].top > 760:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'uprightdown'
        elif self.Statu == 'uprightdown':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left -= 40
            TempRotate[0].top -= 40
            TempRotate[2].left += 40
            TempRotate[2].top -= 40
            TempRotate[3].left += 40 * 2
            TempRotate[3].top -= 40 * 2
            IsRotate = True
            if TempRotate[0].top < 0:
                IsRotate = False
            if TempRotate[3].left > 360:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'horizonright'

class J():
    def __init__(self):
        self.Statu = ''
        self.Color = Turquoise
        self.Body = []
        x = random.randint(1, 4)
        if x == 1:
            self.Statu = 'horizonleft'
            self.Body.append(pygame.Rect(200, 0, 40, 40))
            for i in range(3):
                self.Body.append(pygame.Rect(200 - i * 40, 40, 40, 40))
        elif x == 2:
            self.Statu = 'uprightup'
            self.Body.append(pygame.Rect(240, 80, 40, 40))
            for i in range(3):
                self.Body.append(pygame.Rect(200, 80 - i * 40, 40, 40))
        elif x == 3:
            self.Statu = 'horizonright'
            self.Body.append(pygame.Rect(120, 40, 40, 40))
            for i in range(3):
                self.Body.append(pygame.Rect(120 + i * 40, 0, 40, 40))
        elif x == 4:
            self.Statu = 'uprightdown'
            self.Body.append(pygame.Rect(120, 0, 40, 40))
            for i in range(3):
                self.Body.append(pygame.Rect(160, i * 40, 40, 40))

    def Fall(self):
        for rect in self.Body:
            rect.top += 40

    def IsFalled(self):
        for rect in self.Body:
            if rect.top == 760:
                return True
            if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                return True

    def Move(self, Curkey):
        CanMoveFlag = True
        if Curkey == K_UP:
            self.Rotate()
        elif Curkey == K_LEFT:
            for rect in self.Body:
                if rect.left == 0:
                    CanMoveFlag = not CanMoveFlag
                    break
                elif IsRect[int(rect.top / 40) + 1][int(rect.left / 40) - 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left -= 40
        elif Curkey == K_RIGHT:
            for rect in self.Body:
                if rect.left == 360:
                    CanMoveFlag = not CanMoveFlag
                    break
                if IsRect[int(rect.top / 40) + 1][int(rect.left / 40) + 1]:
                    CanMoveFlag = not CanMoveFlag
                    break
            if CanMoveFlag:
                for rect in self.Body:
                    rect.left += 40

    def Rotate(self):
        if self.Statu == 'horizonleft':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left += 40
            TempRotate[0].top += 40
            TempRotate[2].left += 40
            TempRotate[2].top -= 40
            TempRotate[3].left += 40 * 2
            TempRotate[3].top -= 40 * 2
            IsRotate = True
            if TempRotate[0].left > 360:
                IsRotate = False
            if TempRotate[3].top < 0:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'uprightup'
        elif self.Statu == 'uprightup':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left -= 40
            TempRotate[0].top += 40
            TempRotate[2].left += 40
            TempRotate[2].top += 40
            TempRotate[3].left += 40 * 2
            TempRotate[3].top += 40 * 2
            IsRotate = True
            if TempRotate[3].left > 360:
                IsRotate = False
            if TempRotate[0].top > 760:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'horizonright'
        elif self.Statu == 'horizonright':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left -= 40
            TempRotate[0].top -= 40
            TempRotate[2].left -= 40
            TempRotate[2].top += 40
            TempRotate[3].left -= 40 * 2
            TempRotate[3].top += 40 * 2
            IsRotate = True
            if TempRotate[0].left < 0:
                IsRotate = False
            if TempRotate[3].top > 760:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'uprightdown'
        elif self.Statu == 'uprightdown':
            TempRotate = copy.deepcopy(self.Body)
            TempRotate[0].left += 40
            TempRotate[0].top -= 40
            TempRotate[2].left -= 40
            TempRotate[2].top -= 40
            TempRotate[3].left -= 40 * 2
            TempRotate[3].top -= 40 * 2
            IsRotate = True
            if TempRotate[0].top < 0:
                IsRotate = False
            if TempRotate[3].left < 0:
                IsRotate = False
            if IsRotate:
                for rect in TempRotate:
                    if IsRect[int(rect.top / 40) + 1][int(rect.left / 40)]:
                        IsRotate = False
                        break
            if IsRotate:
                self.Body = copy.deepcopy(TempRotate)
                self.Statu = 'horizonleft'

def ShapeChoose():
    ShapeChoose = random.randint(1, 7)
    if ShapeChoose == 1:
        return I()
    elif ShapeChoose == 2:
        return O()
    elif ShapeChoose == 3:
        return T()
    elif ShapeChoose == 4:
        return Z()
    elif ShapeChoose == 5:
        return S()
    elif ShapeChoose == 6:
        return L()
    elif ShapeChoose == 7:
        return J()

def GameMain():
    global IsRect
    for row in range(21):
        TempRowIsRect = []
        for column in range(11):
            TempRowIsRect.append(False)
        IsRect.append(TempRowIsRect)

    PreBackgroundImg = PreImg
    while True:
        StarFalg = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                ClickMusic.play()
                if event.key == K_SPACE:
                    PreBackgroundImg = PStartImg
            if event.type == KEYUP:
                ClickMusic.play()
                if event.key == K_SPACE:
                    StarFalg = True
        if StarFalg:
            break

        Screen.blit(PreBackgroundImg, (0, 0))
        pygame.display.update()

    falling = ShapeChoose()

    GameOver = False
    Score = 0
    FallSpeed = 4

    while True:     # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    FallSpeed = 15
                else:
                    falling.Move(event.key)
            if event.type == KEYUP:
                if event.key == K_DOWN:
                    FallSpeed = 4

        Screen.blit(BackgroundImg, (0, 0))

        for row in range(20):
            for column in range(10):
                if IsRect[row][column]:
                    pygame.draw.rect(Screen, IsRect[row][column][1], IsRect[row][column][0], 0)

        falling.Fall()

        for rect in falling.Body:
            pygame.draw.rect(Screen, falling.Color, rect, 0)

        if falling.IsFalled():
            for rect in falling.Body:
                Info = []
                Info.append(rect)
                Info.append(falling.Color)
                IsRect[int(rect.top / 40)][int(rect.left / 40)] = Info
            falling = ShapeChoose()

        for IsOver in IsRect[1]:
            if IsOver:
                GameOver = True
                break
        if GameOver:
            IsRect = []
            return Score

        for CheckRow in range(19, 0, -1):
            CheckFlag = True
            for CheckC in range(10):
                if IsRect[CheckRow][CheckC]:
                    pass
                else:
                    CheckFlag = False
            if CheckFlag:
                ExplodeMusic.play()
                Score += 10
                for ChangeRow in range(CheckRow, 0, -1):
                    for ChangeC in range(10):
                        if IsRect[ChangeRow - 1][ChangeC]:
                            IsRect[ChangeRow - 1][ChangeC][0].top += 40
                    IsRect[ChangeRow] = IsRect[ChangeRow - 1]

        ScoreHintSurface = ScoreHintFont.render('Score:', True, (0, 0, 0))
        Screen.blit(ScoreHintSurface, (420, 100))
        ScoreSurface = ScoreFont.render(str(Score), True, (0, 0, 0))
        Screen.blit(ScoreSurface, (480, 180))

        pygame.display.update()
        FPSClock.tick(FallSpeed)

def GameResult(Score):
    ResultImg = ResultPreImg
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                ClickMusic.play()
                if event.key == K_SPACE:
                    ResultImg = RestartImg
            if event.type == KEYUP:
                ClickMusic.play()
                if event.key == K_SPACE:
                    return True
        Screen.blit(ResultImg, (0, 0))
        ScoreSurface = ResultFont.render(str(Score), True, (255, 127, 80))
        if Score < 10:
            Screen.blit(ScoreSurface, (250, 260))
        elif Score < 100:
            Screen.blit(ScoreSurface, (210, 260))
        elif Score < 1000:
            Screen.blit(ScoreSurface, (160, 260))
        pygame.display.update()

if __name__ == '__main__':
    Flag = True
    while Flag:
        Score = GameMain()
        Flag = GameResult(Score)