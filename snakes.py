#!/usr/bin/python
# -*- coding:utf-8 -*-
import random, copy, os


def BoardIsContinues(board):
    if len(board) == 0 or len(board[0]) == 0:
        return False
    check_board = copy.deepcopy(board)
    max_l, max_c = len(check_board), len(check_board[0])

    check_elems = []
    for i in range(max_l):
        for j in range(max_c):
            if check_board[i][j] == "":
                check_elems.insert(0, (i, j))
                check_board[i][j] = "1"
                break
        if len(check_elems) > 0:
            break

    while True:
        if len(check_elems) == 0:
            break
        x = check_elems.pop()
        if x[0]-1 >= 0 and (check_board[x[0]-1][x[1]] == "" or check_board[x[0]-1][x[1]] == "food"):
            check_elems.insert(0, (x[0]-1, x[1]))
            check_board[x[0]-1][x[1]] = "1"
        if x[0]+1 < max_l and (check_board[x[0]+1][x[1]] == "" or check_board[x[0]+1][x[1]] == "food"):
            check_elems.insert(0, (x[0]+1, x[1]))
            check_board[x[0]+1][x[1]] = "1"
        if x[1]-1 >= 0 and (check_board[x[0]][x[1]-1] == "" or check_board[x[0]][x[1]-1] == "food"):
            check_elems.insert(0, (x[0], x[1]-1))
            check_board[x[0]][x[1]-1] = "1"
        if x[1]+1 < max_c and (check_board[x[0]][x[1]+1] == "" or check_board[x[0]][x[1]+1] == "food"):
            check_elems.insert(0, (x[0], x[1]+1))
            check_board[x[0]][x[1]+1] = "1"

    for i in range(max_l):
        for j in range(max_c):
            if check_board[i][j] == "":
                return False

    return True


def SnakeCanGetTail(board, snake):
    if len(board) == 0 or len(board[0]) == 0:
        return False
    check_board = copy.deepcopy(board)
    max_l, max_c = len(check_board), len(check_board[0])
    check_elems = [snake[0]]

    while True:
        if len(check_elems) == 0:
            break
        x = check_elems.pop()
        if x[0]-1 >= 0:
            if (x[0]-1, x[1]) == snake[-1]:
                return True
            if (check_board[x[0]-1][x[1]] == "" or check_board[x[0]-1][x[1]] == "food"):
                check_elems.insert(0, (x[0]-1, x[1]))
                check_board[x[0]-1][x[1]] = "1"
        if x[0]+1 < max_l:
            if (x[0]+1, x[1]) == snake[-1]:
                return True
            if (check_board[x[0]+1][x[1]] == "" or check_board[x[0]+1][x[1]] == "food"):
                check_elems.insert(0, (x[0]+1, x[1]))
                check_board[x[0]+1][x[1]] = "1"
        if x[1]-1 >= 0:
            if (x[0], x[1]-1) == snake[-1]:
                return True
            if (check_board[x[0]][x[1]-1] == "" or check_board[x[0]][x[1]-1] == "food"):
                check_elems.insert(0, (x[0], x[1]-1))
                check_board[x[0]][x[1]-1] = "1"
        if x[1]+1 < max_c:
            if (x[0], x[1]+1) == snake[-1]:
                return True
            if (check_board[x[0]][x[1]+1] == "" or check_board[x[0]][x[1]+1] == "food"):
                check_elems.insert(0, (x[0], x[1]+1))
                check_board[x[0]][x[1]+1] = "1"
    return False



class Snake:
    __board_height = 0
    __board_width = 0
    __board = [[]]
    __snake = []
    __food = (-1,-1)
    __status = "alive"
    __auto_direct_switch1 = True
    __auto_cur_direct2 = ""

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
        #self.move(self.get_auto_direction1())
        a = self.get_auto_direction2()
        print a
        if a != "up" and a != "down" and a != "left" and a != "right":
            os.system("pause")
        self.move(a)
        return


    ## 按固定规则来获取方向
    def get_auto_direction1(self):
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
                    if self.__auto_direct_switch1:
                        auto_direction = "left"
                    else:
                        auto_direction = "up"
                self.__auto_direct_switch1 = not self.__auto_direct_switch1
        return auto_direction


    ## 随机获取方向
    def get_auto_direction2(self):
        (i, j) = self.__snake[0]
        (f_i, f_j) = self.__food
        if self.__board_height < 2 or self.__board_width < 2:
            return "1"
        if i == f_i and j == f_j:
            return "2"

        direct_candidate = []
        if i == f_i:
            if j < f_j:
                direct_candidate = ["right", "up", "down", "left"]
            elif j > f_j:
                direct_candidate = ["left", "up", "down", "right"]
        elif i < f_i:
            if j >= f_j:
                direct_candidate = ["down", "left", "right", "up"]
            elif j < f_j:
                direct_candidate = ["down", "right", "left", "up"]
        else:
            if j >= f_j:
                direct_candidate = ["up", "left", "right", "down"]
            else:
                direct_candidate = ["up", "right", "left", "down"]
        
        if self.__auto_cur_direct2 == "up":
            direct_candidate.remove("down")
        elif self.__auto_cur_direct2 == "down":
            direct_candidate.remove("up")
        elif self.__auto_cur_direct2 == "left":
            direct_candidate.remove("right")
        elif self.__auto_cur_direct2 == "right":
            direct_candidate.remove("left")

        for x in direct_candidate:
            test_snake = copy.deepcopy(self.__snake)
            test_board = copy.deepcopy(self.__board)
            if self.__test_auto_direction2(test_snake, test_board, x):
                self.__auto_cur_direct2 = x
                return x
        else:
            return "3"


    def __test_auto_direction2(self, test_snake, test_board, direction):
        head, next_head = test_snake[0], None
        # 先检查是否撞墙
        if "up" == direction:
            if head[0] <= 0:
                return False
            else:
                next_head = (head[0]-1, head[1])
        elif "down" == direction:
            if head[0] >= self.__board_height - 1:
                return False
            else:
                next_head = (head[0]+1, head[1])
        elif "left" == direction:
            if head[1] <= 0:
                return False
            else:
                next_head = (head[0], head[1]-1)
        elif "right" == direction:
            if head[1] >= self.__board_width - 1:
                return False
            else:
                next_head = (head[0], head[1]+1)
        else:
            return False

        # 检查是否撞到自己
        for x in test_snake[0:len(test_snake)-1]:
            if x == next_head:
                return False

        # 移动，吃食
        if next_head == self.__food:
            test_snake.insert(0, next_head)
            test_board[next_head[0]][next_head[1]] = "head"
            test_board[head[0]][head[1]] = "body"
        else:
            tail = test_snake.pop()
            test_board[head[0]][head[1]] = "body"
            test_board[tail[0]][tail[1]] = ""
            test_board[next_head[0]][next_head[1]] = "head"
            test_snake.insert(0, next_head)

        # 检查 test_board 空白区域是否连续
        if not BoardIsContinues(test_board):
            print test_snake, test_board, direction, "BoardIsContinues"
            return False

        # 检查 test_snake 是否看得到尾巴
        if not SnakeCanGetTail(test_board, test_snake):
            print test_snake, test_board, direction, "SnakeCanGetTail"
            return False

        # 如果吃中食物，说明测试成功
        # 如果未吃中食物，则需要测试下一步是否成功
        if next_head == self.__food:
            return True
        else:
            (i, j) = test_snake[0]
            (f_i, f_j) = self.__food
            direct_candidate = []
            if i == f_i:
                if j < f_j:
                    direct_candidate = ["right", "up", "down", "left"]
                elif j > f_j:
                    direct_candidate = ["left", "up", "down", "right"]
            elif i < f_i:
                if j >= f_j:
                    direct_candidate = ["down", "left", "right", "up"]
                elif j < f_j:
                    direct_candidate = ["down", "right", "left", "up"]
            else:
                if j >= f_j:
                    direct_candidate = ["up", "left", "right", "down"]
                else:
                    direct_candidate = ["up", "right", "left", "down"]
            if direction == "up":
                direct_candidate.remove("down")
            elif direction == "down":
                direct_candidate.remove("up")
            elif direction == "left":
                direct_candidate.remove("right")
            elif direction == "right":
                direct_candidate.remove("left")

            for x in direct_candidate:
                new_test_snake = copy.deepcopy(test_snake)
                new_test_board = copy.deepcopy(test_board)
                if self.__test_auto_direction2(new_test_snake, new_test_board, x):
                    return True
            else:
                print test_snake, test_board, direction, "alltry"
                return False




