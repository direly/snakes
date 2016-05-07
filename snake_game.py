#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, time
import pygame
import snakes




def main():
    ELEM_WIDTH = 40
    COLOR_BACK = (220,220,220)
    COLOR_LINE = (230,230,230)
    COLOR_HEAD = (150,110,110)
    COLOR_BODY = (110,110,110)
    COLOR_CONN = (140,140,140)
    COLOR_FOOD = (110,110,220)

    HEIGHT, WIDTH, PLAY_MODE, GAME_SPEED = 0, 0, 0, 0
    while not (type(HEIGHT) is int and HEIGHT >= 2):
        HEIGHT = input("input board HEIGHT (must >= 2):")
    print "HEIGHT:", HEIGHT
    while not (type(WIDTH) is int and WIDTH >= 2):
        WIDTH = input("input board WIDTH (must >= 2):")
    print "WIDTH:", WIDTH
    while not (type(PLAY_MODE) is int and (PLAY_MODE == 1 or PLAY_MODE == 2 or PLAY_MODE == 3)):
        PLAY_MODE = input("input PLAY_MODE: \n\t1 - play snake game \n\t2 - auto snake mode1\n\t3 - auto snake mode2\n")
    print "PLAY_MODE:", PLAY_MODE
    while not (type(GAME_SPEED) is int and GAME_SPEED >= 1):
        GAME_SPEED = input("input GAME_SPEED (step per seconds, must >= 1):")
    print "GAME_SPEED:", GAME_SPEED

    snake = snakes.Snake(HEIGHT, WIDTH)
    direct = "" # up, down, left, right
    next_direct = "" # up, down, left, right

    pygame.init()
    board = snake.get_board()
    height = len(board)
    width = len(board[0])
    screen = pygame.display.set_mode((width*ELEM_WIDTH, height*ELEM_WIDTH), 0, 32)
    pygame.display.set_caption("Snake!")

    last_time = time.time()
    game_pause = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and direct != "down":
                    game_pause = False
                    next_direct = "up" 
                elif event.key == pygame.K_DOWN and direct != "up":
                    game_pause = False
                    next_direct = "down"
                elif event.key == pygame.K_LEFT and direct != "right":
                    game_pause = False
                    next_direct = "left"
                elif event.key == pygame.K_RIGHT and direct != "left":
                    game_pause = False
                    next_direct = "right"
                elif event.key == pygame.K_SPACE:
                    game_pause = not game_pause

        if game_pause:
            pygame.display.update()
            continue

        cur_time = time.time()
        if (cur_time - last_time) > (1.0 / GAME_SPEED) and "alive" == snake.get_status():
            last_time = cur_time

            if PLAY_MODE == 1:
                direct = next_direct
                snake.move(direct)
            elif PLAY_MODE == 2:
                snake.auto_move1()
            elif PLAY_MODE == 3:
                snake.auto_move2()
            else:
                assert(False)
            #print "time:%.5f status:%s len:%d" %(time.time(), snake.get_status(), len(snake.get_snake()))
        
            # 绘制背景和分割线
            screen.lock()
            screen.fill(COLOR_BACK)
            board, height, width = snake.get_board(), len(board), len(board[0])
            for i in range(height):
                pygame.draw.line(screen, COLOR_LINE, (0,i*ELEM_WIDTH), (width*ELEM_WIDTH-1,i*ELEM_WIDTH))
                pygame.draw.line(screen, COLOR_LINE, (0,(i+1)*ELEM_WIDTH-1), (width*ELEM_WIDTH-1,(i+1)*ELEM_WIDTH-1))
            for i in range(width):
                pygame.draw.line(screen, COLOR_LINE, (i*ELEM_WIDTH,0), (i*ELEM_WIDTH,height*ELEM_WIDTH-1))
                pygame.draw.line(screen, COLOR_LINE, ((i+1)*ELEM_WIDTH-1,0), ((i+1)*ELEM_WIDTH-1,height*ELEM_WIDTH-1))
            # 绘制 food
            (i, j) = snake.get_food()
            pygame.draw.ellipse(screen, COLOR_FOOD, (j*ELEM_WIDTH+4, i*ELEM_WIDTH+4, ELEM_WIDTH-8, ELEM_WIDTH-8))
            # 绘制 snake
            snake_list = snake.get_snake()
            for x in range(len(snake_list)):
                (i, j) = snake_list[x]
                if x == 0:
                    pygame.draw.rect(screen, COLOR_HEAD, (j*ELEM_WIDTH+1, i*ELEM_WIDTH+1, ELEM_WIDTH-2, ELEM_WIDTH-2))
                else:
                    (m, n) = snake_list[x-1]
                    pygame.draw.rect(screen, COLOR_BODY, (j*ELEM_WIDTH+1, i*ELEM_WIDTH+1, ELEM_WIDTH-2, ELEM_WIDTH-2))
                    if i == m and j > n:
                        pygame.draw.rect(screen, COLOR_CONN, (j*ELEM_WIDTH-1, i*ELEM_WIDTH+1, 2, ELEM_WIDTH-2))
                    elif i == m and j < n:
                        pygame.draw.rect(screen, COLOR_CONN, ((j+1)*ELEM_WIDTH-1, i*ELEM_WIDTH+1, 2, ELEM_WIDTH-2))
                    elif j == n and i > m:
                        pygame.draw.rect(screen, COLOR_CONN, (j*ELEM_WIDTH+1, i*ELEM_WIDTH-1, ELEM_WIDTH-2, 2))
                    elif j == n and i < m:
                        pygame.draw.rect(screen, COLOR_CONN, (j*ELEM_WIDTH+1, (i+1)*ELEM_WIDTH-1, ELEM_WIDTH-2, 2))
            screen.unlock()

        pygame.display.update()


if __name__ == "__main__":
    main()














