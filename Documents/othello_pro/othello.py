import pygame
from pygame.locals import *
import sys
import math

class Stone:
    def __init__(self,initial_color):
        self.__colors = ["white","black"]
        

def color(Num):
    if Num == 1:
        return "white"
    elif Num == 2:
        return "black"

def load_image(target):
    return pygame.image.load(target).convert_alpha()

pygame.init()
pygame.display.set_caption(u"Othelo")

board = [[0 for i in range(8)] for i in range(8)]
board[3][3] = board[4][4] = 1
board[3][4] = board[4][3] = 2

turn = 1

screen_SIZE = (500,500)
screen = pygame.display.set_mode(screen_SIZE)

boardImg = load_image('pic/board.png')
whiteImg = load_image('pic/white.png')
blackImg = load_image('pic/black.png')
# 白石 = 1 , 黒石 = 2 として扱う

myfont = pygame.font.SysFont(None, 60)

def put_stone(ImgNum,PosNum1,PosNum2):
    global Img
    if ImgNum == 1:
        Img = whiteImg
    elif ImgNum == 2:
        Img = blackImg
    Pos1 = PosNum1 * 50 + 20 + (PosNum1 + 1)
    Pos2 = PosNum2 * 50 + 20 + (PosNum2 + 1)

    return screen.blit(Img,(Pos1,Pos2))

def switch_turn(p_turn):
    global turn
    if p_turn == 1:
        return 2
    elif p_turn == 2:
        return 1

def ret_stone(sta1,sta2,end1,end2,direction):
    while True:
        p_sta1 = sta1 + direction[0]
        p_sta2 = sta2 + direction[1]
        board[p_sta1][p_sta2] = turn
        if p_sta1 == end1 and p_sta2 == end2:
            print(p_sta1,p_sta2,end1,end2,direction)
            break
        return

def set_stone(x, y):
    global turn

    direction = []

# 座標からクリックされたマスを割り出す
    Rx = x - 20
    Ry = y - 20
    squ1 = math.floor(Rx / (50 + 1))
    squ2 = math.floor(Ry / (50 + 1))

    Con1 = bool     # 石があらかじめそこにないこと
    Con2 = bool     # 石に隣接すること
    Con3 = bool     # 盤面の中にあること
    Con4 = bool     # 自分の石で相手の石を挟んでいること

# すでに石が置いてないか → 正常作動
    if board[squ1][squ2] == 0:
        Con1 = True
    else:
        Con1 = False

# 石に隣接するか → listの外の数が定義されてしまう
    for i in range(-1,2):
        for j in range(-1,2):
            if board[squ1 + i][squ2 + j] == 0 or board[squ1 + i][squ2 + j] == turn:
                pass
            else:
                Con2 = True
                direction.append([i,j])

    if Con2 != True:
        Con2 = False

# ボード上にますがにますが存在するか → 正常作動
    if 0 < Rx < 409 and 0 < Ry < 409:
        Con3 = True
    else:
        Con3 = False

# 相手の石を挟んでいるか → 製作中
    for direct in direction:
        p_squ1 = squ1
        p_squ2 = squ2
        while True:
            p_squ1 = p_squ1 + direct[0]
            p_squ2 = p_squ2 + direct[1]
            if p_squ1 == 8 or p_squ1 == -1 or p_squ2 == 8 or p_squ2 == -1:
                break
            if board[p_squ1][p_squ2] == turn:
                Con4 = True
                ret_stone(squ1,squ2,p_squ1,p_squ2,direct)
                break
            else:
                pass

        if Con4 != True:
            Con4 = False

# 上記4条件を満たした時実行
    if Con1 and Con2 and Con3 and Con4 == True:
        board[squ1][squ2] = turn
        turn = switch_turn(turn)
    else:
        pass

while True:
    screen.fill((0,0,0))
    screen.blit(boardImg,(20,20))

    str_turn = myfont.render("turn=" + str(color(turn)), True, (225,225,225))
    screen.blit(str_turn, (20,434))

    for i in range(0,8):
        for j in range(0,8):
            if board[i][j] == 0:
                pass
            elif board[i][j] == 1 or 2:
                put_stone(board[i][j],i,j)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            set_stone(x, y)
