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


def updateBallPos(PaddleYPos,OpponentYPos,BallXPos,BallYPos,BallXDir,BallYDir):
    BallXPos += BallXDir*BALL_X_SPEED
    BallYPos += BallYDir * BALL_Y_SPEED
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


def drawPaddle(PaddleYPos):
    paddle = pygame.rect(PADDLE_BUFFER, PaddleYPos, PADDLE_WIDTH, PADDLE_HEIGHT)
    pygame.draw.rect(screen, WHITE, paddle)


def updatePaddle(action, PaddleYPos):
    if (action[1] == 1):
        PaddleYPos -= PADDLE_SPEED

    if (action[2] ==1):
        PaddleYPos += PADDLE_SPEED

    if (PaddleYPos <0):
        PaddleYPos = 0

    if (PaddleYPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        PaddleYPos = WINDOW_HEIGHT - PADDLE_HEIGHT

    return PaddleYPos


def drawOpponent(OpponentYPos):
    paddle = pygame.rect(WINDOW_WIDTH-PADDLE_BUFFER-PADDLE_WIDTH,OpponentYPos,PADDLE_WIDTH,PADDLE_HEIGHT)
    pygame.draw.rect(screen,WHITE,paddle)


def updateOpponent(OpponentYPos, BallYPos):

    if (OpponentYPos +PADDLE_HEIGHT/2 < BallYPos +BALL_HEIGHT/2):
        OpponentYPos += PADDLE_SPEED

    if (OpponentYPos +PADDLE_HEIGHT/2 > BallYPos +BALL_HEIGHT/2):
        OpponentYPos -= PADDLE_SPEED

    if (OpponentYPos <0):
        OpponentYPos = 0

    if (OpponentYPos > WINDOW_HEIGHT - PADDLE_HEIGHT):
        OpponentYPos = WINDOW_HEIGHT - PADDLE_HEIGHT

    return OpponentYPos

class Pong:
    def __init__(self):
        self.tally =0
        self.paddleYPos = WINDOW_HEIGHT/2 - PADDLE_HEIGHT/2
        self.opponentYPos = WINDOW_HEIGHT/2 - PADDLE_HEIGHT/2
        self.ballXPos = WINDOW_WIDTH/2 - BALL_WIDTH/2
        self.ballYPos = random.randint(0,4)*(WINDOW_HEIGHT-BALL_HEIGHT)/4
        self.ballXDir = 1
        self.ballYDir = 1
        self.randomDir()

    def randomDir(self):
        num = random.randint(0,3)
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

    def getPresentFrame(self):
        pygame.event.pump()
        screen.fill(BLACK)

        drawPaddle(self.paddleYPos)
        drawOpponent(self.opponentYPos)
        drawBall(self.ballXPos,self.ballYPos)

        data = pygame.surfarray.array3d(pygame.display.get_surface())

        pygame.display.flip()

        return data

    def getNextFrame (self, action):
        pygame.event.pump()
        score = 0
        screen.fill(BLACK)

        self.paddleYPos = updatePaddle(action, self.paddleYPos)
        drawPaddle(self.paddleYPos)

        self.opponentYPos = updateOpponent(self.opponentYPos, self.ballYPos)
        drawOpponent(self.opponentYPos)

        [score , self.paddleYPos, self.opponentYPos, self.ballXPos, self.ballYPos, self.ballXDir, self.ballYDir] = updateBallPos(self.paddleYPos, self.opponentYPos , self.ballXPos , self.ballYPos, self.ballXDir, self.ballYDir)

        drawBall(self.ballXPos, self.ballYPos)

        data = pygame.surfarray.array3d(pygame.display.get_surface())

        pygame.display.flip()

        self.tally += score
        print("Tally is " + str(self.tally))
        return [score, data]
