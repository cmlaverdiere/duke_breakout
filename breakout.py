import pygame, sys, math, random
from pygame.locals import *

def main():

    # Init
    pygame.init()
    screen = pygame.display.set_mode((640,360),0,32)
    close = pygame.time.Clock

    # Declarations
    COLUMN_LIM = 9
    ROW_LIM = 5
    X_OFFSET = 45
    Y_OFFSET = 15
    paddleLength = 40
    paddleHeight = 15
    ballWidth = 15
    ballHeight = 15

    paddleLoc = [300, 315]
    ballLoc = [313, 300]
    dxPaddle = 0
    dxBall = 0
    dyBall = 0
    blocksHitThisRun = 0

    paddleFile = "res/paddle.png"
    ballFile = "res/ball.png"
    backgroundFile = "res/bg%d.jpg" % random.randint(1,8)

    blockPurpleFile = "res/blockPurple.png"
    blockGreenFile= "res/blockGreen.png"
    blockBlueFile = "res/blockBlue.png"
    blockYellowFile = "res/blockYellow.png"
    blockRedFile = "res/blockRed.png"

    clock = pygame.time.Clock()

    paddleMovingLeft = False
    paddleMovingRight= False
    ballMovingLeft = False
    ballMovingRight= False
    ballMovingUp = False
    ballMovingDown = False
    hasWon = False
    dukeMode = False 
    victoryNotPlayed = True

    # Sounds
    blockBreak = pygame.mixer.Sound("res/blockBreak.ogg")
    dukeSong = pygame.mixer.Sound("res/DukeNukemThemeCut.ogg")
    gunShot = pygame.mixer.Sound("res/gunShot.ogg")
    gunCock = pygame.mixer.Sound("res/gunCock.ogg")
    damnImGood = pygame.mixer.Sound("res/damnImGood.ogg")
    holyShit = pygame.mixer.Sound("res/holyShit.ogg")

    # Fonts
    font = pygame.font.Font(None, 18)
    fontBig = pygame.font.Font(None, 36)
    descText = font.render("Controls: Space - Launch Ball  |  a / d - Left / Right  |  Chris Laverdiere 2012",  
                           1, (255, 255, 0))
    winText = fontBig.render("Congrats. You get nothing. Leave.", 1, (0, 0, 255))
    dukeText = font.render("Naa, sike. Restart the game and hit 'b' for a bonus.", 1, (255, 0, 0))
    dukeWinText = fontBig.render("Hail to the king, baby!", 1, (255, 255, 0))

    # Load Images
    paddle = pygame.image.load(paddleFile).convert_alpha()
    ball = pygame.image.load(ballFile).convert_alpha()
    background = pygame.image.load(backgroundFile).convert_alpha()

    redBlock = pygame.image.load(blockRedFile).convert_alpha()
    purpleBlock = pygame.image.load(blockPurpleFile).convert_alpha()
    blueBlock = pygame.image.load(blockBlueFile).convert_alpha()
    greenBlock = pygame.image.load(blockGreenFile).convert_alpha()
    yellowBlock = pygame.image.load(blockYellowFile).convert_alpha()
    colorBlockList = [redBlock, purpleBlock, blueBlock, greenBlock, yellowBlock]


    #Shapes
    class makeRect:
        def __init__(self, x, y, pos, obj):
            self.x = x
            self.y = y
            self.pos = (pos[0], pos[1])
            self.color = color
            self.obj = obj

    rectList = [[0 for i in xrange(COLUMN_LIM)] for j in xrange(ROW_LIM)] 

    for row in range(0, ROW_LIM):
        for column in range(0,COLUMN_LIM):
            shape = makeRect(55, 20, (60 * column + X_OFFSET , 25 * row + Y_OFFSET), colorBlockList[column % 5])
            rectList[row][column] = shape

    # Game Loop

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == K_a:
                    paddleMovingLeft = True

                elif event.key == K_d:
                    paddleMovingRight = True

                elif event.key == K_b and hasWon == False:
                    backgroundFile = "res/bg9.jpg"
                    background = pygame.image.load(backgroundFile).convert_alpha()
                    dukeMode = True
                    dukeSong.play(-1)
                    dukeSong.set_volume(1)

            elif event.type == KEYUP:
                if event.key == K_a:
                    paddleMovingLeft = False

                elif event.key == K_d:
                    paddleMovingRight = False

                elif event.key == K_SPACE:
                    ballMovingRight = True
                    ballMovingUp = True
                    if dukeMode:
                        gunCock.play()
                        gunCock.set_volume(1)

        # Movement vars 
        if paddleMovingLeft:
            dxPaddle = -7
            paddleLoc[0] += dxPaddle

        if paddleMovingRight:
            dxPaddle = 7
            paddleLoc[0] += dxPaddle

        if ballMovingRight:
            if dukeMode:
                dxBall = 6
            else:
                dxBall = 4

        if ballMovingLeft:
            if dukeMode:
                dxBall = -6
            else:
                dxBall = -4

        if ballMovingUp:
            if dukeMode:
                dyBall = -6
            else:
                dyBall = -4

        if ballMovingDown:
            if dukeMode:
                dyBall = 6
            else:
                dyBall = 4

        # Catch ball on borders:
        if ballLoc[0] < 0:
            ballMovingLeft = False
            ballMovingRight = True

        if ballLoc[0] > 640 - ballWidth:
            ballMovingRight = False 
            ballMovingLeft = True 

        if ballLoc[1] < 0 - ballWidth:
            ballMovingUp = False 
            ballMovingDown = True 

        # Paddle hit detection:
        if ballMovingUp or ballMovingDown:
            if ballLoc[1] in range(paddleLoc[1] - paddleHeight, paddleLoc[1]) \
                    and ballLoc[0] in range(paddleLoc[0] - ballWidth, paddleLoc[0] + paddleLength):
                ballMovingUp = True
                ballMovingDown = False
                blocksHitThisRun = 0

        # Block hit detection:
        for i, row in enumerate(rectList):
            for j, item in enumerate(row):
                if ballLoc[0] in range(item.pos[0],item.pos[0] + item.x) \
                        and ballLoc[1] in range(item.pos[1], item.pos[1] + item.y):
                    del(rectList[i][j])
                    ballMovingUp = not ballMovingUp
                    ballMovingDown = not ballMovingDown
                    if dukeMode:
                        gunShot.play()
                        gunShot.set_volume(1)
                        blocksHitThisRun += 1
                        if blocksHitThisRun >= 8:
                            holyShit.play()
                            holyShit.set_volume(1)
                            blocksHitThisRun = 0
                    else:
                        blockBreak.play()
                        blockBreak.set_volume(1)

        # Reset when player loses
        if ballLoc[1] > 360:
            ballLoc[0] = 313
            ballLoc[1] = 300 
            ballMovingLeft, ballMovingDown, ballMovingUp, ballMovingRight = False, False, False, False
            dxBall, dyBall = 0, 0
            blocksHitThisRun = 0

        # When all blocks destroyed:
        if all(len(row) == 0 for row in rectList): 
            hasWon = True

        # Update Positions
        ballLoc[0] += dxBall
        ballLoc[1] += dyBall

        # Draw items
        clock.tick(60)

        screen.blit(background, (0, 0))
        screen.blit(descText, (10, 340))
        screen.blit(paddle, paddleLoc)
        screen.blit(ball, ballLoc)

        if hasWon and dukeMode:
            screen.blit(dukeWinText, (195, 100))
            ballLoc[0] = 313
            ballLoc[1] = 300 
            ballMovingLeft, ballMovingDown, ballMovingUp, ballMovingRight = False, False, False, False
            dxBall, dyBall = 0, 0
            if victoryNotPlayed:
                damnImGood.play()
                damnImGood.set_volume(1)
                victoryNotPlayed = False

        elif hasWon:
            screen.blit(winText, (120,140))
            screen.blit(dukeText, (155, 170))
            ballLoc[0] = 313
            ballLoc[1] = 300 
            ballMovingLeft, ballMovingDown, ballMovingUp, ballMovingRight = False, False, False, False
            dxBall, dyBall = 0, 0

        # Draw all non-hit rectangles
        for row in rectList:
            for item in row:
                screen.blit(item.obj, item.pos)

        pygame.display.update()

if __name__ == "__main__":
    main()
