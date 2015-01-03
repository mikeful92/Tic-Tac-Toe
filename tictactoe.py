import pygame, sys, random
from pygame.locals import *


#settings for window
screenWidth  = 360
screenHeight = 360

#FPS
FPS = 24

#game settings
boxSize       =  96 # size of box height & width in pixels
boarderSize   =  33
lineThickness =   3
boardWidth    =   3
boardHeight   =   3
# 2x boader + 3x boxSize + 2x lineThickness = 360
assert (3 * boxSize) + (2 * boarderSize) + (2 * lineThickness) == 360, 'Board and boxes are not proper size'

#            R    G    B
GRAY     = (100, 100, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
BLUE     = (  0,   0, 255)
ORANGE   = (255, 128,   0)
BLACK    = (  0,   0,   0)

BGCOLOR  = WHITE
LINECOLOR = RED
SYMBOLCOLOR = BLACK
HIGHLIGHTCOLOR = BLUE

def main():
    #variables that need to be global
    global clock, screen
    #initiate pygame
    pygame.init()

    #game clock
    clock = pygame.time.Clock()

    #screen for display
    screen = pygame.display.set_mode((screenWidth, screenHeight))

    #create screen
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    screen.fill(BGCOLOR)

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Tic Tac Toe Game')

    mainBoard = newBoard()

    #game loop
    while True:
        mouseClicked = False
        screen.fill(BGCOLOR)
        drawBoard(mainBoard)
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy, boxState = getBoxAtPixel(mainBoard, mousex, mousey)

        if boxx != None and boxy != None and boxState == None:
            drawHighlightBox(boxx, boxy)
        if boxx != None and boxy != None and boxState == None and mouseClicked:
            markBox(mainBoard, boxx, boxy)
            mainBoard = computerMove(mainBoard)
            if hasWon(mainBoard):
                #gameWonAnimation(mainBoard)
                #pygame.time.wait(2000)

                #mainBoard = newBoard()

                #drawBoard(mainBoard)
                #pygame.display.update()
                #pygame.time.wait(1000)
                print "Congratulations"

        pygame.display.update()
        clock.tick(FPS)


def newBoard():
    board = []
    for x in range(3):
        for y in range(3):
            cell = [x,y, None]
            board.append(cell)
    return board

def drawBoard(board):
    line1Start  = (boarderSize + boxSize, boarderSize)
    line1End    = (boarderSize + boxSize,screenWidth - boarderSize)
    line2Start  = (boarderSize + boxSize + lineThickness + boxSize,boarderSize)
    line2End    = (boarderSize + boxSize + lineThickness + boxSize,screenWidth - boarderSize)
    line3Start  = (boarderSize,boarderSize + boxSize)
    line3End    = (screenWidth - boarderSize,boarderSize + boxSize)
    line4Start  = (boarderSize,boarderSize + boxSize + lineThickness + boxSize)
    line4End    = (screenWidth - boarderSize,boarderSize + boxSize + lineThickness + boxSize)

    pygame.draw.line(screen, LINECOLOR, line1Start, line1End, lineThickness)
    pygame.draw.line(screen, LINECOLOR, line2Start, line2End, lineThickness)
    pygame.draw.line(screen, LINECOLOR, line3Start, line3End, lineThickness)
    pygame.draw.line(screen, LINECOLOR, line4Start, line4End, lineThickness)

    for box in board:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        if box[2] == True:
            pygame.draw.circle(screen, LINECOLOR, (left + (boxSize/2), top + (boxSize/2)), 35, 2)
        if box[2] == False:
            pygame.draw.line(screen, LINECOLOR, (left + 10, top + 10), ((left + boxSize)-20,(top + boxSize)-20), 2)
            pygame.draw.line(screen, LINECOLOR, ((left + boxSize)-20, top + 10), (left + 10,(top + boxSize)-20), 2)

def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (boxSize + lineThickness) + boarderSize
    top = boxy * (boxSize + lineThickness) + boarderSize
    return (left, top)

def getBoxAtPixel(board, x, y):
    for box in board:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        boxRect = pygame.Rect(left, top, boxSize, boxSize)
        if boxRect.collidepoint(x, y):
            return (box[0], box[1], box[2])
    return (None, None, None)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(screen, HIGHLIGHTCOLOR, (left, top, boxSize - 4, boxSize - 4), 2)

def markBox(board, boxx, boxy):
    pos = (boxx*3) + boxy
    board[pos][2] = True

def hasWon(board):
    if board[0][2] and board[1][2] and board[2][2]:
        return True
    elif board[3][2] and board[4][2] and board[5][2]:
        return True
    elif board[6][2] and board[7][2] and board[8][2]:
        return True
    elif board[0][2] and board[3][2] and board[6][2]:
        return True
    elif board[1][2] and board[4][2] and board[7][2]:
        return True
    elif board[2][2] and board[5][2] and board[8][2]:
        return True
    elif board[0][2] and board[4][2] and board[8][2]:
        return True
    elif board[2][2] and board[4][2] and board[6][2]:
        return True

def computerMove(board):
    openBox = []
    #prevent win by cols
    if board[0][2] and board[1][2] and not board[2][2]:
        board[2][2] = False
    elif board[0][2] and board [2][2] and not board[1][2]:
        board[1][2] = False
    elif board[1][2] and board [2][2] and not board[0][2]:
        board[0][2] = False
    elif board[3][2] and board [4][2] and not board[5][2]:
        board[5][2] = False
    elif board[3][2] and board [5][2] and not board[4][2]:
        board[4][2] = False
    elif board[4][2] and board [5][2] and not board[3][2]:
        board[3][2] = False
    elif board[6][2] and board [7][2] and not board[8][2]:
        board[8][2] = False
    elif board[6][2] and board [8][2] and not board[7][2]:
        board[7][2] = False
    elif board[7][2] and board [8][2] and not board[6][2]:
        board[6][2] = False
    #prevent win by rows
    elif board[0][2] and board[3][2] and not board[6][2]:
        board[6][2] = False
    elif board[0][2] and board [6][2] and not board[3][2]:
        board[3][2] = False
    elif board[3][2] and board [6][2] and not board[0][2]:
        board[0][2] = False
    elif board[1][2] and board [4][2] and not board[7][2]:
        board[7][2] = False
    elif board[1][2] and board [7][2] and not board[4][2]:
        board[4][2] = False
    elif board[4][2] and board [7][2] and not board[1][2]:
        board[1][2] = False
    elif board[2][2] and board [5][2] and not board[8][2]:
        board[8][2] = False
    elif board[2][2] and board [8][2] and not board[5][2]:
        board[5][2] = False
    elif board[5][2] and board [8][2] and not board[2][2]:
        board[2][2] = False
    #prevent win by diagonal (top right to bot left)
    elif board[0][2] and board [4][2] and not board[8][2]:
        board[8][2] = False
    elif board[0][2] and board [8][2] and not board[4][2]:
        board[4][2] = False
    elif board[4][2] and board [8][2] and not board[0][2]:
        board[0][2] = False
    #prevent win by diagonal (bot left to top right)
    elif board[2][2] and board [4][2] and not board[6][2]:
        board[6][2] = False 
    elif board[2][2] and board [6][2] and not board[4][2]:
        board[4][2] = False 
    elif board[4][2] and board [6][2] and not board[2][2]:
        board[2][2] = False
    else:
        for box in board:
            if box[2] == None:
                openBox.append((box[0],box[1]))
        choice = random.sample(openBox, 1)
        choice = (choice[0][0]*3) + choice[0][1]
        board[choice][2] = False
    return board

if __name__ == '__main__':
    main()