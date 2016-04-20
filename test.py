#!/usr/bin/python
# -*- coding:utf-8 -*-
import snakes

def main():
    board = [["2", "2"],["", ""]]
    print snakes.BoardIsContinues(board)
    for i in range(len(board)):
        print board[i]




if __name__ == "__main__":
    main()

