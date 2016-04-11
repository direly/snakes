# -*- coding:utf-8 -*-
import sys, random, time
import pygame

max_l = 7 # must >= 2
max_c = 7 # must >= 2
elem_width = 40
back_color = (220,220,220)
snack_color = (110,110,110)
head_color = (150,110,110)
food_color = (110,110,220)
line_color = (230,230,230)
board = [ [0 for i in range(max_c)] for j in range(max_l) ]
snack = [(max_l/2, max_c/2)] # init snack
board[max_l/2][max_c/2] = 1 # init board
direct = 0 # init direct. 1-up, 2-down, 3-left, 4-right, 0-not_start
next_direct = 0


pygame.init()
screen = pygame.display.set_mode((max_c*elem_width, max_l*elem_width), 0, 32)
pygame.display.set_caption("Snake!")


# 控制snack的方向
# board的长宽必须都 >= 2
# def SnackAiDirect():




def SnackMove():
    '''
    rvalue: 1 -- win
    rvalue: 2 -- hit wall
    rvalue: 3 -- hit self
    rvalue: 4 -- continue
    '''
    global board, snack, screen, direct, next_direct
    
    SnackAiDirect()
    direct = next_direct

    head, next_head = snack[0], None
    # 获取head的下一个位置，并检查是否撞墙、是否撞到自己（撞自己的时候，不可能撞到尾巴）
    if 1 == direct:
        if head[0] <= 0:
            return 2
        else:
            next_head = (head[0]-1, head[1])
    elif 2 == direct:
        if head[0] >= max_l-1:
            return 2
        else:
            next_head = (head[0]+1, head[1])
    elif 3 == direct:
        if head[1] <= 0:
            return 2
        else:
            next_head = (head[0], head[1]-1)
    elif 4 == direct:
        if head[1] >= max_c-1:
            return 2
        else:
            next_head = (head[0], head[1]+1)
    for x in snack[0:len(snack)-1]:
        if x[0] == next_head[0] and x[1] == next_head[1]:
            return 3

    # 检查是否吃到食物
    if board[next_head[0]][next_head[1]] == 2:
        snack.insert(0, next_head)
        board[next_head[0]][next_head[1]] = 1
        # 下一个食物
        rlt = NewFood()
        if 1 == rlt:
            return 1
    else:
        tail = snack.pop()
        board[tail[0]][tail[1]] = 0
        snack.insert(0, next_head)
        board[next_head[0]][next_head[1]] = 1

    return 4 


def NewFood():
    '''
    rvalue: 1 -- borad full
    rvalue: 2 -- get food succ
    rvalue: 3 -- fail
    '''
    global board

    empty_cnt = 0
    for i in range(max_l):
        for j in range(max_c):
            if board[i][j] == 0:
                empty_cnt += 1
    if empty_cnt == 0:
        return 1
    
    dst_pos = random.randint(0,empty_cnt-1)
    for i in range(max_l):
        for j in range(max_c):
            if board[i][j] == 0:
                if dst_pos == 0:
                    board[i][j] = 2
                    return 2
                else:
                    dst_pos -= 1

    return 3


def PaintBoard():
    global board, screen, snack
    screen.fill(back_color)
    screen.lock()
    for i in range(max_l):
        for j in range(max_c):
            if board[i][j] == 1:
                pygame.draw.rect(screen, snack_color, (j*elem_width+1, i*elem_width+1, elem_width-2, elem_width-2))
            if board[i][j] == 2:
                pygame.draw.ellipse(screen, food_color, (j*elem_width+4, i*elem_width+4, elem_width-8, elem_width-8))
    i, j = snack[0][0], snack[0][1]
    pygame.draw.rect(screen, head_color, (j*elem_width+1, i*elem_width+1, elem_width-2, elem_width-2))
    for i in range(max_l):
        pygame.draw.line(screen, line_color, (0,i*elem_width), (max_l*elem_width-1,i*elem_width))
        pygame.draw.line(screen, line_color, (0,(i+1)*elem_width-1), (max_l*elem_width-1,(i+1)*elem_width-1))
    for i in range(max_c):
        pygame.draw.line(screen, line_color, (i*elem_width,0), (i*elem_width,max_c*elem_width-1))
        pygame.draw.line(screen, line_color, ((i+1)*elem_width-1,0), ((i+1)*elem_width-1,max_c*elem_width-1))
    screen.unlock()


def GetTick():
    return int(time.time() * 100)

NewFood()
timer =  GetTick() # init timer
status = 4
step = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    cur_time = GetTick()
    if timer != cur_time:
        timer = cur_time
        if status == 4:
            step += 1
            status = SnackMove()
            if 1 == status:
                print step, "win"
            elif 2 == status:
                print step, "hit wall"
            elif 3 == status:
                print step, "hit self"
            elif 4 == status:
                print step, "continue"
        
    PaintBoard()
    pygame.display.update()


