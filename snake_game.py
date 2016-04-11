#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, time
import pygame
import snakes



# 用于控制速度
def GetTick():
    return int(time.time() * 2)


def main():
    ELEM_WIDTH = 40
    COLOR_BACK = (220,220,220)
    COLOR_LINE = (230,230,230)
    COLOR_BODY = (110,110,110)
    COLOR_HEAD = (150,110,110)
    COLOR_FOOD = (110,110,220)

    snake = snakes.Snake(9,9)
    direct = "" # up, down, left, right
    next_direct = "" # up, down, left, right

    pygame.init()
    board = snake.get_board()
    height = len(board)
    width = len(board[0])
    screen = pygame.display.set_mode((width*ELEM_WIDTH, height*ELEM_WIDTH), 0, 32)
    pygame.display.set_caption("Snake!")

    last_tick = GetTick()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and direct != "down":
                    next_direct = "up" 
                elif event.key == pygame.K_DOWN and direct != "up":
                    next_direct = "down"
                elif event.key == pygame.K_LEFT and direct != "right":
                    next_direct = "left"
                elif event.key == pygame.K_RIGHT and direct != "left":
                    next_direct = "right"
        cur_tick = GetTick()
        if cur_tick != last_tick and "alive" == snake.get_status():
            last_tick = cur_tick
            direct = next_direct
            snake.move(direct)
            print snake.get_status()
        
            # 绘制screen
            board = snake.get_board()
            height = len(board)
            width = len(board[0])
            screen.fill(COLOR_BACK)
            screen.lock()
            for i in range(height):
                for j in range(width):
                    if board[i][j] == "head":
                        pygame.draw.rect(screen, COLOR_HEAD, (j*ELEM_WIDTH+1, i*ELEM_WIDTH+1, ELEM_WIDTH-2, ELEM_WIDTH-2))
                    elif board[i][j] == "body":
                        pygame.draw.rect(screen, COLOR_BODY, (j*ELEM_WIDTH+1, i*ELEM_WIDTH+1, ELEM_WIDTH-2, ELEM_WIDTH-2))
                    elif board[i][j] == "food":
                        pygame.draw.ellipse(screen, COLOR_FOOD, (j*ELEM_WIDTH+4, i*ELEM_WIDTH+4, ELEM_WIDTH-8, ELEM_WIDTH-8))
            for i in range(height):
                pygame.draw.line(screen, COLOR_LINE, (0,i*ELEM_WIDTH), (height*ELEM_WIDTH-1,i*ELEM_WIDTH))
                pygame.draw.line(screen, COLOR_LINE, (0,(i+1)*ELEM_WIDTH-1), (height*ELEM_WIDTH-1,(i+1)*ELEM_WIDTH-1))
            for i in range(width):
                pygame.draw.line(screen, COLOR_LINE, (i*ELEM_WIDTH,0), (i*ELEM_WIDTH,width*ELEM_WIDTH-1))
                pygame.draw.line(screen, COLOR_LINE, ((i+1)*ELEM_WIDTH-1,0), ((i+1)*ELEM_WIDTH-1,width*ELEM_WIDTH-1))
            screen.unlock()

        pygame.display.update()


if __name__ == "__main__":
    main()














