#!/usr/bin/python
# -*- coding:utf-8 -*-
import random, copy, os


# 检查board是否连续
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

# 检查 head 和 tail 之间是否有阻隔
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


# 检查头尾是否相邻
def SnakeHeadNearTail(snake):
    if len(snake) <= 1:
        return False
    head, tail = snake[0], snake[-1]
    if head[0] == tail[0] and abs(head[1] - tail[1]) == 1:
        return True
    if head[1] == tail[1] and abs(head[0] - tail[0]) == 1:
        return True
    return False


class Snake:
    __board_height = 0
    __board_width = 0
    __board = [[]]
    __snake = []
    __food = (-1,-1)
    __status = "alive"
    ## for auto1
    __auto1_direct_switch = True
    ## for auto2
    __auto2_cur_direct_list = []
    __auto2_cur_direct = ""
    __auto2_cur_direct_type = ""
    __auto2_tested_snakes = []

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
        if self.__status == "full":
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
            if self.__check_win():
                self.__status = "full"
                return 
            self.__new_food()
        else:
            tail = self.__snake.pop()
            self.__board[head[0]][head[1]] = "body"
            self.__board[tail[0]][tail[1]] = ""
            self.__board[next_head[0]][next_head[1]] = "head"
            self.__snake.insert(0, next_head)
        return


    def auto_move1(self):
        if self.__status == "full":
            return 
        self.move(self.get_auto_direction1())

    def auto_move2(self):
        if self.__status == "full":
            return 
        if len(self.__auto2_cur_direct_list) == 0:
            self.get_auto_direction2()
        self.__auto2_cur_direct = self.__auto2_cur_direct_list.pop(0)
        self.move(self.__auto2_cur_direct)
        print self.__auto2_cur_direct, "\t", self.__auto2_cur_direct_type
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
                    if self.__auto1_direct_switch:
                        auto_direction = "left"
                    else:
                        auto_direction = "up"
                self.__auto1_direct_switch = not self.__auto1_direct_switch
        return auto_direction


    ## 通过尝试（回溯）来获取方向
    def get_auto_direction2(self):
        (i, j) = self.__snake[0]
        (f_i, f_j) = self.__food
        assert(self.__board_height >= 2 or self.__board_width >= 2)
        assert(not (i == f_i and j == f_j))
        assert(len(self.__auto2_cur_direct_list) == 0)

        # 1是离 food 更近的方向
        # 2是离 food 更远的方向
        direct_candidate_1 = []
        direct_candidate_2 = []
        if i == f_i:
            if j < f_j:
                direct_candidate_1 = ["right"]
                direct_candidate_2 = ["up", "down", "left"]
            elif j > f_j:
                direct_candidate_1 = ["left"]
                direct_candidate_2 = ["up", "down", "right"]
        elif i < f_i:
            if j > f_j:
                direct_candidate_1 = ["down", "left"]
                direct_candidate_2 = ["right", "up"]
            elif j < f_j:
                direct_candidate_1 = ["down", "right"]
                direct_candidate_2 = ["left", "up"]
            elif j == f_j:
                direct_candidate_1 = ["down"]
                direct_candidate_2 = ["right", "left", "up"]
        elif i > f_i:
            if j > f_j:
                direct_candidate_1 = ["up", "left"]
                direct_candidate_2 = ["right", "down"]
            elif j < f_j:
                direct_candidate_1 = ["up", "right"]
                direct_candidate_2 = ["left", "down"]
            elif j == f_j:
                direct_candidate_1 = ["up"]
                direct_candidate_2 = ["right", "left", "down"]
        
        # 除去不可以选的方向
        if self.__auto2_cur_direct == "up":
            if "down" in direct_candidate_1: direct_candidate_1.remove("down")
            if "down" in direct_candidate_2: direct_candidate_2.remove("down")
        elif self.__auto2_cur_direct == "down":
            if "up" in direct_candidate_1: direct_candidate_1.remove("up")
            if "up" in direct_candidate_2: direct_candidate_2.remove("up")
        elif self.__auto2_cur_direct == "left":
            if "right" in direct_candidate_1: direct_candidate_1.remove("right")
            if "right" in direct_candidate_2: direct_candidate_2.remove("right")
        elif self.__auto2_cur_direct == "right":
            if "left" in direct_candidate_1: direct_candidate_1.remove("left")
            if "left" in direct_candidate_2: direct_candidate_2.remove("left")

        # 除去可能撞墙、撞到自己的方向
        head = self.__snake[0]
        if head[0] <= 0:
            if "up" in direct_candidate_1: direct_candidate_1.remove("up")
            if "up" in direct_candidate_2: direct_candidate_2.remove("up")
        if head[0] >= self.__board_height - 1:
            if "down" in direct_candidate_1: direct_candidate_1.remove("down")
            if "down" in direct_candidate_2: direct_candidate_2.remove("down")
        if head[1] <= 0:
            if "left" in direct_candidate_1: direct_candidate_1.remove("left")
            if "left" in direct_candidate_2: direct_candidate_2.remove("left")
        if head[1] >= self.__board_width - 1:
            if "right" in direct_candidate_1: direct_candidate_1.remove("right")
            if "right" in direct_candidate_2: direct_candidate_2.remove("right")
        for x in self.__snake[0:len(self.__snake)-1]:
            if x == (head[0]-1, head[1]):
                if "up" in direct_candidate_1: direct_candidate_1.remove("up")
                if "up" in direct_candidate_2: direct_candidate_2.remove("up")
            if x == (head[0]+1, head[1]):
                if "down" in direct_candidate_1: direct_candidate_1.remove("down")
                if "down" in direct_candidate_2: direct_candidate_2.remove("down")
            if x == (head[0], head[1]-1):
                if "left" in direct_candidate_1: direct_candidate_1.remove("left")
                if "left" in direct_candidate_2: direct_candidate_2.remove("left")
            if x == (head[0], head[1]+1):
                if "right" in direct_candidate_1: direct_candidate_1.remove("right")
                if "right" in direct_candidate_2: direct_candidate_2.remove("right")

        random.shuffle(direct_candidate_1)
        random.shuffle(direct_candidate_2)
        self.__auto2_tested_snakes = []
        for x in direct_candidate_1 + direct_candidate_2:
            test_snake = copy.deepcopy(self.__snake)
            test_board = copy.deepcopy(self.__board)
            self.__auto2_cur_direct_list.append(x)
            self.__auto2_tested_snakes.append(self.__snake)
            result = self.__test_auto_direction2(test_snake, test_board, x, True, False)
            self.__auto2_tested_snakes.pop()
            if result:
                self.__auto2_cur_direct_type = "good"
                return 
            else:
                self.__auto2_cur_direct_list.pop()

        for x in direct_candidate_1 + direct_candidate_2:
            test_snake = copy.deepcopy(self.__snake)
            test_board = copy.deepcopy(self.__board)
            self.__auto2_cur_direct_list.append(x)
            self.__auto2_tested_snakes.append(self.__snake)
            result = self.__test_auto_direction2(test_snake, test_board, x, False, False)
            self.__auto2_tested_snakes.pop()
            if result:
                self.__auto2_cur_direct_type = "soso"
                return 
            else:
                self.__auto2_cur_direct_list.pop()

        if len(direct_candidate_1 + direct_candidate_2) > 0:
            self.__auto2_cur_direct_list.append(random.choice(direct_candidate_1 + direct_candidate_2))
            self.__auto2_cur_direct_type = "bad"
            return

        self.__auto2_cur_direct_list.append(random.choice(["up", "down", "left", "right"]))
        self.__auto2_cur_direct_type = "extremely_bad"
        return

    # deep_test: True - 递归检查; False - 不递归检查（只检查一步）
    # keep_distance: True - 要求头尾不相邻; False - 无要求
    def __test_auto_direction2(self, test_snake, test_board, direction, deep_test, keep_distance):
        #print "__test_auto_direction2: ", test_snake, test_board, direction
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
            # 如果和 self.__snake 形状相同，则会导致无限递归
            for s in self.__auto2_tested_snakes:
                if s == test_snake:
                    return False

        # 检查是否吃完
        if len(test_snake) == self.__board_height * self.__board_width:
            return True

        # 检查 test_board 空白区域是否连续
        # if not BoardIsContinues(test_board):
        #     #print test_snake, test_board, direction, "BoardIsContinues"
        #     return False

        # 检查 head 和 tail 是否相邻
        if keep_distance and SnakeHeadNearTail(test_snake):
            return False

        # 检查 test_snake 是否看得到尾巴
        if not SnakeCanGetTail(test_board, test_snake):
            #print test_snake, test_board, direction, "SnakeCanGetTail"
            return False

        if deep_test:
            # 深度检查逻辑：
            #   1. 如果吃中食物，说明测试成功
            #   2. 如果未吃中食物，则需要测试下一步是否成功
            if next_head == self.__food:
                return True
            else:
                # 1是离 food 更近的方向
                # 2是离 food 更远的方向
                (i, j) = test_snake[0]
                (f_i, f_j) = self.__food
                direct_candidate_1 = []
                direct_candidate_2 = []
                if i == f_i:
                    if j < f_j:
                        direct_candidate_1 = ["right"]
                        direct_candidate_2 = ["up", "down", "left"]
                    elif j > f_j:
                        direct_candidate_1 = ["left"]
                        direct_candidate_2 = ["up", "down", "right"]
                elif i < f_i:
                    if j > f_j:
                        direct_candidate_1 = ["down", "left"]
                        direct_candidate_2 = ["right", "up"]
                    elif j < f_j:
                        direct_candidate_1 = ["down", "right"]
                        direct_candidate_2 = ["left", "up"]
                    elif j == f_j:
                        direct_candidate_1 = ["down"]
                        direct_candidate_2 = ["right", "left", "up"]
                elif i > f_i:
                    if j > f_j:
                        direct_candidate_1 = ["up", "left"]
                        direct_candidate_2 = ["right", "down"]
                    elif j < f_j:
                        direct_candidate_1 = ["up", "right"]
                        direct_candidate_2 = ["left", "down"]
                    elif j == f_j:
                        direct_candidate_1 = ["up"]
                        direct_candidate_2 = ["right", "left", "down"]
                if direction == "up":
                    if "down" in direct_candidate_1: direct_candidate_1.remove("down")
                    if "down" in direct_candidate_2: direct_candidate_2.remove("down")
                elif direction == "down":
                    if "up" in direct_candidate_1: direct_candidate_1.remove("up")
                    if "up" in direct_candidate_2: direct_candidate_2.remove("up")
                elif direction == "left":
                    if "right" in direct_candidate_1: direct_candidate_1.remove("right")
                    if "right" in direct_candidate_2: direct_candidate_2.remove("right")
                elif direction == "right":
                    if "left" in direct_candidate_1: direct_candidate_1.remove("left")
                    if "left" in direct_candidate_2: direct_candidate_2.remove("left")
                random.shuffle(direct_candidate_1)
                random.shuffle(direct_candidate_2)

                for x in direct_candidate_1 + direct_candidate_2:
                    new_test_snake = copy.deepcopy(test_snake)
                    new_test_board = copy.deepcopy(test_board)
                    self.__auto2_cur_direct_list.append(x)
                    self.__auto2_tested_snakes.append(test_snake)
                    result = self.__test_auto_direction2(new_test_snake, new_test_board, x, True, False)
                    self.__auto2_tested_snakes.pop()
                    if result:
                        return True
                    else:
                        self.__auto2_cur_direct_list.pop()
                else:
                    #print test_snake, test_board, direction, "all no"
                    return False
        else:
            # 非深度检查，至此认为检查通过
            return True




