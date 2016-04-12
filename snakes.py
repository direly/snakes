#!/usr/bin/python
# -*- coding:utf-8 -*-
import random, copy


class Snake:
    __board_height = 0
    __board_width = 0
    __board = [[]]
    __snake = []
    __food = (-1,-1)
    __status = "alive"
    __switch1 = True

    def __init__(self, board_height, board_width):
        if board_height < 2:
            board_height = 2
        if board_width < 2:
            board_width = 2
        self.__board = [ ["" for i in range(board_width)] for j in range(board_height) ]
        self.__board_height = board_height
        self.__board_width = board_width
        self.__snake.append((board_height/2, board_width/2))
        self.__board[board_height/2][board_width/2] = "head"
        self.__new_food()


    def __check_win(self):
        empty_place_cnt = 0
        for i in range(self.__board_height):
            for j in range(self.__board_width):
                if self.__board[i][j] != "head" and self.__board[i][j] != "body":
                    empty_place_cnt += 1
        if empty_place_cnt == 0:
            return True
        else:
            return False


    def __new_food(self):
        food_pos = None
        empty_place_cnt = 0
        for i in range(self.__board_height):
            for j in range(self.__board_width):
                if self.__board[i][j] == "":
                    empty_place_cnt += 1
                    if 1 == random.randint(1, empty_place_cnt):
                        food_pos = (i, j)
        if empty_place_cnt == 0:
            return False
        else:
            self.__board[food_pos[0]][food_pos[1]] = "food"
            self.__food = food_pos
            return True


    def get_status(self):
        return copy.deepcopy(self.__status)


    def get_board(self):
        return copy.deepcopy(self.__board)


    def get_snake(self):
        return copy.deepcopy(self.__snake)


    def get_food(self):
        return copy.deepcopy(self.__food)


    def move(self, direction):
        # 检查是否win
        if self.__check_win():
            self.__status = "full"
            return
        head, next_head = self.__snake[0], None
        # 检查是否撞墙
        if "up" == direction:
            if head[0] <= 0:
                self.__status = "death - hit wall"
                return 
            else:
                next_head = (head[0]-1, head[1])
        elif "down" == direction:
            if head[0] >= self.__board_height - 1:
                self.__status = "death - hit wall"
                return 
            else:
                next_head = (head[0]+1, head[1])
        elif "left" == direction:
            if head[1] <= 0:
                self.__status = "death - hit wall"
                return 
            else:
                next_head = (head[0], head[1]-1)
        elif "right" == direction:
            if head[1] >= self.__board_width - 1:
                self.__status = "death - hit wall"
                return 
            else:
                next_head = (head[0], head[1]+1)
        else:
            return
        # 检查是否撞到自己
        for x in self.__snake[0:len(self.__snake)-1]:
            if x == next_head:
                self.__status = "death - hit self"
                return 
        # 移动，吃食
        if next_head == self.__food:
            self.__snake.insert(0, next_head)
            self.__board[next_head[0]][next_head[1]] = "head"
            self.__board[head[0]][head[1]] = "body"
            self.__new_food()
        else:
            tail = self.__snake.pop()
            self.__board[head[0]][head[1]] = "body"
            self.__board[tail[0]][tail[1]] = ""
            self.__board[next_head[0]][next_head[1]] = "head"
            self.__snake.insert(0, next_head)
        return


    def auto_move(self):
        self.move(self.get_auto_direction())
        return


    def get_auto_direction(self):
        (i, j) = self.__snake[0]
        if self.__board_height < 2 or self.__board_width < 2:
            return ""

        if self.__board_height == 2:
            if i == 0:
                if j == self.__board_width - 1:
                    auto_direction = "down"
                else:
                    auto_direction = "right"
            else:
                if j == 0:
                    auto_direction = "up"
                else:
                    auto_direction = "left"
            return auto_direction

        if self.__board_width == 2:
            if j == 0:
                if i == 0:
                    auto_direction = "right"
                else:
                    auto_direction = "up"
            else:
                if i == self.__board_height - 1:
                    auto_direction = "left"
                else:
                    auto_direction = "down"
            return auto_direction

        # 列是偶数
        if self.__board_width % 2 == 0:
            if i == 0:
                if j == 0:
                    auto_direction = "down"
                else:
                    auto_direction = "left"
            else:
                if j == self.__board_width - 1:
                    auto_direction = "up"
                elif j % 2 == 0:
                    if i == self.__board_height - 1:
                        auto_direction = "right"
                    else:
                        auto_direction = "down"
                else:
                    if i == 1:
                        auto_direction = "right"
                    else:
                        auto_direction = "up"
            return auto_direction

        # 行是偶数
        if self.__board_height % 2 == 0:
            if j == 0:
                if i == self.__board_height - 1:
                    auto_direction = "right"
                else:
                    auto_direction = "down"
            else:
                if i == 0:
                    auto_direction = "left"
                elif i % 2 == 1:
                    if j == self.__board_width - 1:
                        auto_direction = "up"
                    else:
                        auto_direction = "right"
                else:
                    if j == 1:
                        auto_direction = "up"
                    else:
                        auto_direction = "left"
            return auto_direction

        # 行和列都是单数，这个情况稍微复杂点
        if self.__board_height % 2 == 1 and self.__board_width % 2 == 1:
            if j < self.__board_width - 2:
                if i == 0:
                    if j == 0:
                        auto_direction = "down"
                    else:
                        auto_direction = "left"
                else:
                    if j % 2 == 0:
                        if i == self.__board_height - 1:
                            auto_direction = "right"
                        else:
                            auto_direction = "down"
                    else:
                        if i == 1:
                            auto_direction = "right"
                        else:
                            auto_direction = "up"
            elif i > 1:
                if j == self.__board_width - 1:
                    if i % 2 == 0:
                        auto_direction = "up"
                    else:
                        auto_direction = "left"
                else:
                    if i % 2 == 0:
                        auto_direction = "right"
                    else:
                        auto_direction = "up"
            else:
                if i == 0 and j == self.__board_width - 2:
                    auto_direction = "left"
                if i == 0 and j == self.__board_width - 1:
                    auto_direction = "left"
                if i == 1 and j == self.__board_width - 2:
                    auto_direction = "up"
                if i == 1 and j == self.__board_width - 1:
                    if self.__switch1:
                        auto_direction = "left"
                    else:
                        auto_direction = "up"
                self.__switch1 = not self.__switch1
        return auto_direction



