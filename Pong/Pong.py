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

#Speed of paddle and ball
PADDLE_SPEED = 2
BALL_X_SPEED = 3
BALL_Y_SPEED = 2

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)

screen = pygame.display.set_mode(WINDOW_WIDTH,WINDOW_HEIGHT)

def drawBall(x,y):
    ball = pygame.rect(x,y,BALL_WIDTH,BALL_HEIGHT)
    pygame.draw.rect(screen,WHITE,ball)
