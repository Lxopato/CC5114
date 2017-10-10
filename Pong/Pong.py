import pygame
import random


FPS = 60

#Window Size
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 480

#Paddle Size
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60

#Ball Size
BALL_WIDTH = 10
BALL_HEIGHT = 10

#Distance from window's edge
PADDLE_BUFFERX = 10
PADDLE_BUFFERY = 40

#Speed of paddle and ball
PADDLE_SPEED = 2
BALL_X_SPEED = 3
BALL_Y_SPEED = 3

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
RED = (255, 0 , 0)

#Display text in window
pygame.init()
TITLE_TEXT = pygame.font.SysFont("monospace", 32)
SCORE_TEXT = pygame.font.SysFont("monospace", 16)

#Window
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))


def drawBall(BallXPos, BallYPos):
    ball = pygame.Rect(BallXPos, BallYPos, BALL_WIDTH, BALL_HEIGHT)
    pygame.draw.rect(screen, WHITE, ball)


def updateBallPos(PaddleYPos, OpponentYPos, BallXPos, BallYPos, BallXDir, BallYDir):
    BallXPos += BallXDir * BALL_X_SPEED
    BallYPos += BallYDir * BALL_Y_SPEED
    score = 0

    if (BallXPos <= PADDLE_BUFFERX + PADDLE_WIDTH and PaddleYPos <= BallYPos + BALL_HEIGHT and  PaddleYPos + PADDLE_HEIGHT >= BallYPos - BALL_HEIGHT ):
        BallXDir = 1
    elif (BallXPos <= 0):
        BallXDir = 1
        score = -1
        return [score, PaddleYPos, OpponentYPos, BallXPos, BallYPos, BallXDir, BallYDir]

    if (BallXPos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFERX and OpponentYPos <= BallYPos + BALL_HEIGHT and OpponentYPos + PADDLE_HEIGHT >= BallYPos -BALL_HEIGHT):
        BallXDir = -1
    elif(BallXPos >= WINDOW_WIDTH - BALL_WIDTH):
        BallXDir = -1
        score = 1
        return [score, PaddleYPos, OpponentYPos, BallXPos, BallYPos, BallXDir, BallYDir]

    if (BallYPos <= PADDLE_BUFFERY):
        BallYPos = PADDLE_BUFFERY
        BallYDir = 1
    elif (BallYPos > WINDOW_HEIGHT - BALL_HEIGHT - PADDLE_BUFFERY):
        BallYPos = WINDOW_HEIGHT - BALL_HEIGHT - PADDLE_BUFFERY
        BallYDir = -1

    return [score, PaddleYPos, OpponentYPos, BallXPos, BallYPos, BallXDir, BallYDir]


def drawPaddle(PaddleYPos):
    paddle = pygame.Rect(PADDLE_BUFFERX, PaddleYPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle)


def updatePaddle(action, PaddleYPos):
    if (action[1] == 1):
        PaddleYPos -= PADDLE_SPEED

    if (action[2] ==1):
        PaddleYPos += PADDLE_SPEED

    if (PaddleYPos < PADDLE_BUFFERY):
        PaddleYPos = PADDLE_BUFFERY

    if (PaddleYPos > WINDOW_HEIGHT - PADDLE_HEIGHT - PADDLE_BUFFERY):
        PaddleYPos = WINDOW_HEIGHT - PADDLE_HEIGHT - PADDLE_BUFFERY

    return PaddleYPos


def drawOpponent(OpponentYPos):
    paddle = pygame.Rect(WINDOW_WIDTH- PADDLE_BUFFERX -PADDLE_WIDTH, OpponentYPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle)


def updateOpponent(OpponentYPos, BallYPos):

    if (OpponentYPos + PADDLE_HEIGHT/2 < BallYPos + BALL_HEIGHT/2):
        OpponentYPos += PADDLE_SPEED

    if (OpponentYPos + PADDLE_HEIGHT/2 > BallYPos + BALL_HEIGHT/2):
        OpponentYPos -= PADDLE_SPEED

    if (OpponentYPos < PADDLE_BUFFERY):
        OpponentYPos = PADDLE_BUFFERY

    if (OpponentYPos > WINDOW_HEIGHT - PADDLE_HEIGHT - PADDLE_BUFFERY):
        OpponentYPos = WINDOW_HEIGHT - PADDLE_HEIGHT - PADDLE_BUFFERY

    return OpponentYPos
def drawText():
    top = pygame.Rect(0, 0, WINDOW_WIDTH, 40)
    pygame.draw.rect(screen, RED, top)

    bottom = pygame.Rect(0, 440, WINDOW_WIDTH, 40)
    pygame.draw.rect(screen, RED, bottom)

class Pong:
    def __init__(self):
        self.delta =0
        self.paddleYPos = WINDOW_HEIGHT/2 - PADDLE_HEIGHT/2
        self.opponentYPos = WINDOW_HEIGHT/2 - PADDLE_HEIGHT/2
        self.ballXPos = WINDOW_WIDTH/2 - BALL_WIDTH/2
        self.ballYPos = random.randint(0, 4)*(WINDOW_HEIGHT-BALL_HEIGHT)/4
        self.ballXDir = 1
        self.ballYDir = 1
        self.randomDir()

    def randomDir(self):
        num = random.randint(0, 3)
        if (num == 0):
            self.ballXDir = 1
            self.ballYDir = 1
        elif (num == 1):
            self.ballXDir = -1
            self.ballYDir = 1
        elif (num == 2):
            self.ballXDir = 1
            self.ballYDir = -1
        elif (num == 3):
            self.ballXDir = -1
            self.ballYDir = -1

    def startGame(self):
        pygame.event.pump()
        screen.fill(BLACK)

        drawPaddle(self.paddleYPos)
        drawOpponent(self.opponentYPos)
        drawBall(self.ballXPos, self.ballYPos)
        drawText()
        data = pygame.surfarray.array3d(pygame.display.get_surface())

        pygame.display.flip()

        return data

    def getFrameData(self, action):
        pygame.event.pump()
        screen.fill(BLACK)

        self.paddleYPos = updatePaddle(action, self.paddleYPos)
        drawPaddle(self.paddleYPos)

        self.opponentYPos = updateOpponent(self.opponentYPos, self.ballYPos)
        drawOpponent(self.opponentYPos)

        [score, self.paddleYPos, self.opponentYPos, self.ballXPos, self.ballYPos, self.ballXDir, self.ballYDir] = updateBallPos(self.paddleYPos, self.opponentYPos , self.ballXPos , self.ballYPos, self.ballXDir, self.ballYDir)

        drawBall(self.ballXPos, self.ballYPos)
        drawText()

        data = pygame.surfarray.array3d(pygame.display.get_surface())

        pygame.display.flip()
        scoretext = SCORE_TEXT.render("Delta is {0}".format(self.delta), 1, WHITE)
        screen.blit(scoretext, (5, 460))

        title = TITLE_TEXT.render("NEURAL PONG", 1, WHITE)
        screen.blit(title, (5, 10))
        self.delta += score

        return [score, data]
