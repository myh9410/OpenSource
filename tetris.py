import random, time, pygame, sys
from pygame.locals import *
from tetrimino import *
from random import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 600
BOXSIZE = 28
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '1'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

pygame.init()

FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.time.set_timer(pygame.USEREVENT, FPS * 10)
pygame.display.set_caption('TETRIS')

class UI :
    #############################
    #        테트리스 색        #
    #############################IJLOSTZ
    #               R    G    B
    red         = (155,   0,   0)
    LIGHTRED    = (175,  20,  20)
    green       = (  0, 155,   0)
    LIGHTGREEN  = ( 20, 175,  20)
    blue        = (  0,   0, 155)
    LIGHTBLUE   = ( 20,  20, 175)
    yellow      = (155, 155,   0)
    LIGHTYELLOW = (175, 175,  20)
    cyan        = ( 69, 206, 204)
    orange      = (253, 189,  53)
    pink        = (255, 216, 216)
    white       = (255, 255, 255)

    #############################
    #           폰트            #
    #############################
    font_path = "./assets/fonts/OpenSans-Light.ttf"
    font_path_b = "./assets/fonts/OpenSans-Bold.ttf"

    h1 = pygame.font.Font(font_path, 50)
    h2 = pygame.font.Font(font_path, 30)
    h4 = pygame.font.Font(font_path, 20)
    h5 = pygame.font.Font(font_path, 13)
    h6 = pygame.font.Font(font_path, 10)

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 30)

    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    #############################
    #           사운드          #
    #############################    
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav")
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
    single_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
    double_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
    triple_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav")
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")

    #############################
    #           배경색          #
    ############################# 
    black = (10, 10, 10) #rgb(10, 10, 10)
    white = (255, 255, 255) #rgb(255, 255, 255)
    grey_1 = (26, 26, 26) #rgb(26, 26, 26)
    grey_2 = (35, 35, 35) #rgb(35, 35, 35)
    grey_3 = (55, 55, 55) #rgb(55, 55, 55)

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]

def draw_block(x, y, color):
    pygame.draw.rect(DISPLAYSURF, color, Rect(x, y, BOXSIZE, BOXSIZE))
    pygame.draw.rect(DISPLAYSURF, UI.black, Rect(x, y, BOXSIZE, BOXSIZE),1)

def draw_board(next, hold, score, level, goal):
    DISPLAYSURF.fill(UI.pink)

    pygame.draw.rect(
        DISPLAYSURF,
        UI.white,
        Rect(450, 0, 196, 600)
    )

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4):
        for j in range(4):
            dx = 505 + BOXSIZE * j
            dy = 140 + BOXSIZE * i
            if grid_n[i][j] != 0:
                pygame.draw.rect(DISPLAYSURF, UI.t_color[grid_n[i][j]], Rect(dx, dy, BOXSIZE, BOXSIZE))

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 505 + BOXSIZE * j
                dy = 50 + BOXSIZE * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(DISPLAYSURF, UI.t_color[grid_h[i][j]], Rect(dx, dy, BOXSIZE, BOXSIZE))

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = UI.h5.render("HOLD", 1, UI.black)
    text_next = UI.h5.render("NEXT", 1, UI.black)
    text_score = UI.h5.render("SCORE", 1, UI.black)
    score_value = UI.h4.render(str(score), 1, UI.black)
    text_level = UI.h5.render("LEVEL", 1, UI.black)
    level_value = UI.h4.render(str(level), 1, UI.black)
    text_goal = UI.h5.render("GOAL", 1, UI.black)
    goal_value = UI.h4.render(str(goal), 1, UI.black)

    # Place texts
    DISPLAYSURF.blit(text_hold, (500, 14))
    DISPLAYSURF.blit(text_next, (500, 104))
    DISPLAYSURF.blit(text_score, (500, 194))
    DISPLAYSURF.blit(score_value, (505, 210))
    DISPLAYSURF.blit(text_level, (500, 254))
    DISPLAYSURF.blit(level_value, (505, 270))
    DISPLAYSURF.blit(text_goal, (500, 314))
    DISPLAYSURF.blit(goal_value, (505, 330))

    # Draw board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            dx = 75 + BOXSIZE * x
            dy = 19 + BOXSIZE * y
            draw_block(dx, dy, UI.t_color[matrix[x][y + 1]])

# Draw a tetrimino
def draw_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r):
        ty += 1

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[tx + j][ty + i] = 8

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = grid[i][j]

# Erase a tetrimino
def erase_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for j in range(21):
        for i in range(10):
            if matrix[i][j] == 8:
                matrix[i][j] = 0

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = 0

def is_bottom(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (y + i + 1) > 20:
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
                    return True

    return False

def is_leftedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j - 1) < 0:
                    return True
                elif matrix[x + j - 1][y + i] != 0:
                    return True

    return False

def is_rightedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j + 1) > 9:
                    return True
                elif matrix[x + j + 1][y + i] != 0:
                    return True

    return False

def is_turnable(x, y, mino, r):
    if r != 3:
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True

def is_stackable(mino):
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            #print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False

    return True

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def checkForKeyPress():
    checkForQuit()
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def terminate():
    pygame.quit()
    sys.exit()

##############################################################################
##############################################################################
#initial values
blink = False
start = False
pause = False
done = False
game_over = False

score = 0
level = 1
goal = level * 5
bottom_count = 0
hard_drop = False

dx, dy = 3, 0
rotation = 0

mino = randint(1, 7)
next_mino = randint(1, 7)

hold = False
hold_mino = -1
                     
movingDown = False
movingLeft = False
movingRight = False
                         

matrix = [[0 for y in range(BOARDHEIGHT + 1)] for x in range(BOARDWIDTH)]
          
#####################################################################
while not done:
    # 게임 퍼즈화면
    checkForQuit()
    if pause : 
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT :
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                draw_board(next_mino, hold_mino, score, level, goal)
                pause_text = UI.h2_b.render("PAUSED", 1, UI.white)
                pause_start = UI.h5.render("Press any key to continue", 1, UI.white)
                DISPLAYSURF.blit(pause_text, (157, 210))
                if blink:
                    DISPLAYSURF.blit(pause_start, (143, 290))
                    blink = False
                else:
                    blink = True
                pygame.display.update()
            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_p:
                    pause = False
                    pygame.time.set_timer(pygame.USEREVENT, 8)
                else:
                    pause = False
                    pygame.time.set_timer(pygame.USEREVENT, 8)

        #게임 실행화면
    elif start:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, FPS * 2)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, FPS * 10)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation)
                draw_board(next_mino, hold_mino, score, level, goal)
    
                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                # Move mino down
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1
    
                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation)
                        draw_board(next_mino, hold_mino, score, level, goal)
                        if is_stackable(next_mino):
                            mino = next_mino
                            next_mino = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else:
                            start = False
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 8)
                    else:
                        bottom_count += 1
                # Erase line
                erase_count = 0
                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        k = j
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1
                if erase_count == 1:
                    score += 50 * level
                elif erase_count == 2:
                    score += 150 * level
                elif erase_count == 3:
                    score += 350 * level
                elif erase_count == 4:
                    score += 1000 * level

                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    goal += level * 5
                    FPS = int(FPS * 0.8)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_p:#pause 기능
                    pause = True            
                elif event.key == K_SPACE:
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, 8)
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif event.key == K_LSHIFT:#블럭 홀딩
                    if hold == False:
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino
                            next_mino = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif event.key == K_UP:#정방향 회전
                    if is_turnable(dx, dy, mino, rotation):
                        rotation += 1
                    elif is_turnable(dx, dy - 1, mino, rotation):
                        dy -= 1
                        rotation += 1
                    elif is_turnable(dx + 1, dy, mino, rotation):
                        dx += 1
                        rotation += 1
                    elif is_turnable(dx - 1, dy, mino, rotation):
                        dx -= 1
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif event.key == K_q:#역방향 회전
                    if is_turnable(dx, dy, mino, rotation):
                        rotation -= 1
                    elif is_turnable(dx, dy - 1, mino, rotation):
                        dy -= 1
                        rotation += 1
                    elif is_turnable(dx + 1, dy, mino, rotation):
                        dx += 1
                        rotation += 1
                    elif is_turnable(dx - 1, dy, mino, rotation):
                        dx -= 1
                        rotation -= 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif event.key == K_LEFT:#왼쪽 이동
                    if not is_leftedge(dx, dy, mino, rotation):
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif event.key == K_RIGHT:#오른쪽 이동
                    if not is_rightedge(dx, dy, mino, rotation):
                        dx += 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                
        pygame.display.update()

    # Game over screen
    elif game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                over_text_1 = UI.h2_b.render("GAME", 1, UI.white)
                over_text_2 = UI.h2_b.render("OVER", 1, UI.white)
                over_start = UI.h5.render("Press SPACE BAR to continue", 1, UI.white)

                draw_board(next_mino, hold_mino, score, level, goal)
                DISPLAYSURF.blit(over_text_1, (168, 230))
                DISPLAYSURF.blit(over_text_2, (168, 260))
    
                if blink:
                    DISPLAYSURF.blit(over_start, (132, 320))
                    blink = False
                else:
                    blink = True
    
                pygame.display.update()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game_over = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    matrix = [[0 for y in range(BOARDHEIGHT + 1)] for x in range(BOARDWIDTH)]
                    pygame.time.set_timer(pygame.USEREVENT, 8)
    
    # Start screen
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                DISPLAYSURF.fill(UI.white)
                pygame.draw.rect(
                    DISPLAYSURF,
                    UI.black,
                    Rect(0, 0, 640, 600)
                )

                title = UI.h1.render("TETRIS", 1, UI.red)
                title_start = UI.h5.render("Press space to start", 1, UI.white)

                if blink:
                    DISPLAYSURF.blit(title_start, (257, 300))
                    blink = False
                else:
                    blink = True
                DISPLAYSURF.blit(title, (240, 200))
    
                pygame.display.update()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    start = True

pygame.quit()


'''



                #블럭 회전
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                #블럭 역방향 회전
                elif (event.key == K_q): 
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                # 아래키 누르면 블럭 빠르게 떨어짐.
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # 블럭 한번에 떨굼
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1
                # 블럭 홀딩
                elif event.key == K_LSHIFT:
                    if hold == False:
                        if holdPiece == getHoldPiece():
                            holdPiece = fallingPiece
                            fallingPiece = nextPiece
                            nextPiece = getNewPiece()
                        else:
                            holdPiece, fallingPiece = fallingPiece, holdPiece
                        hold = True

                
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # 게임 화면 상에 보여줌
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        showNextPiece(nextPiece)
        showHoldPiece(holdPiece)
        if fallingPiece != None:
            drawNextPiece(fallingPiece)
            drawHoldPiece(holdPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
#######################################################################


def drawBoard(next, hold, score, level, goal):
    # 경계선 만듦
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN, TOPMARGIN, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # 보드 배경
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])
#############################################################################

################################################################################
#def runGame의 끝
################################################################################
def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():#종료
    pygame.quit()
    sys.exit()

def showTextScreen(text):
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR2)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = makeTextObjs('Press any key to Start.', BASICFONT, TEXTCOLOR2)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def calculateLevelAndFallFreq(score):
    #레벨 설정. 레벨에 따라 떨어지는 속도 빨라짐.
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getNewPiece():#랜덤으로 모양 나옴.
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # 블럭 떨어지는 위치
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece

def getHoldPiece():
    shape = random.choice(list(NOPIECE.keys()))
    holdPiece = {'shape': shape,
                'rotation': 0,
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # 블럭 떨어지는 위치
                'color': random.randint(0, len(COLORS)-1)}
    return holdPiece

def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']         

#보드 
def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def removeCompleteLines(board):
    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1 # move on to check next row up
    return numLinesRemoved


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

#########################################################
#실제 게임화면에서 보이는 부분들↓↓↓↓↓↓↓↓↓↓↓↓#
#########################################################
def drawBoard(next, hold, score, level, goal):
    # 경계선 만듦
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN, TOPMARGIN, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # 보드 배경
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

def drawNextPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))
                
def drawStatus(score, level):
    # 점수 표시
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 420)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # 레벨 표시
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 450)
    DISPLAYSURF.blit(levelSurf, levelRect)

def showNextPiece(piece):
    #다음에 나올 모양에 대한 Next라는 텍스트 보여줌.
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 150, 480)
    DISPLAYSURF.blit(nextSurf, nextRect)
    #다음에 나올 모양 보여줌
    drawNextPiece(piece, pixelx=WINDOWWIDTH-150, pixely=500)

def drawHoldPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = NOPIECE[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def showHoldPiece(piece):
    #다음에 나올 모양에 대한 Next라는 텍스트 보여줌.
    nextSurf = BASICFONT.render('Hold:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 150, 280)
    DISPLAYSURF.blit(nextSurf, nextRect)
    #다음에 나올 모양 보여줌
    drawHoldPiece(piece, pixelx=WINDOWWIDTH-150, pixely=320)  

if __name__ == '__main__':
    main()
'''
