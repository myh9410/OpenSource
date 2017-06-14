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

    # 다음 블럭 사이드 메뉴에 그리기
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4):
        for j in range(4):
            dx = 505 + BOXSIZE * j
            dy = 140 + BOXSIZE * i
            if grid_n[i][j] != 0:
                pygame.draw.rect(DISPLAYSURF, UI.t_color[grid_n[i][j]], Rect(dx, dy, BOXSIZE, BOXSIZE))

    # 홀딩 블럭 사이드 메뉴에 그리기
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 505 + BOXSIZE * j
                dy = 50 + BOXSIZE * i
                if grid_h[i][j] != 0:
                    pygame.draw.rect(DISPLAYSURF, UI.t_color[grid_h[i][j]], Rect(dx, dy, BOXSIZE, BOXSIZE))

    # 점수 설정
    if score > 999999:
        score = 999999

    # 사이드 메뉴바에 보일 텍스트
    text_hold = UI.h5.render("HOLD", 1, UI.black)
    text_next = UI.h5.render("NEXT", 1, UI.black)
    text_score = UI.h5.render("SCORE", 1, UI.black)
    score_value = UI.h4.render(str(score), 1, UI.black)
    text_level = UI.h5.render("LEVEL", 1, UI.black)
    level_value = UI.h4.render(str(level), 1, UI.black)
    text_goal = UI.h5.render("GOAL", 1, UI.black)
    goal_value = UI.h4.render(str(goal), 1, UI.black)

    # 텍스트 위치
    DISPLAYSURF.blit(text_hold, (500, 14))
    DISPLAYSURF.blit(text_next, (500, 104))
    DISPLAYSURF.blit(text_score, (500, 194))
    DISPLAYSURF.blit(score_value, (505, 210))
    DISPLAYSURF.blit(text_level, (500, 254))
    DISPLAYSURF.blit(level_value, (505, 270))
    DISPLAYSURF.blit(text_goal, (500, 314))
    DISPLAYSURF.blit(goal_value, (505, 330))

    # 보드 만들기
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            dx = 75 + BOXSIZE * x
            dy = 19 + BOXSIZE * y
            draw_block(dx, dy, UI.t_color[matrix[x][y + 1]])

# 블럭 만들기
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

# 블럭 지우기
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
#초기 값 설정
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
    checkForQuit()#강제 종료
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
                    UI.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 8)
                else:
                    pause = False
                    UI.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 8)

    #게임 실행화면
    elif start:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # 낙하속도 설정
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, FPS * 2)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, FPS * 10)

                # 블럭 생성
                draw_mino(dx, dy, mino, rotation)
                draw_board(next_mino, hold_mino, score, level, goal)
    
                # 블럭 삭제
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)

                # 블럭 한칸씩 낙하
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1
    
                # 새 블럭 생성
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
                # 줄 삭제
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
                    UI.single_sound.play()
                    score += 50 * level
                elif erase_count == 2:
                    UI.double_sound.play()
                    score += 150 * level
                elif erase_count == 3:
                    UI.triple_sound.play()
                    score += 350 * level
                elif erase_count == 4:
                    UI.tetris_sound.play()
                    score += 1000 * level

                # 레벨 증가
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    goal += level * 5
                    FPS = int(FPS * 0.8)

            elif event.type == KEYDOWN:
                erase_mino(dx, dy, mino, rotation)
                if event.key == K_p:#pause 기능
                    UI.click_sound.play()
                    pause = True            
                elif event.key == K_SPACE:
                    UI.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, 8)
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif event.key == K_LSHIFT:#블럭 홀딩
                    if hold == False:
                        UI.move_sound.play()
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
                        UI.move_sound.play()
                        rotation += 1
                    elif is_turnable(dx, dy - 1, mino, rotation):
                        UI.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable(dx + 1, dy, mino, rotation):
                        UI.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable(dx - 1, dy, mino, rotation):
                        UI.move_sound.play()
                        dx -= 1
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif event.key == K_q:#역방향 회전
                    if is_turnable(dx, dy, mino, rotation):
                        UI.move_sound.play()
                        rotation -= 1
                    elif is_turnable(dx, dy - 1, mino, rotation):
                        UI.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable(dx + 1, dy, mino, rotation):
                        UI.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable(dx - 1, dy, mino, rotation):
                        UI.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif event.key == K_LEFT:#왼쪽 이동
                    if not is_leftedge(dx, dy, mino, rotation):
                        UI.move_sound.play()
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                elif event.key == K_RIGHT:#오른쪽 이동
                    if not is_rightedge(dx, dy, mino, rotation):
                        UI.move_sound.play()
                        dx += 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_board(next_mino, hold_mino, score, level, goal)
                
        pygame.display.update()

    # Game over 화면
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
    
    # Start 화면
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
                    UI.click_sound.play()
                    start = True

pygame.quit()
