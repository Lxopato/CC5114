import pygame
import random


FPS = 60

#Window Size
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

#Paddle Size
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80

#Ball Size
BALL_WIDTH = 15
BALL_HEIGHT = 15

#Distance from window's edge
PADDLE_BUFFER = 20

#Speed of paddle and ball
PADDLE_SPEED = 2
BALL_X_SPEED = 3
BALL_Y_SPEED = 2

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)

screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))


def drawBall(BallXPos,BallYPos):
    ball = pygame.rect(BallXPos,BallYPos,BALL_WIDTH,BALL_HEIGHT)
    pygame.draw.rect(screen,WHITE,ball)


def drawPaddle(PaddleYPos):
    paddle = pygame.rect(PADDLE_BUFFER,PaddleYPos,PADDLE_WIDTH,PADDLE_HEIGHT)
    pygame.draw.rect(screen,WHITE,paddle)


def drawOpponent(OpponentYPos):
    paddle = pygame.rect(WINDOW_WIDTH-PADDLE_BUFFER-PADDLE_WIDTH,OpponentYPos,PADDLE_WIDTH,PADDLE_HEIGHT)
    pygame.draw.rect(screen,WHITE,paddle)


def updateBallPos(PaddleYPos,OpponentYPos,BallXPos,BallYPos,BallXDir,BallYDir):
    BallXPos = BallXPos + BallXDir*BALL_X_SPEED
    BallYPos = BallYPos + BallYDir * BALL_Y_SPEED
    score = 0

    if (BallXPos <= PADDLE_BUFFER + PADDLE_WIDTH and PaddleYPos <= BallYPos + BALL_HEIGHT and  PaddleYPos + PADDLE_HEIGHT >= BallYPos - BALL_HEIGHT ):
        BallXDir = 1
    elif (BallXPos <= 0):
        BallXDir = 1
        score = -1
        return [score, PaddleYPos, OpponentYPos, BallXPos, BallYPos, BallXDir, BallYDir]

    if (BallXPos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFER and OpponentYPos <= BallYPos + BALL_HEIGHT and OpponentYPos + PADDLE_HEIGHT >= BallYPos -BALL_HEIGHT):
        BallXDir = -1
    elif(BallXPos >= WINDOW_WIDTH - BALL_WIDTH):
        BallXDir = -1
        score = 1
        return [score, PaddleYPos, OpponentYPos, BallXPos, BallYPos, BallXDir, BallYDir]

    if (BallYPos <= 0):
        BallYPos = 0
        BallYDir = 1
    elif (BallYPos >WINDOW_HEIGHT - BALL_HEIGHT):
        BallYPos = WINDOW_HEIGHT - BALL_HEIGHT
        BallYDir = -1

    return [score, PaddleYPos, OpponentYPos, BallXPos, BallYPos, BallXDir, BallYDir]
