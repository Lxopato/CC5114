import pygame
import random

FPS = 30

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
BALL_Y_SPEED = 2

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
RED = (255, 0 , 0)

#Display text in window
pygame.init()
TITLE_TEXT = pygame.font.SysFont("monospace", 32, bold=True)

#Window
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

#ARRAY FOR DATA
DATA = []


def drawBall(ballXPos, ballYPos):
    ball = pygame.Rect(ballXPos, ballYPos, BALL_WIDTH, BALL_HEIGHT)
    pygame.draw.rect(screen, WHITE, ball)


def updateBallPos(PaddleYPos, OpponentYPos, BallXPos, BallYPos, BallXDir, BallYDir):
    BallXPos += BallXDir * BALL_X_SPEED
    BallYPos += BallYDir * BALL_Y_SPEED
    reset = False

    if (BallXPos <= PADDLE_BUFFERX + PADDLE_WIDTH and PaddleYPos <= BallYPos + BALL_HEIGHT and  PaddleYPos + PADDLE_HEIGHT >= BallYPos - BALL_HEIGHT ):
        BallXDir = 1
    elif (BallXPos <= 0):
        BallXDir = 1
        reset = True
        return [reset, PaddleYPos, OpponentYPos, BallXPos, BallYPos, BallXDir, BallYDir]

    if (BallXPos >= WINDOW_WIDTH - PADDLE_WIDTH - PADDLE_BUFFERX and OpponentYPos <= BallYPos + BALL_HEIGHT and OpponentYPos + PADDLE_HEIGHT >= BallYPos -BALL_HEIGHT):
        BallXDir = -1
    elif(BallXPos >= WINDOW_WIDTH - BALL_WIDTH):
        BallXDir = -1
        reset = True
        return [reset, PaddleYPos, OpponentYPos, BallXPos, BallYPos, BallXDir, BallYDir]

    if (BallYPos <= PADDLE_BUFFERY):
        BallYPos = PADDLE_BUFFERY
        BallYDir = 1
    elif (BallYPos > WINDOW_HEIGHT - BALL_HEIGHT - PADDLE_BUFFERY):
        BallYPos = WINDOW_HEIGHT - BALL_HEIGHT - PADDLE_BUFFERY
        BallYDir = -1

    return [reset, PaddleYPos, OpponentYPos, BallXPos, BallYPos, BallXDir, BallYDir]


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
    mov = [0, 0, 0]
    if (OpponentYPos + PADDLE_HEIGHT/2 < BallYPos + BALL_HEIGHT/2):
        OpponentYPos += PADDLE_SPEED
        mov = [0, 1, 0]

    if (OpponentYPos + PADDLE_HEIGHT/2 > BallYPos + BALL_HEIGHT/2):
        OpponentYPos -= PADDLE_SPEED
        mov = [0, 0, 1]

    if (OpponentYPos < PADDLE_BUFFERY):
        OpponentYPos = PADDLE_BUFFERY

    if (OpponentYPos > WINDOW_HEIGHT - PADDLE_HEIGHT - PADDLE_BUFFERY):
        OpponentYPos = WINDOW_HEIGHT - PADDLE_HEIGHT - PADDLE_BUFFERY

    return OpponentYPos, mov


def drawText():
    top = pygame.Rect(0, 0, WINDOW_WIDTH, 40)
    pygame.draw.rect(screen, RED, top)
    title = TITLE_TEXT.render("NEURAL PONG", 1, WHITE)
    screen.blit(title, (135, 5))

    bottom = pygame.Rect(0, 440, WINDOW_WIDTH, 40)
    pygame.draw.rect(screen, RED, bottom)


class Pong:
    def __init__(self):
        self.paddleYPos = WINDOW_HEIGHT/2 - PADDLE_HEIGHT/2
        self.opponentYPos = WINDOW_HEIGHT/2 - PADDLE_HEIGHT/2
        self.ballXPos = WINDOW_WIDTH/2 - BALL_WIDTH/2
        self.ballYPos = random.randint(0, 4)*(WINDOW_HEIGHT-BALL_HEIGHT)/4
        self.ballXDir = 1
        self.ballYDir = 1
        self.randomDir()

    def randomDir(self):
        num = random.randint(0, 3)
        if num == 0:
            self.ballXDir = 1
            self.ballYDir = 1
        elif num == 1:
            self.ballXDir = -1
            self.ballYDir = 1
        elif num == 2:
            self.ballXDir = 1
            self.ballYDir = -1
        elif num == 3:
            self.ballXDir = -1
            self.ballYDir = -1

    def restart_game(self):
        print("RESTART!!!")
        self.paddleYPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        self.opponentYPos = WINDOW_HEIGHT / 2 - PADDLE_HEIGHT / 2
        self.ballXPos = WINDOW_WIDTH / 2 - BALL_WIDTH / 2
        self.ballYPos = random.randint(0, 4) * (WINDOW_HEIGHT - BALL_HEIGHT) / 4
        self.ballXDir = 1
        self.ballYDir = 1
        self.randomDir()
        del DATA[:]

    def start_game(self):
        print("START!!!")
        pygame.event.pump()
        screen.fill(BLACK)
        drawPaddle(self.paddleYPos)
        drawOpponent(self.opponentYPos)
        drawBall(self.ballXPos, self.ballYPos)
        drawText()
        pygame.display.flip()

        return [self.ballXPos, self.ballYPos, self.ballXDir, self.ballYDir, self.paddleYPos]

    def play(self, action):
        pygame.event.pump()
        screen.fill(BLACK)

        self.paddleYPos = updatePaddle(action, self.paddleYPos)
        drawPaddle(self.paddleYPos)

        self.opponentYPos, expected = updateOpponent(self.opponentYPos, self.ballYPos)
        drawOpponent(self.opponentYPos)

        [reset, self.paddleYPos, self.opponentYPos, self.ballXPos, self.ballYPos, self.ballXDir, self.ballYDir] = updateBallPos(self.paddleYPos, self.opponentYPos, self.ballXPos, self.ballYPos, self.ballXDir, self.ballYDir)
        drawBall(self.ballXPos, self.ballYPos)

        drawText()
        pygame.display.flip()

        DATA.append([self.ballXPos, self.ballYPos, self.ballXDir, self.ballYDir, self.paddleYPos, expected])

        if reset:
            return DATA, reset

        return [self.ballXPos, self.ballYPos, self.ballXDir, self.ballYDir, self.paddleYPos], reset
