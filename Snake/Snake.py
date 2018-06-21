# -*- coding:utf-8 -*-

import pygame, sys, random
from pygame.locals import *

pygame.init()
ScreenX = 500
ScreenY = 500
ScreenSize = (ScreenX, ScreenY)
Screen = pygame.display.set_mode(ScreenSize, 0, 32)
pygame.display.set_caption("Ly's Snake Game")
Difficulty = 10

class snake():
    def __init__(self):
        self.Direction = K_RIGHT
        self.Body = []
        self.AddBody()
        self.AddBody()

    def AddBody(self):
        NewAddLeft, NewAddTop = (0, 0)
        if self.Body:
            NewAddLeft, NewAddTop = (self.Body[0].left, self.Body[0].top)
        NewAddBody = pygame.Rect(NewAddLeft, NewAddTop, 20, 20)
        if self.Direction == K_LEFT:
            if NewAddBody.left == 0:
                NewAddBody.left = 480
            else:
                NewAddBody.left -= 20
        elif self.Direction == K_RIGHT:
            if NewAddBody.left == 480:
                NewAddBody.left = 0
            else:
                NewAddBody.left += 20
        elif self.Direction == K_UP:
            if NewAddBody.top == 0:
                NewAddBody.top = 480
            else:
                NewAddBody.top -= 20
        elif self.Direction == K_DOWN:
            if NewAddBody.top == 480:
                NewAddBody.top = 0
            else:
                NewAddBody.top += 20
        self.Body.insert(0, NewAddBody)

    def DelBody(self):
        self.Body.pop()

    def IsDie(self):
        if self.Body[0] in self.Body[1:]:
            return True
        return False

    def Move(self):
        self.AddBody()
        self.DelBody()

    def ChangeDirection(self, Curkey):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if Curkey in LR + UD:
            if (Curkey in LR) and (self.Direction in LR):
                return
            if (Curkey in UD) and (self.Direction in UD):
                return
            self.Direction = Curkey

class food():
    def __init__(self):
        self.Obj = pygame.Rect(-20, 0, 20, 20)

    def Remove(self):
        self.Obj.x = -20

    def SendFood(self):
        if self.Obj.x == -20:
            AllPos = []
            for pos in range(20, ScreenX - 20, 20):
                AllPos.append(pos)
            self.Obj.left = random.choice(AllPos)
            self.Obj.top = random.choice(AllPos)

def GameMain():
    global Difficulty
    FPSClock = pygame.time.Clock()
    Score = 0

    Snake = snake()
    Food = food()

    BackgroungImg = pygame.image.load('BackgroundImg.png').convert()
    DifficultyChoiceImg = pygame.image.load('DCBgImg.png').convert()

    ChoiceHintFont = pygame.font.SysFont('arial', 30)
    ChoiceFont = pygame.font.SysFont('arial', 180)
    # DifficultyChoice
    while True:
        IsChoice = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    IsChoice = True
                    break
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    Difficulty = Difficulty + 1
                elif event.key == K_DOWN:
                    if Difficulty > 1:
                        Difficulty = Difficulty - 1
        if IsChoice:
            break

        Screen.blit(DifficultyChoiceImg, (0, 0))
        ChoiceHintSurface = ChoiceHintFont.render('Please choose a difficulty by direction key:', True, (0, 0, 0))
        Screen.blit(ChoiceHintSurface, (30, 110))
        ChoiceSurface = ChoiceFont.render(str(Difficulty), True, (0, 0, 0))
        Screen.blit(ChoiceSurface, (150, 150))
        EntranceHintSurface = ChoiceHintFont.render('Press Space to enter the game', True, (0, 0, 0))
        Screen.blit(EntranceHintSurface, (70, 350))
        pygame.display.update()

    ScoreFont = pygame.font.SysFont('arial', 30)
    while True:     # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                Snake.ChangeDirection(event.key)

        Screen.blit(BackgroungImg, (0, 0))
        pygame.draw.rect(Screen, (0, 0, 0), Food.Obj, 0)
        Snake.Move()

        for rect in Snake.Body:
            pygame.draw.rect(Screen, (0, 0, 0), rect, 0)

        if Snake.IsDie():
            return Score

        if Food.Obj == Snake.Body[0]:
            Score += Difficulty
            Food.Remove()
            Snake.AddBody()

        Food.SendFood()

        ScoreSurface = ScoreFont.render(str(Score), True, (0, 0, 0))
        Screen.blit(ScoreSurface, (0, 0))

        pygame.draw.rect(Screen, (0, 0, 0), Food.Obj, 0)

        pygame.display.update()
        FPSClock.tick(Difficulty)

def GameResult(Score):
    GameResultBackgroundImg = pygame.image.load('GRBgImg.png').convert()
    ScoreHintFont = pygame.font.SysFont('arial', 35)
    ScoreFont = pygame.font.SysFont('arial', 180)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True

        Screen.blit(GameResultBackgroundImg, (0, 0))
        ChoiceHintSurface = ScoreHintFont.render('Your Score is:', True, (0, 0, 0))
        Screen.blit(ChoiceHintSurface, (40, 110))
        ChoiceSurface = ScoreFont.render(str(Score), True, (0, 0, 0))
        Screen.blit(ChoiceSurface, (150, 150))
        EntranceHintSurface = ScoreHintFont.render('Press Space to restart the game', True, (0, 0, 0))
        Screen.blit(EntranceHintSurface, (50, 350))
        pygame.display.update()

if __name__ == '__main__':
    flag = True
    while flag:
        Score = GameMain()
        flag = GameResult(Score)